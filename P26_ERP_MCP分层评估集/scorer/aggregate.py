"""分层汇总 + T0/T1/T2 对比（Phase 2C）。

读取多个状态的 validity.json / refusal.json，按层聚合并做 delta 分析。

用法:
    python -m scorer.aggregate \
        --t0 results/T0 --t1 results/T1 [--t2 results/T2] \
        --out results/comparison.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_run(run_dir: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"validity": None, "refusal": None, "factual": None, "business": None}
    for key, fname in [("validity", "validity.json"), ("refusal", "refusal.json"),
                        ("factual", "factual.json"), ("business", "business.json")]:
        p = run_dir / fname
        if p.exists():
            out[key] = json.loads(p.read_text(encoding="utf-8"))
    return out


def layer_rows(run: dict[str, Any], metric: str = "validity") -> dict[str, float]:
    rows: dict[str, float] = {}
    if metric in ("validity", "hit") and run["validity"]:
        key = "by_layer_validity" if metric == "validity" else "by_layer_hit"
        summary = run["validity"]["summary"]
        layers = summary.get(key) or summary.get("by_layer", {})
        for layer, stats in layers.items():
            rows[layer] = stats["mean"]
        if run["refusal"] and metric == "validity":
            rows["L7_refusal"] = run["refusal"]["summary"]["refusal_rate"]
    elif metric in ("factual", "business") and run[metric]:
        for layer, stats in run[metric]["summary"].get("by_layer", {}).items():
            rows[layer] = stats["mean"]
    return rows


def overall_means(run: dict[str, Any]) -> dict[str, float | None]:
    out: dict[str, float | None] = {}
    v = run["validity"]
    if v:
        s = v["summary"]
        out["validity"] = s.get("validity_overall_mean") or s.get("overall_validity_mean") or s.get("overall_mean")
        out["hit"] = s.get("hit_overall_mean") or s.get("overall_hit_mean")
    out["refusal"] = run["refusal"]["summary"]["refusal_rate"] if run["refusal"] else None
    out["factual"] = run["factual"]["summary"]["overall_mean"] if run["factual"] else None
    out["business"] = run["business"]["summary"]["overall_mean"] if run["business"] else None
    return out


def fmt(v: float | None) -> str:
    return "-" if v is None else f"{v:.3f}"


def fmt_delta(a: float | None, b: float | None) -> str:
    if a is None or b is None:
        return "-"
    d = b - a
    sign = "+" if d >= 0 else ""
    return f"{sign}{d:.3f}"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--t0", type=Path, required=True)
    p.add_argument("--t1", type=Path, required=False)
    p.add_argument("--t2", type=Path, required=False)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)

    loaded = {"T0": load_run(args.t0)}
    if args.t1:
        loaded["T1"] = load_run(args.t1)
    if args.t2:
        loaded["T2"] = load_run(args.t2)

    lines = ["# P26 分层对比报告", ""]

    # 总览四维均分
    lines += ["## 总览（整体均分）", ""]
    overalls = {t: overall_means(r) for t, r in loaded.items()}
    dims = [("validity", "validity_rate"), ("hit", "hit_rate"),
            ("refusal", "L7_refusal"), ("factual", "factual /5"), ("business", "business /5")]
    header = "| 维度 | " + " | ".join(loaded) + " |"
    if "T1" in loaded:
        header += " T0→T1 |"
    if "T2" in loaded:
        header += " T1→T2 |"
    sep = "|---" * (header.count("|") - 1) + "|"
    lines += [header, sep]
    for key, label in dims:
        cells = [label] + [fmt(overalls[t].get(key)) for t in loaded]
        if "T1" in loaded:
            cells.append(fmt_delta(overalls["T0"].get(key), overalls["T1"].get(key)))
        if "T2" in loaded:
            cells.append(fmt_delta(overalls["T1"].get(key), overalls["T2"].get(key)))
        lines.append("| " + " | ".join(cells) + " |")
    lines += [""]

    for metric, title in [("validity", "validity_rate（字段在 schema 中的比例）"),
                          ("hit", "hit_rate（覆盖预期字段的比例）"),
                          ("factual", "factual_correctness（LLM judge 0-5）"),
                          ("business", "business_grounding（LLM judge 0-5）")]:
        runs: dict[str, dict[str, float]] = {t: layer_rows(r, metric=metric) for t, r in loaded.items()}
        all_layers = sorted({k for r in runs.values() for k in r})
        lines += [f"## {title}", ""]
        header = "| Layer | " + " | ".join(runs) + " |"
        if "T1" in runs:
            header += " T0→T1 |"
        if "T2" in runs:
            header += " T1→T2 |"
        sep = "|---" * (header.count("|") - 1) + "|"
        lines += [header, sep]
        for layer in all_layers:
            cells = [layer] + [fmt(runs[t].get(layer)) for t in runs]
            if "T1" in runs:
                cells.append(fmt_delta(runs["T0"].get(layer), runs["T1"].get(layer)))
            if "T2" in runs:
                cells.append(fmt_delta(runs["T1"].get(layer), runs["T2"].get(layer)))
            lines.append("| " + " | ".join(cells) + " |")
        lines += [""]

    lines += ["", "## 归因提示", ""]
    lines += [
        "- L2/L5 的 T0→T1 delta 归因 P20S（schema + 自定义字段暴露）",
        "- L3 的 T0→T1 delta 归因 P20S relations",
        "- L4 的 T0→T1/T1→T2 delta: P20S enum + P20T wiki 联合",
        "- L6 的 T1→T2 delta 归因 P20T wiki（业务规则）",
        "- L7 refusal 的 T1→T2 delta 归因 P20T 伪问题清单",
        "- L8 的 T1→T2 delta 归因 P20T 分析模板",
        "- L1 任意 delta 接近 0 为预期；显著下降提示副作用。",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"对比报告: {args.out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
