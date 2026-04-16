"""合并 L1-L8 JSON 为 _all.json。

Usage:
    python build_all.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAYERS = [
    "L1_control.json",
    "L2_field_hallucination.json",
    "L3_join_sensitive.json",
    "L4_enum_semantic.json",
    "L5_custom_field.json",
    "L6_business_rule.json",
    "L7_pseudo.json",
    "L8_multi_step.json",
]


def main() -> None:
    merged: list[dict] = []
    per_layer: dict[str, int] = {}
    for f in LAYERS:
        path = HERE / f
        data = json.loads(path.read_text(encoding="utf-8"))
        merged.extend(data)
        layer = data[0]["layer"] if data else f.split("_")[0]
        per_layer[layer] = len(data)

    out = HERE / "_all.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"合并 {len(merged)} 题 -> {out}")
    for layer, count in sorted(per_layer.items()):
        print(f"  {layer}: {count}")


if __name__ == "__main__":
    main()
