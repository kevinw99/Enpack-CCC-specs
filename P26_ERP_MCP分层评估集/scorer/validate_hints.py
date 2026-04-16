"""核对每题 required_fields_hint 是否真实存在于对应 form 的 schema 中。

用法:
    python -m scorer.validate_hints \
        --questions questions/_all.json \
        --schema-dir 源代码/mcp-kingdee-server/schema

输出每题的 hint 字段在哪个 form 存在 / 哪些缺失，便于 Phase 1C 审核。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .validity import extract_schema_keys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--schema-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args(argv)

    questions = json.loads(args.questions.read_text(encoding="utf-8"))

    # 预加载所有 form 的字段池
    form_keys: dict[str, set[str]] = {}
    for q in questions:
        for fid in q.get("required_forms", []):
            if fid in form_keys:
                continue
            schema_path = args.schema_dir / f"{fid}.md"
            if schema_path.exists():
                form_keys[fid] = extract_schema_keys(schema_path.read_text(encoding="utf-8"))
            else:
                form_keys[fid] = set()

    issues: list[dict[str, Any]] = []
    total_hints = 0
    missing_hints = 0

    for q in questions:
        hints = q.get("required_fields_hint", [])
        forms = q.get("required_forms", [])
        if not hints or not forms:
            continue
        union: set[str] = set()
        for fid in forms:
            union |= form_keys.get(fid, set())
        missing: list[str] = []
        for h in hints:
            base = h.split(".")[0]
            if base not in union and h not in union:
                missing.append(h)
            total_hints += 1
        if missing:
            missing_hints += len(missing)
            issues.append({
                "id": q["id"],
                "layer": q["layer"],
                "forms": forms,
                "missing_hints": missing,
                "suggestion": _nearest_match(missing, union),
            })

    total_qs = len([q for q in questions if q.get("required_fields_hint")])
    print(f"共核对 {total_qs} 题（含 hint）")
    print(f"hint 字段总数: {total_hints}，缺失/拼写错误: {missing_hints}（{missing_hints/total_hints:.1%}）")
    print(f"有问题的题数: {len(issues)}")
    for it in issues:
        print(f"  [{it['id']} {it['layer']}] {it['forms']} — 缺: {it['missing_hints']}")
        for miss, sugg in it["suggestion"].items():
            if sugg:
                print(f"      {miss} → 最接近: {sugg}")

    if args.out:
        args.out.write_text(
            json.dumps({"issues": issues, "total_hints": total_hints,
                        "missing_hints": missing_hints}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"报告: {args.out}")

    return 0


def _nearest_match(missing: list[str], candidates: set[str]) -> dict[str, str | None]:
    """对每个缺失 hint，找字符最相似的候选（Dice 相似度）。"""
    out: dict[str, str | None] = {}
    for m in missing:
        best: tuple[float, str | None] = (0.0, None)
        base = m.split(".")[0]
        for c in candidates:
            s = _similarity(base, c)
            if s > best[0]:
                best = (s, c)
        out[m] = best[1] if best[0] > 0.5 else None
    return out


def _similarity(a: str, b: str) -> float:
    if a == b:
        return 1.0
    bigrams_a = {a[i:i+2] for i in range(len(a) - 1)}
    bigrams_b = {b[i:i+2] for i in range(len(b) - 1)}
    if not bigrams_a or not bigrams_b:
        return 0.0
    inter = bigrams_a & bigrams_b
    return 2 * len(inter) / (len(bigrams_a) + len(bigrams_b))


if __name__ == "__main__":
    sys.exit(main())
