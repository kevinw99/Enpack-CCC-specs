"""T0/T1 答案生成（LLM 层模拟）。

方法：对每题调用 DeepSeek，要求返回\"会查询的字段 + 简要答题思路\"。
- T0 模式: 只给 form_id（模拟 P20E 原样，LLM 没有 schema 上下文）
- T1 模式: 给 form_id + P20S schema/{form}.md 内容（模拟 P20E 整合 P20S 后）

输出 answers.jsonl，每行:
    {"id": "...", "answer": "...", "picked_fields": [...]}

用法:
    python -m scorer.runner --mode T0 --questions questions/_all.json \
        --schema-dir 源代码/mcp-kingdee-server/schema --out results/T0/answers.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(Path.home() / "AI" / ".env")

SYSTEM_PROMPT = """你是一个金蝶 ERP 数据分析助手。
给定用户问题和表单上下文，返回你会查询的字段 key 列表和简要答题思路。
输出合法 JSON:
  {"fields": ["FXXX", "FYYY.FName", ...], "plan": "简要答题步骤"}
若问题所需数据不在 ERP 中（伪问题），应 fields=[] 并在 plan 中说明\"数据不在 ERP\"。
不要解释，只返回 JSON。
"""


def _client() -> OpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        raise RuntimeError("缺少 DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def build_context(q: dict[str, Any], schema_dir: Path, include_schema: bool) -> str:
    forms = q.get("required_forms", [])
    ctx = f"相关表单: {', '.join(forms) if forms else '(未指定，请自行判断数据是否在 ERP 中)'}\n"
    if include_schema:
        for fid in forms:
            p = schema_dir / f"{fid}.md"
            if p.exists():
                ctx += f"\n【{fid} Schema (P20S)】\n{p.read_text(encoding='utf-8')}\n"
    return ctx


def ask_one(client: OpenAI, question: str, context: str) -> dict[str, Any]:
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\n问题: {question}"},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        timeout=90,
    )
    raw = resp.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"fields": [], "plan": raw}
    fields = [str(x) for x in data.get("fields", [])]
    plan = str(data.get("plan", ""))
    return {"picked_fields": fields, "plan": plan, "answer": " ".join(fields) + "\n" + plan}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["T0", "T1"], required=True)
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--schema-dir", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--limit", type=int, default=0, help="只跑前 N 题（调试用）")
    args = p.parse_args(argv)

    questions = json.loads(args.questions.read_text(encoding="utf-8"))
    if args.limit:
        questions = questions[: args.limit]

    include_schema = args.mode == "T1"
    client = _client()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            context = build_context(q, args.schema_dir, include_schema)
            try:
                r = ask_one(client, q["question"], context)
            except Exception as e:  # noqa: BLE001
                r = {"picked_fields": [], "plan": f"<err: {e}>", "answer": f"<err: {e}>"}
            rec = {"id": q["id"], "layer": q["layer"], **r}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            f.flush()
            print(f"[{i}/{len(questions)}] {q['id']} ({q['layer']}) — {len(r['picked_fields'])} fields")
    print(f"答案: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
