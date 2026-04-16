"""field_validity_rate 自动评分器（Phase 2A）。

定义: 答案文本中引用的字段 key（如 FBillNo, FApplicationDeptId.FName）
      有多少比例真实存在于对应 form 的 schema 中。

用法:
    python -m scorer.validity \
        --answers results/T1/answers.jsonl \
        --questions questions/_all.json \
        --schema-dir 源代码/mcp-kingdee-server/schema \
        --out results/T1/validity.json

answers.jsonl 每行格式:
    {"id": "L2-01", "answer": "...字段 FApplicationDeptId, FDate..."}
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from statistics import mean
from typing import Any

# 字段抽取规则：支持标准字段（FNumber）+ 自定义字段（F_BDK_LXR）
# 需要同时匹配 F 后跟大写字母，或 F_ 后跟大写字母
_FIELD_RE = re.compile(r"F_?[A-Z][A-Za-z0-9_]*")


def extract_schema_keys(schema_md: str) -> set[str]:
    """从 P20S 产出的 schema/{form}.md 抽取字段 key（表格第一列 `FXxx`）。"""
    keys: set[str] = set()
    for line in schema_md.splitlines():
        if line.startswith("| `") and "` |" in line:
            end = line.index("`", 3)
            keys.add(line[3:end])
    return keys


def extract_answer_fields(answer_text: str) -> list[str]:
    """从答案文本中抽取所有 F 开头的字段引用（去重保序）。"""
    seen: set[str] = set()
    out: list[str] = []
    for m in _FIELD_RE.findall(answer_text):
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def validity_rate(picked: list[str], valid_keys: set[str]) -> float:
    if not picked:
        return 0.0
    if not valid_keys:
        return 0.0
    hits = 0
    for p in picked:
        base = p.split(".")[0]
        if base in valid_keys:
            hits += 1
    return hits / len(picked)


def hit_rate(picked: list[str], expected: list[str]) -> float | None:
    """picked 里命中 expected（答案要点中预期字段）的比例。None 表示题目无 hint。"""
    if not expected:
        return None
    picked_set = set(picked)
    # 同时考虑全 key 和 base（截掉 .FName 后缀）
    picked_bases = {p.split(".")[0] for p in picked}
    hits = 0
    for e in expected:
        if e in picked_set or e.split(".")[0] in picked_bases:
            hits += 1
    return hits / len(expected)


def score_one(
    answer: str,
    forms: list[str],
    schema_dir: Path,
    expected_hint: list[str] | None = None,
) -> dict[str, Any]:
    """合并该题涉及的所有 form 的字段池作为 valid_keys。"""
    valid_keys: set[str] = set()
    available_forms: list[str] = []
    missing_forms: list[str] = []
    for fid in forms:
        p = schema_dir / f"{fid}.md"
        if p.exists():
            valid_keys |= extract_schema_keys(p.read_text(encoding="utf-8"))
            available_forms.append(fid)
        else:
            missing_forms.append(fid)

    picked = extract_answer_fields(answer)
    rate = validity_rate(picked, valid_keys)
    hit = hit_rate(picked, expected_hint or [])
    return {
        "picked_fields": picked,
        "picked_count": len(picked),
        "valid_keys_size": len(valid_keys),
        "available_forms": available_forms,
        "missing_forms": missing_forms,
        "validity_rate": round(rate, 3),
        "hit_rate": round(hit, 3) if hit is not None else None,
        "is_refusal": len(picked) == 0,
    }


def load_answers(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out[obj["id"]] = obj.get("answer", "")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m scorer.validity")
    p.add_argument("--answers", type=Path, required=True, help="answers.jsonl")
    p.add_argument("--questions", type=Path, required=True, help="questions/_all.json")
    p.add_argument("--schema-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)

    answers = load_answers(args.answers)
    questions = json.loads(args.questions.read_text(encoding="utf-8"))

    per_question: list[dict[str, Any]] = []
    per_layer_validity: dict[str, list[float]] = {}
    per_layer_hit: dict[str, list[float]] = {}
    refusals_excluded = 0
    for q in questions:
        ans = answers.get(q["id"], "")
        forms = q.get("required_forms", [])
        # 仅对与 schema 相关的题评分；L7 伪问题跳过
        if not forms or q.get("pseudo_question"):
            continue
        result = score_one(ans, forms, args.schema_dir, q.get("required_fields_hint", []))
        result.update({"id": q["id"], "layer": q["layer"]})
        per_question.append(result)
        # Refusal gating: picked=[] 不计入 validity 均值（避免混入拒答信号）
        if result["is_refusal"]:
            refusals_excluded += 1
        else:
            per_layer_validity.setdefault(q["layer"], []).append(result["validity_rate"])
        if result["hit_rate"] is not None:
            per_layer_hit.setdefault(q["layer"], []).append(result["hit_rate"])

    def _summ(per_layer: dict[str, list[float]]) -> dict[str, Any]:
        return {
            layer: {"count": len(rates), "mean": round(mean(rates), 3)}
            for layer, rates in sorted(per_layer.items())
        }

    all_v = [v for rates in per_layer_validity.values() for v in rates]
    all_h = [v for rates in per_layer_hit.values() for v in rates]
    summary = {
        "total_scored": len(per_question),
        "refusals_excluded": refusals_excluded,
        "validity_overall_mean": round(mean(all_v), 3) if all_v else 0.0,
        "hit_overall_mean": round(mean(all_h), 3) if all_h else 0.0,
        "by_layer_validity": _summ(per_layer_validity),
        "by_layer_hit": _summ(per_layer_hit),
    }

    out_data = {"summary": summary, "per_question": per_question}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"评分 {len(per_question)} 题（其中 {refusals_excluded} 题拒答/空，剔除出 validity 均值）")
    print(f"validity 整体均值: {summary['validity_overall_mean']}")
    for layer, stats in summary["by_layer_validity"].items():
        print(f"  V {layer}: {stats['mean']}  (n={stats['count']})")
    print(f"hit_rate 整体均值: {summary['hit_overall_mean']}")
    for layer, stats in summary["by_layer_hit"].items():
        print(f"  H {layer}: {stats['mean']}  (n={stats['count']})")
    print(f"详细结果: {args.out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
