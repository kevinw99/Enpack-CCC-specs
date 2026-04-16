"""refusal_correctness 评分器（Phase 2B）。

对 L7 伪问题：答案是否明确识别\"此数据不在 ERP 中\"并引导到正确来源。
先用关键词启发式 + 可选 LLM 二值判断。

用法:
    python -m scorer.refusal \
        --answers results/T1/answers.jsonl \
        --questions questions/_all.json \
        --out results/T1/refusal.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

# 正确拒答的关键措辞
_REFUSAL_PHRASES = [
    "不在 ERP", "不在erp", "不属于 ERP", "非 ERP",
    "ERP 暂无", "ERP 不含", "ERP 无法",
    "金蝶 ERP 没有", "金蝶没有", "未覆盖",
    "建议查", "请查", "应查", "数据缺口",
    "不在金蝶", "另一系统", "其他系统", "独立系统",
    "MES", "CRM", "PLM", "HR", "OA",
]

# 错误尝试回答的反向信号（试图给具体数字/表）
_WRONG_SIGNALS = [
    "根据 ERP 数据", "从金蝶查到",
]


def score_refusal_heuristic(answer: str) -> dict[str, Any]:
    text = answer or ""
    matched = [p for p in _REFUSAL_PHRASES if p in text]
    wrong = [p for p in _WRONG_SIGNALS if p in text]
    is_refusal = bool(matched) and not wrong
    return {
        "is_correct_refusal": is_refusal,
        "matched_phrases": matched,
        "wrong_signals": wrong,
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
    p = argparse.ArgumentParser(prog="python -m scorer.refusal")
    p.add_argument("--answers", type=Path, required=True)
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)

    answers = load_answers(args.answers)
    questions = json.loads(args.questions.read_text(encoding="utf-8"))

    per_question: list[dict[str, Any]] = []
    for q in questions:
        if not q.get("pseudo_question"):
            continue
        ans = answers.get(q["id"], "")
        result = score_refusal_heuristic(ans)
        result.update({"id": q["id"], "layer": q["layer"]})
        per_question.append(result)

    correct = sum(1 for r in per_question if r["is_correct_refusal"])
    n = len(per_question)
    summary = {
        "total": n,
        "correct_refusals": correct,
        "refusal_rate": round(correct / n, 3) if n else 0.0,
    }
    out_data = {"summary": summary, "per_question": per_question}

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out_data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"L7 伪问题 {n} 题，正确拒答 {correct}（{summary['refusal_rate']}）")
    print(f"详细: {args.out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
