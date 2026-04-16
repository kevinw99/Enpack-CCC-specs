"""P26 Real MCP-level runner (Phase 4 real T1 / Phase 5 T2).

与 scorer/runner.py 的区别：
    runner.py     = LLM-level 模拟（把 schema 文本直接拼进 prompt，不走工具）
    mcp_runner.py = 真实 MCP 工具链（spawn src.server stdio、list_tools、
                    让 LLM 自主决定调用，依赖 P20E 整合的 docstring 质量）

三段评估通过工具白名单实现：
    --stage T0   仅 query_* + describe_form（P20S/P20T 未上线的基线）
    --stage T1   + kingdee_get_schema / _relations / _list_cached_schemas（P20S 上线）
    --stage T2   + kingdee_get_wiki                                       （P20T 上线）

输出 answers.jsonl 兼容现有 scorer/validity.py：
    {"id", "layer", "picked_fields", "plan", "answer",
     "tool_calls": [{"name", "args", "result_preview"}, ...]}

用法示例：
    python -m scorer.mcp_runner --stage T2 \\
        --questions questions/_all.json \\
        --out results/T2_mcp/answers.jsonl \\
        --server-cmd ".venv/bin/python -m src.server" \\
        --server-cwd /Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server \\
        --limit 3     # 烟测先跑 3 题
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(Path.home() / "AI" / ".env")


# ── 工具白名单（按 stage 过滤）────────────────────────────────────────

# 旧态 T0：P20S/P20T 未上线的 P20E 工具
TOOLS_T0 = {
    "kingdee_query_bills",
    "kingdee_query_materials",
    "kingdee_query_inventory",
    "kingdee_query_fixed_assets",
    "kingdee_describe_form",
    "kingdee_search_forms_online",
}
# T1 增加 P20S schema 三件套
TOOLS_T1 = TOOLS_T0 | {
    "kingdee_get_schema",
    "kingdee_get_relations",
    "kingdee_list_cached_schemas",
}
# T2 增加 P20T wiki
TOOLS_T2 = TOOLS_T1 | {"kingdee_get_wiki"}

STAGE_TOOLS = {"T0": TOOLS_T0, "T1": TOOLS_T1, "T2": TOOLS_T2}


# ── Prompt ────────────────────────────────────────────────────────

_SYSTEM_BASE = """你是金蝶 ERP 数据分析助手。用户会提出业务问题，你通过调用工具拿到字段定义/业务约定/实际数据后给出回答。

工具使用纪律（违反会导致答不完）：
- **幂等性**：同一个 form_id 只调一次 kingdee_get_schema；已经调过的 form_id 不要再调。已经调过 kingdee_list_cached_schemas 不要再调。
- **不探索不存在的工具**：白名单外的工具不要尝试；kingdee_search_forms_online 不要连续调超过 1 次。
- **优先行动**：拿到 schema/wiki 信息后**立刻进入 query_bills / query_materials 等数据动作**，不要继续"再确认一下字段"。
- **Turn 预算**：最多 12 轮工具调用。到第 9 轮仍未查到数据要立即收尾输出 JSON；不要在 schema 探索上超过 4 轮。

判断"伪问题"的双向约束（既防逃避也防硬答）：

A. 下列类型是**典型伪问题，必须直接拒答**，不要尝试 query（ERP 本来就不管这些）：
   - 员工个人非工作信息：生日、婚姻、健康、家庭、兴趣
   - 客户非交易类信息：投诉、满意度、NPS、评价、回访记录
   - 市场情报：竞争对手信息、市场占有率、行业趋势、舆情
   - 生产车间实时感应数据：温度、湿度、电流、振动、OEE 实时
   - 物流中转详情：通关、报关、集装箱追踪、船期
   - 工艺细节：配方参数、工艺流程图、SOP 细节
   - 任何涉及"为什么""怎么想的""动机/意图"的主观问题
"""

_SYSTEM_QUERY_CONSTRAINT = """
B. 涉及采购/销售/库存/生产/财务/固定资产**客观交易数据**的分析题（即使多步、跨表、需要计算），**必须**至少执行一次 query_bills/query_materials/query_inventory；不允许仅因 schema 未缓存就放弃。

C. 如果 schema 不在 cache，降级方案是：直接 query_bills 传最常见字段（FID, FBillNo, FDate, FDocumentStatus 等），而不是放弃

查询建议：
- 业务约定（尤其公司私有规则）在 kingdee_get_wiki 里，不在 schema 里
- 跨表查询先用 kingdee_get_relations 确认关联路径
"""

_SYSTEM_TAIL = """
最终回答必须是合法 JSON：
  {"fields": ["FXXX", "FYYY.FName", ...], "plan": "解答思路 + 关键结论"}
fields 列你答题会引用的字段；只有真正的伪问题才允许 fields=[]。
"""

# Tool call quotas (code-level enforcement)
TOOL_QUOTAS = {"kingdee_search_forms_online": 2}


def build_system_prompt(stage: str) -> str:
    """Build stage-specific system prompt. T0 omits B/C query constraints."""
    parts = [_SYSTEM_BASE]
    if stage in ("T1", "T2"):
        parts.append(_SYSTEM_QUERY_CONSTRAINT)
    parts.append(_SYSTEM_TAIL)
    return "".join(parts)


# ── MCP tool → OpenAI function schema 转换 ────────────────────────

def mcp_tool_to_openai(tool: Any) -> dict:
    """Translate an mcp.types.Tool to OpenAI function-calling schema."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.inputSchema or {"type": "object", "properties": {}},
        },
    }


# ── picked_fields 抽取 ────────────────────────────────────────────

_FIELD_RE = re.compile(r"\bF(?:_BDK_)?[A-Za-z][A-Za-z0-9_]*")


def _extract_from_text(text: str) -> list[str]:
    seen, out = set(), []
    for m in _FIELD_RE.findall(text or ""):
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def _extract_from_tool_args(tool_calls: list[dict]) -> list[str]:
    """Extract field keys from FieldKeys arg of any kingdee_query_bills call."""
    out = []
    for tc in tool_calls:
        name = tc.get("name", "")
        args = tc.get("args", {}) or {}
        # bills 直接有 field_keys；query_materials/inventory 可能有
        for key in ("field_keys", "FieldKeys"):
            if key in args and isinstance(args[key], str):
                out.extend([f.strip() for f in args[key].split(",") if f.strip()])
        # nested params={} dict
        nested = args.get("params") if isinstance(args.get("params"), dict) else None
        if nested:
            for key in ("field_keys", "FieldKeys"):
                if key in nested and isinstance(nested[key], str):
                    out.extend([f.strip() for f in nested[key].split(",") if f.strip()])
    # dedupe preserving order
    seen, dedup = set(), []
    for f in out:
        if f not in seen:
            seen.add(f)
            dedup.append(f)
    return dedup


# ── 单题执行：tool-use loop ────────────────────────────────────────

MAX_TURNS = 12


async def answer_one(
    session: ClientSession,
    client: OpenAI,
    question: dict,
    openai_tools: list[dict],
    model: str,
    stage: str = "T1",
) -> dict:
    messages: list[dict] = [
        {"role": "system", "content": build_system_prompt(stage)},
        {"role": "user", "content": f"问题: {question['question']}\n"
                                     f"提示相关表单: {', '.join(question.get('required_forms', [])) or '（未指定，自行判断）'}"},
    ]
    tool_calls_log: list[dict] = []
    tool_call_counts: dict[str, int] = {}   # code-level quota tracking

    for turn in range(MAX_TURNS):
        # Sync OpenAI call (DeepSeek API)
        resp = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=messages,
            tools=openai_tools,
            tool_choice="auto",
            temperature=0.0,
            timeout=120,
        )
        msg = resp.choices[0].message
        finish = resp.choices[0].finish_reason

        if msg.tool_calls:
            messages.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in msg.tool_calls
                ],
            })
            for tc in msg.tool_calls:
                tname = tc.function.name
                try:
                    targs = json.loads(tc.function.arguments or "{}")
                except json.JSONDecodeError:
                    targs = {}
                # Code-level tool quota enforcement
                tool_call_counts[tname] = tool_call_counts.get(tname, 0) + 1
                quota = TOOL_QUOTAS.get(tname)
                if quota is not None and tool_call_counts[tname] > quota:
                    result_text = (f"<quota exceeded: {tname} 已调用 {quota} 次，"
                                   f"不允许再调。请直接使用已有信息继续。>")
                else:
                    try:
                        result = await session.call_tool(tname, targs)
                        # extract text content
                        parts = []
                        for block in (result.content or []):
                            text = getattr(block, "text", None)
                            if text:
                                parts.append(text)
                        result_text = "\n".join(parts) or "(no content)"
                    except Exception as e:  # noqa: BLE001
                        result_text = f"<tool error: {e}>"
                # cap result size in conversation to avoid blowing context
                capped = result_text[:8000] + ("\n...[truncated]" if len(result_text) > 8000 else "")
                tool_calls_log.append({
                    "name": tname, "args": targs,
                    "result_preview": result_text[:400],
                    "result_size": len(result_text),
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": capped,
                })
            continue  # another turn

        # No more tool calls → finalize
        final_text = msg.content or ""
        # Try to parse JSON; if model forgot, treat full content as plan
        fields, plan = [], final_text
        try:
            # Find first JSON object in content
            m = re.search(r"\{[\s\S]*\}", final_text)
            if m:
                data = json.loads(m.group(0))
                fields = [str(x) for x in data.get("fields", [])]
                plan = str(data.get("plan", final_text))
        except json.JSONDecodeError:
            pass

        # Merge picked_fields: model's + tool arg extraction + regex on plan
        merged = list(dict.fromkeys(
            fields
            + _extract_from_tool_args(tool_calls_log)
            + _extract_from_text(plan)
        ))
        return {
            "id": question["id"],
            "layer": question["layer"],
            "picked_fields": merged,
            "plan": plan,
            "answer": " ".join(merged) + "\n" + plan,
            "tool_calls": tool_calls_log,
            "turns_used": turn + 1,
            "finish_reason": finish,
        }

    # Hit MAX_TURNS without a final text → force a no-tools summary call
    messages.append({
        "role": "user",
        "content": "已达到工具调用上限。请立即基于已掌握信息输出最终 JSON "
                   "{\"fields\": [...], \"plan\": \"...\"}；不要再调用任何工具。",
    })
    try:
        resp = await asyncio.to_thread(
            client.chat.completions.create,
            model=model, messages=messages,
            tool_choice="none", temperature=0.0, timeout=120,
        )
        final_text = resp.choices[0].message.content or ""
    except Exception as e:  # noqa: BLE001
        final_text = f"<forced-summary error: {e}>"

    fields, plan = [], final_text
    try:
        m = re.search(r"\{[\s\S]*\}", final_text)
        if m:
            data = json.loads(m.group(0))
            fields = [str(x) for x in data.get("fields", [])]
            plan = str(data.get("plan", final_text))
    except json.JSONDecodeError:
        pass
    merged = list(dict.fromkeys(
        fields + _extract_from_tool_args(tool_calls_log) + _extract_from_text(plan)
    ))
    return {
        "id": question["id"],
        "layer": question["layer"],
        "picked_fields": merged,
        "plan": plan,
        "answer": " ".join(merged) + "\n" + plan,
        "tool_calls": tool_calls_log,
        "turns_used": MAX_TURNS,
        "finish_reason": "max_turns_forced_summary",
    }


# ── Main ──────────────────────────────────────────────────────────

async def run(args: argparse.Namespace) -> int:
    questions = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    if args.limit:
        questions = questions[: args.limit]

    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        print("缺少 DEEPSEEK_API_KEY（检查 ~/AI/.env）", file=sys.stderr)
        return 2
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # Spawn MCP server as stdio subprocess
    server_parts = args.server_cmd.split()
    server_params = StdioServerParameters(
        command=server_parts[0],
        args=server_parts[1:],
        cwd=args.server_cwd,
        env=os.environ.copy(),
    )

    allowed = STAGE_TOOLS[args.stage]
    args.out.parent.mkdir(parents=True, exist_ok=True)

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_resp = await session.list_tools()
            all_tools = tools_resp.tools
            filtered = [t for t in all_tools if t.name in allowed]
            print(f"[stage={args.stage}] MCP server 暴露 {len(all_tools)} 个工具；"
                  f"本阶段启用 {len(filtered)} 个：")
            for t in filtered:
                print(f"  - {t.name}")
            openai_tools = [mcp_tool_to_openai(t) for t in filtered]

            with args.out.open("w", encoding="utf-8") as f:
                for i, q in enumerate(questions, 1):
                    try:
                        rec = await answer_one(session, client, q, openai_tools, args.model, stage=args.stage)
                    except Exception as e:  # noqa: BLE001
                        rec = {"id": q["id"], "layer": q["layer"],
                               "picked_fields": [], "plan": f"<err: {e}>",
                               "answer": f"<err: {e}>", "tool_calls": [],
                               "turns_used": 0, "finish_reason": "error"}
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    f.flush()
                    tool_names = [tc["name"] for tc in rec.get("tool_calls", [])]
                    print(f"[{i}/{len(questions)}] {rec['id']} ({rec['layer']}) — "
                          f"{len(rec.get('picked_fields', []))} fields / "
                          f"{len(tool_names)} tool calls: {tool_names}")

    print(f"答案: {args.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--stage", choices=["T0", "T1", "T2"], required=True)
    p.add_argument("--questions", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--server-cmd", type=str,
                   default=".venv/bin/python -m src.server")
    p.add_argument("--server-cwd", type=str,
                   default=str(Path.home() / "AI" / "Enpack_CCC" / "源代码" / "mcp-kingdee-server"))
    p.add_argument("--model", type=str, default="deepseek-chat")
    p.add_argument("--limit", type=int, default=0)
    args = p.parse_args(argv)
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
