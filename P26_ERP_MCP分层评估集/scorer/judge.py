"""LLM-as-Judge: factual_correctness + business_grounding 评分器。

两者共用同一 prompt 模板与评分框架；区别在参考依据（schema-based vs wiki-based）。

用法:
    python -m scorer.judge --metric factual \
        --answers results/T1/answers.jsonl \
        --questions questions/_all.json \
        --out results/T1/factual.json

    python -m scorer.judge --metric business \
        --answers results/T1/answers.jsonl \
        --questions questions/_all.json \
        --wiki-dir 源代码/mcp-kingdee-server/wiki \
        --out results/T1/business.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path.home() / "AI" / ".env")


FACTUAL_SYSTEM = """你是 ERP 评估评委。
给定问题、参考答案要点、被测答案，判定答案的事实正确性（是否与 ERP 真实含义一致）。

评分标准（0-5 分）:
- 5: 完全符合参考要点，字段、过滤条件、聚合粒度均正确
- 4: 大部分符合，有 1-2 个小偏差
- 3: 方向对但关键要点缺失或误用
- 2: 多处错误
- 1: 基本错误
- 0: 完全偏题或拒答（若题目应可答）

输出合法 JSON: {"score": 0-5, "reason": "简要评语"}
不要解释，只返回 JSON。
"""

BUSINESS_SYSTEM = """你是 ERP 评估评委，重点评估\"业务判断是否符合公司规则\"。
给定问题、公司业务规则（wiki 摘录）、参考答案要点、被测答案。

评分标准（0-5 分）:
- 5: 业务判断完全符合公司规则（如\"已审核 + 未关闭 = 可发货\"）
- 4: 大致符合，规则细节略有偏差
- 3: 套用通用业务框架，未引用公司私有规则
- 2: 业务判断与公司规则冲突
- 1: 基本错误
- 0: 完全偏题

输出合法 JSON: {"score": 0-5, "reason": "简要评语"}
不要解释，只返回 JSON。
"""


def _client() -> OpenAI:
    key = os.getenv("DEEPSEEK_API_KEY", "")
    if not key:
        raise RuntimeError("缺少 DEEPSEEK_API_KEY")
    return OpenAI(api_key=key, base_url="https://api.deepseek.com")


_LAYER_TOPIC_HINTS = {
    "L4": ["财务", "采购", "销售", "库存"],  # 状态枚举常在业务流程 wiki
    "L6": ["财务", "采购", "销售", "生产", "库存"],  # 业务规则主阵地
    "L7": ["伪问题与数据缺口"],
    "L8": ["财务", "采购", "销售", "生产"],
}


def _load_wiki_context(wiki_dir: Path | None, question: dict[str, Any]) -> str:
    """为 business judge 拼接相关 wiki 内容。

    策略：按层选主题目录 → 抓目录下的 md 文件（限 top-3，每个限 2KB）。
    """
    if not wiki_dir or not wiki_dir.exists():
        return ""
    topics = _LAYER_TOPIC_HINTS.get(question.get("layer", ""), [])
    q_text = question.get("question", "")
    chunks: list[tuple[int, str]] = []  # (relevance, content)
    for topic in topics:
        tdir = wiki_dir / topic
        if not tdir.exists():
            continue
        for p in tdir.rglob("*.md"):
            body = p.read_text(encoding="utf-8")[:2000]
            # 粗糙相关度：问题中的字符在文件名+body 中出现次数
            rel = sum(1 for ch in q_text if ch in p.name) + sum(1 for ch in q_text if ch in body) // 20
            chunks.append((rel, f"### {p.parent.name}/{p.name}\n{body}\n"))
    chunks.sort(key=lambda x: -x[0])
    return "\n".join(c for _, c in chunks[:3])


def _judge(client: OpenAI, system: str, user: str) -> dict[str, Any]:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        timeout=90,
    )
    try:
        data = json.loads(resp.choices[0].message.content or "{}")
    except json.JSONDecodeError:
        return {"score": 0, "reason": "judge JSON 解析失败"}
    score = int(data.get("score", 0))
    return {"score": max(0, min(5, score)), "reason": str(data.get("reason", ""))}


def load_answers(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        out[obj["id"]] = obj.get("answer", "")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--metric", choices=["factual", "business"], required=True)
    p.add_argument("--answers", type=Path, required=True)
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--wiki-dir", type=Path, required=False, default=None)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args(argv)

    answers = load_answers(args.answers)
    questions = json.loads(args.questions.read_text(encoding="utf-8"))
    if args.limit:
        questions = questions[: args.limit]

    client = _client()
    system = FACTUAL_SYSTEM if args.metric == "factual" else BUSINESS_SYSTEM

    per_question: list[dict[str, Any]] = []
    per_layer: dict[str, list[int]] = {}
    for q in questions:
        dims = q.get("scoring_dimensions", [])
        target = "factual_correctness" if args.metric == "factual" else "business_grounding"
        if target not in dims:
            continue
        ans = answers.get(q["id"], "")
        if not ans.strip():
            continue

        ref_points = q.get("reference_answer_points", [])
        wiki_ctx = _load_wiki_context(args.wiki_dir, q) if args.metric == "business" else ""

        user = f"问题: {q['question']}\n\n参考答案要点:\n" + "\n".join(f"- {pt}" for pt in ref_points)
        if wiki_ctx:
            user += f"\n\n公司业务规则（wiki）:\n{wiki_ctx}"
        user += f"\n\n被测答案:\n{ans}"

        try:
            r = _judge(client, system, user)
        except Exception as e:  # noqa: BLE001
            r = {"score": 0, "reason": f"<err: {e}>"}

        per_question.append({"id": q["id"], "layer": q["layer"], **r})
        per_layer.setdefault(q["layer"], []).append(r["score"])
        print(f"[{q['id']} {q['layer']}] {r['score']}/5 — {r['reason'][:60]}")

    summary = {
        "total": len(per_question),
        "overall_mean": round(mean([r["score"] for r in per_question]), 3) if per_question else 0.0,
        "by_layer": {
            layer: {"count": len(s), "mean": round(mean(s), 3)}
            for layer, s in sorted(per_layer.items())
        },
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"summary": summary, "per_question": per_question}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n{args.metric}: 整体均分 {summary['overall_mean']}/5")
    for layer, s in summary["by_layer"].items():
        print(f"  {layer}: {s['mean']}/5  (n={s['count']})")
    print(f"详细: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
