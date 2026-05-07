"""P28 模型MCP对比评估 — DeepSeek vs Claude Opus

对比两种模型在同时使用 KB MCP + ERP MCP 时的效果差异。
两种模型使用相同的工具集和数据源，隔离模型能力差异。

Usage:
    python compare.py                    # 运行全部问题
    python compare.py --limit 2          # 只跑前 2 题（快速测试）
    python compare.py --provider deepseek  # 只跑 DeepSeek
    python compare.py --provider claude    # 只跑 Claude
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from datetime import datetime
from pathlib import Path

# ── Path setup ──────────────────────────────────────────
_script_dir = Path(__file__).resolve().parent
_project_root = _script_dir.parents[1]
_src_root = _project_root / "源代码"
_kb_root = _src_root / "mcp-kb-server"
_kingdee_root = _src_root / "mcp-kingdee-server"

sys.path.insert(0, str(_script_dir))
sys.path.insert(0, str(_src_root / "rd_ai_tools"))

import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from dotenv import load_dotenv
load_dotenv(_kingdee_root / ".env")
load_dotenv(Path.home() / "AI" / ".env")

# Fix: Claude Code sets empty ANTHROPIC_AUTH_TOKEN and ANTHROPIC_BASE_URL
# which break the Anthropic SDK when creating a client
for _env_key in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL"):
    if not os.environ.get(_env_key):
        os.environ.pop(_env_key, None)

from questions import TestQuestion, QUESTIONS
from common.llm_client import (
    call_llm, create_deepseek_client, create_anthropic_client, extract_json,
)

# KB tool imports — load from mcp-kb-server/src/
sys.path.insert(0, str(_kb_root))
from src.tools.search import search_knowledge_base  # noqa: E402
from src.tools.company import get_company_profile  # noqa: E402
from src.tools.products import lookup_product  # noqa: E402
from src.tools.competitors import lookup_competitor  # noqa: E402
from src.tools.industry import get_industry_context  # noqa: E402
from src.store.vector_db import VectorDB  # noqa: E402

# Clear cached `src` package so ERP's src/ can be imported next
_src_modules = [k for k in sys.modules if k == "src" or k.startswith("src.")]
for _k in _src_modules:
    del sys.modules[_k]
sys.path.remove(str(_kb_root))

# ERP tool imports — load from mcp-kingdee-server/src/
sys.path.insert(0, str(_kingdee_root))
from src.kingdee_client import _post, _query_payload, _rows  # noqa: E402
from src.futures.client import get_futures_spot, analyze_futures_trend  # noqa: E402

# ── Config ──────────────────────────────────────────
CLAUDE_MODEL = "claude-opus-4-20250514"

MODEL_IDS = {
    "ds-flash": "deepseek-v4-flash",
    "ds-pro": "deepseek-v4-pro",
    "ds-hybrid": {"router": "deepseek-v4-flash", "answerer": "deepseek-v4-pro"},
    "claude": CLAUDE_MODEL,
}

# Pricing per 1M tokens (USD, list price)
PRICING = {
    "ds-flash": {"input": 0.14, "output": 0.28},
    "ds-pro": {"input": 0.435, "output": 0.87},
    "ds-hybrid": {"input": 0.14, "output": 0.87},  # flash input + pro output (approximation)
    "claude": {"input": 10.0, "output": 30.0},
}

def _is_deepseek(provider: str) -> bool:
    return provider.startswith("ds-")

OUTPUT_DIR = _script_dir / "results"
OUTPUT_DIR.mkdir(exist_ok=True)

# ── Router Prompt (covers KB + ERP tools) ──────────────────
ROUTER_SYSTEM = """\
你是一个数据查询规划器。给定一个业务问题，你需要决定调用哪些工具来获取相关数据。
你可以同时使用知识库(KB)和ERP两类工具。

可用工具：

【知识库工具 (KB)】
1. kb_search(query, category) - 语义搜索知识库。category可选: company/operations/tech/analysis/industry/research/all
2. kb_company_profile(aspect) - 公司档案。aspect: overview/history/org_structure/financials/key_personnel/mission
3. kb_product(product_name) - 产品信息查询
4. kb_competitor(company_name) - 竞品信息查询
5. kb_industry(topic) - 行业背景信息

【ERP工具】
6. erp_schema(form_id) - 获取表单字段结构（查询前先确认字段）
7. erp_relations() - 获取跨表JOIN路径
8. erp_wiki(topic) - 获取业务规则/公司私有约定（topic为空返回目录）
9. erp_materials(keyword) - 搜索物料档案
10. erp_inventory(material_number) - 查即时库存（需先查物料编码）
11. erp_bills(form_id, field_keys, filter_string, limit) - 查询任意金蝶单据
    常用form_id: PUR_PurchaseOrder(采购订单), SAL_SaleOrder(销售订单), STK_Inventory(库存)
12. erp_fixed_assets(department, asset_name) - 查固定资产
13. erp_futures_spot(keyword) - 期货实时价格（铜/铝等）
14. erp_futures_analysis(keyword, days) - 期货走势分析

规则：
- 规划3-6个工具调用步骤，宁多勿少——多一个查询的成本极低，但漏掉关键数据会严重影响回答质量
- 对于KB问题，至少用2-3个不同工具交叉检索（如 kb_search + kb_product + kb_company_profile），确保数据完整
- 对于ERP问题，先查物料/schema再查具体数据（如 erp_materials → erp_inventory）
- 对于混合问题，KB和ERP工具都要用，从多角度获取数据
- 如果步骤之间有依赖（如先查物料编码再查库存），用 step_ref 标注

输出格式（纯JSON，不要其他文字）：
```json
{"steps": [
  {"tool": "kb_search", "params": {"query": "...", "category": "all"}, "reason": "..."},
  {"tool": "erp_materials", "params": {"keyword": "铜箔"}, "reason": "..."}
]}
```"""

ANSWER_SYSTEM = """\
你是 Enpack（英联股份/英年科技）的内部AI助手，可以同时访问公司知识库和ERP系统。
下面提供了从公司知识库和ERP系统中获取的数据。

回答策略：
1. 优先使用提供的数据回答，引用数据来源（"根据知识库"、"根据ERP数据"等）。
2. 如果数据只覆盖部分问题，先回答覆盖的部分，再用专业知识补充，明确区分来源。
3. 给出具体、可操作的回答。
用中文回答。"""


# ── Tool Executors ──────────────────────────────────────────

async def execute_kb_tool(tool: str, params: dict, db: VectorDB) -> dict:
    """Execute a KB tool and return results."""
    try:
        if tool == "kb_search":
            results = search_knowledge_base(
                params.get("query", ""),
                category=params.get("category", "all"),
                max_results=5,
                db=db,
            )
            return {"tool": tool, "params": params, "data": results}

        elif tool == "kb_company_profile":
            data = get_company_profile(aspect=params.get("aspect", "overview"), db=db)
            return {"tool": tool, "params": params, "data": data}

        elif tool == "kb_product":
            data = lookup_product(product_name=params.get("product_name", ""), db=db)
            return {"tool": tool, "params": params, "data": data}

        elif tool == "kb_competitor":
            data = lookup_competitor(company_name=params.get("company_name", ""), db=db)
            return {"tool": tool, "params": params, "data": data}

        elif tool == "kb_industry":
            data = get_industry_context(topic=params.get("topic", ""), db=db)
            return {"tool": tool, "params": params, "data": data}

        return {"tool": tool, "params": params, "data": None, "error": f"未知KB工具: {tool}"}
    except Exception as e:
        return {"tool": tool, "params": params, "data": None, "error": str(e)}


async def execute_erp_tool(tool: str, params: dict, prev_results: list[dict]) -> dict:
    """Execute an ERP tool and return results."""
    params = _resolve_refs(params, prev_results)
    try:
        if tool == "erp_schema":
            form_id = params.get("form_id", "")
            schema_path = _kingdee_root / "schema" / f"{form_id}.md"
            if schema_path.exists():
                content = schema_path.read_text(encoding="utf-8")
                if len(content) > 4000:
                    content = content[:4000] + "\n... (截断)"
                return {"tool": tool, "params": params,
                        "data": {"form_id": form_id, "schema_md": content}}
            return {"tool": tool, "params": params, "data": None,
                    "error": f"schema not found: {form_id}"}

        elif tool == "erp_relations":
            p = _kingdee_root / "schema" / "relations.md"
            if p.exists():
                return {"tool": tool, "params": params,
                        "data": {"relations_md": p.read_text(encoding="utf-8")[:3000]}}
            return {"tool": tool, "params": params, "data": None, "error": "relations.md missing"}

        elif tool == "erp_wiki":
            topic = params.get("topic", "")
            wiki_dir = _kingdee_root / "wiki"
            if not wiki_dir.exists():
                return {"tool": tool, "params": params, "data": None, "error": "wiki dir missing"}
            if not topic:
                topics = sorted(str(p.relative_to(wiki_dir)) for p in wiki_dir.rglob("*.md"))
                return {"tool": tool, "params": params, "data": {"index": topics}}
            target = wiki_dir / f"{topic}.md"
            if not target.exists():
                leaf = topic.split("/")[-1]
                matches = list(wiki_dir.rglob(f"*{leaf}*.md"))
                if matches:
                    target = matches[0]
            if target.exists():
                return {"tool": tool, "params": params,
                        "data": {"topic": topic, "content": target.read_text(encoding="utf-8")[:4000]}}
            return {"tool": tool, "params": params, "data": None, "error": f"topic not found: {topic}"}

        elif tool == "erp_materials":
            keyword = params.get("keyword", "")
            result = await _post("query", _query_payload(
                "BD_Material",
                "FMaterialId,FNumber,FName,FSpecification,FBaseUnitId.FName,FMaterialGroup.FName",
                f"FForbidStatus='A' and (FName like '%{keyword}%' or FNumber like '%{keyword}%')",
                "FNumber ASC", 0, 20,
            ))
            rows = _rows(result)
            return {"tool": tool, "params": params, "data": {"count": len(rows), "rows": rows}}

        elif tool == "erp_inventory":
            mat_num = params.get("material_number", "")
            if not mat_num:
                return {"tool": tool, "params": params, "data": None, "error": "无物料编码"}
            result = await _post("query", _query_payload(
                "STK_Inventory",
                "FMaterialId.FNumber,FMaterialId.FName,FStockId.FName,FBaseQty,FBaseUnitId.FName",
                f"FBaseQty>0 and FMaterialId.FNumber='{mat_num}'",
                "FMaterialId.FNumber ASC", 0, 50,
            ))
            rows = _rows(result)
            return {"tool": tool, "params": params, "data": {"count": len(rows), "rows": rows}}

        elif tool == "erp_bills":
            form_id = params.get("form_id", "")
            field_keys = params.get("field_keys", "FID,FBillNo,FDate,FDocumentStatus")
            filter_string = params.get("filter_string", "")
            limit = params.get("limit", 20)
            result = await _post("query", _query_payload(
                form_id, field_keys, filter_string, "FID DESC", 0, limit,
            ))
            rows = _rows(result)
            return {"tool": tool, "params": params,
                    "data": {"form_id": form_id, "count": len(rows), "rows": rows[:20]}}

        elif tool == "erp_fixed_assets":
            dept = params.get("department", "")
            name = params.get("asset_name", "")
            parts = []
            if dept:
                parts.append(f"FDeptId.FName like '%{dept}%'")
            if name:
                parts.append(f"FAssetName like '%{name}%'")
            filter_str = " and ".join(parts) if parts else ""
            result = await _post("query", _query_payload(
                "FA_CARD",
                "FAssetNumber,FAssetName,FDeptId.FName,FStatus,FOriginalValue,FQty",
                filter_str, "FAssetNumber ASC", 0, 50,
            ))
            rows = _rows(result)
            return {"tool": tool, "params": params, "data": {"count": len(rows), "rows": rows}}

        elif tool == "erp_futures_spot":
            keyword = params.get("keyword", "铜")
            data = await get_futures_spot(keyword)
            return {"tool": tool, "params": params,
                    "data": json.loads(data) if isinstance(data, str) else data}

        elif tool == "erp_futures_analysis":
            keyword = params.get("keyword", "铜")
            days = params.get("days", 30)
            data = await analyze_futures_trend(keyword, days)
            return {"tool": tool, "params": params,
                    "data": json.loads(data) if isinstance(data, str) else data}

        return {"tool": tool, "params": params, "data": None, "error": f"未知ERP工具: {tool}"}
    except Exception as e:
        return {"tool": tool, "params": params, "data": None, "error": str(e)}


def _resolve_refs(params: dict, prev_results: list[dict]) -> dict:
    """Replace STEP_N_RESULT references with actual data from previous steps."""
    resolved = {}
    for k, v in params.items():
        if isinstance(v, str) and "STEP_" in v and "_RESULT" in v:
            try:
                step_idx = int(v.split("STEP_")[1].split("_")[0]) - 1
                if 0 <= step_idx < len(prev_results):
                    prev = prev_results[step_idx]
                    data = prev.get("data", {})
                    if prev.get("tool") == "erp_materials" and data:
                        rows = data.get("rows", [])
                        if rows and len(rows[0]) >= 2:
                            v = rows[0][1]
                        else:
                            v = ""
                    else:
                        v = json.dumps(data, ensure_ascii=False)[:500]
            except (ValueError, IndexError):
                pass
        resolved[k] = v
    return resolved


# ── Core Pipeline ──────────────────────────────────────────

async def plan_tools(question: str, client, provider: str) -> tuple[list[dict], dict]:
    """Use LLM to plan which tools to call. Returns (steps, token_info)."""
    model_cfg = MODEL_IDS.get(provider)
    if isinstance(model_cfg, dict):
        model = model_cfg["router"]
    else:
        model = model_cfg
    is_ds = _is_deepseek(provider)
    router_max_tokens = 4096 if is_ds else 1024
    kwargs = dict(
        system=ROUTER_SYSTEM,
        client=client,
        provider="deepseek" if is_ds else "anthropic",
        model=model,
        max_tokens=router_max_tokens,
        temperature=0.1,
    )
    if is_ds:
        kwargs["response_format"] = {"type": "json_object"}
    resp = await call_llm(f"业务问题: {question}", **kwargs)
    try:
        plan = extract_json(resp.text)
        steps = plan.get("steps", [])
    except (ValueError, KeyError):
        steps = []
    return steps, {"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens}


async def execute_tools(steps: list[dict], db: VectorDB) -> list[dict]:
    """Execute planned tool calls sequentially."""
    results = []
    for step in steps:
        tool = step.get("tool", "skip")
        params = step.get("params", {})
        if tool == "skip":
            results.append({"tool": "skip", "reason": step.get("reason", "")})
        elif tool.startswith("kb_"):
            result = await execute_kb_tool(tool, params, db)
            results.append(result)
        elif tool.startswith("erp_"):
            result = await execute_erp_tool(tool, params, results)
            results.append(result)
        else:
            results.append({"tool": tool, "params": params, "data": None, "error": f"未知工具: {tool}"})
    return results


def build_answer_prompt(question: str, tool_results: list[dict]) -> str:
    """Build prompt with tool results as context."""
    context_parts = []
    for i, r in enumerate(tool_results, 1):
        tool = r.get("tool", "unknown")
        if tool == "skip":
            continue
        data = r.get("data")
        error = r.get("error")
        reason = r.get("reason", "")
        source = "知识库" if tool.startswith("kb_") else "ERP系统"

        if error:
            context_parts.append(f"【{source} 查询 {i}】{reason}\n工具: {tool}\n结果: 查询失败 - {error}")
        elif data:
            data_str = json.dumps(data, ensure_ascii=False, indent=2)
            if len(data_str) > 3000:
                data_str = data_str[:3000] + "\n... (截断)"
            context_parts.append(f"【{source} 查询 {i}】{reason}\n工具: {tool}\n数据:\n{data_str}")

    if not context_parts:
        context = "（未查询到相关数据）"
    else:
        context = "\n\n---\n\n".join(context_parts)

    return f"以下是从公司系统中获取的数据:\n\n{context}\n\n---\n\n问题: {question}"


async def run_one_provider(
    question: TestQuestion,
    provider: str,
    client,
    db: VectorDB,
) -> dict:
    """Run one question with one provider, return results."""
    # Step 1: Route
    t0 = time.time()
    steps, router_tokens = await plan_tools(question.question, client, provider)
    route_time = time.time() - t0

    # Step 2: Execute tools
    t1 = time.time()
    tool_results = await execute_tools(steps, db)
    exec_time = time.time() - t1
    data_count = sum(1 for r in tool_results if r.get("data"))

    # Step 3: Answer
    prompt = build_answer_prompt(question.question, tool_results)
    model_cfg = MODEL_IDS.get(provider)
    if isinstance(model_cfg, dict):
        answer_model = model_cfg["answerer"]
    else:
        answer_model = model_cfg
    is_ds = _is_deepseek(provider)
    t2 = time.time()
    resp = await call_llm(
        prompt,
        system=ANSWER_SYSTEM,
        client=client,
        provider="deepseek" if is_ds else "anthropic",
        model=answer_model,
        max_tokens=2048,
        temperature=0.3,
    )
    answer_time = time.time() - t2

    total_input = router_tokens["input_tokens"] + resp.input_tokens
    total_output = router_tokens["output_tokens"] + resp.output_tokens
    pricing = PRICING[provider]
    cost = (total_input * pricing["input"] + total_output * pricing["output"]) / 1_000_000

    return {
        "tools_planned": [s.get("tool") for s in steps],
        "tools_data_count": data_count,
        "tool_details": _summarize_tools(tool_results),
        "answer": resp.text,
        "router_tokens": router_tokens,
        "answer_tokens": {"input_tokens": resp.input_tokens, "output_tokens": resp.output_tokens},
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "route_time_s": round(route_time, 2),
        "exec_time_s": round(exec_time, 2),
        "answer_time_s": round(answer_time, 2),
        "total_time_s": round(route_time + exec_time + answer_time, 2),
        "cost_usd": round(cost, 6),
    }


def _summarize_tools(tool_results: list[dict]) -> list[dict]:
    """Summarize tool results (strip large data for readability)."""
    summaries = []
    for r in tool_results:
        s = {"tool": r.get("tool"), "reason": r.get("reason", "")}
        if r.get("error"):
            s["status"] = "error"
            s["error"] = r["error"]
        elif r.get("data"):
            s["status"] = "ok"
            data = r["data"]
            if isinstance(data, dict) and "count" in data:
                s["row_count"] = data["count"]
            elif isinstance(data, list):
                s["result_count"] = len(data)
        else:
            s["status"] = "no_data"
        summaries.append(s)
    return summaries


# ── Main Harness ──────────────────────────────────────────

async def run_comparison(
    providers: list[str] | None = None,
    limit: int = 0,
    output_name: str = "comparison.json",
):
    """Run all questions through both providers and produce comparison."""
    if providers is None:
        providers = ["ds-flash", "claude"]

    questions = QUESTIONS[:limit] if limit > 0 else QUESTIONS

    print(f"P28 模型MCP对比评估")
    print(f"{'=' * 60}")
    print(f"Questions: {len(questions)}")
    print(f"Providers: {', '.join(providers)}")
    for p in providers:
        m = MODEL_IDS.get(p)
        if isinstance(m, dict):
            print(f"  {p}: router={m['router']}, answerer={m['answerer']}")
        else:
            print(f"  {p}: {m}")
    print()

    # Init clients
    clients = {}
    for p in providers:
        if _is_deepseek(p) and not any(_is_deepseek(k) for k in clients):
            clients[p] = create_deepseek_client()
        elif _is_deepseek(p):
            clients[p] = list(v for k, v in clients.items() if _is_deepseek(k))[0]
        elif p == "claude":
            clients["claude"] = create_anthropic_client()

    db = VectorDB()

    results = []
    totals = {p: {"input": 0, "output": 0, "cost": 0, "time": 0} for p in providers}

    for i, q in enumerate(questions):
        print(f"[{i+1}/{len(questions)}] {q.id} ({q.category}) {q.question[:40]}...")
        entry = {
            "id": q.id,
            "question": q.question,
            "category": q.category,
            "description": q.description,
        }

        for provider in providers:
            print(f"  → {provider}...", end="", flush=True)
            try:
                result = await run_one_provider(q, provider, clients[provider], db)
                entry[provider] = result
                totals[provider]["input"] += result["total_input_tokens"]
                totals[provider]["output"] += result["total_output_tokens"]
                totals[provider]["cost"] += result["cost_usd"]
                totals[provider]["time"] += result["total_time_s"]
                tools_str = ",".join(result["tools_planned"])
                print(f" {result['total_time_s']}s, tools=[{tools_str}], ${result['cost_usd']:.4f}")
            except Exception as e:
                print(f" ERROR: {e}")
                entry[provider] = {"error": str(e)}

        results.append(entry)

    db.close()

    # Build output
    output = {
        "meta": {
            "timestamp": datetime.now().isoformat(),
            "questions_count": len(questions),
            "providers": providers,
            "models": {p: MODEL_IDS[p] for p in providers},
        },
        "results": results,
        "summary": {},
    }

    for p in providers:
        t = totals[p]
        output["summary"][p] = {
            "total_input_tokens": t["input"],
            "total_output_tokens": t["output"],
            "total_cost_usd": round(t["cost"], 4),
            "total_time_s": round(t["time"], 1),
            "avg_time_s": round(t["time"] / len(questions), 2) if questions else 0,
            "avg_cost_usd": round(t["cost"] / len(questions), 6) if questions else 0,
        }

    # Save JSON
    output_path = OUTPUT_DIR / output_name
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n{'=' * 60}")
    print(f"Results saved to {output_path}")

    # Print summary
    _print_summary(output)

    # Save readable report
    report_path = OUTPUT_DIR / output_name.replace(".json", "_report.md")
    _write_report(output, report_path)
    print(f"Report saved to {report_path}")

    return output


def _print_summary(output: dict):
    """Print comparison summary to console."""
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    summary = output["summary"]
    providers = output["meta"]["providers"]

    header = f"{'指标':<25}"
    for p in providers:
        header += f"  {p:>12}"
    print(header)
    print("-" * (25 + 14 * len(providers)))

    metrics = [
        ("总输入 tokens", "total_input_tokens", "{:,}"),
        ("总输出 tokens", "total_output_tokens", "{:,}"),
        ("总费用 (USD)", "total_cost_usd", "${:.4f}"),
        ("总耗时 (s)", "total_time_s", "{:.1f}"),
        ("平均耗时 (s)", "avg_time_s", "{:.2f}"),
        ("平均费用 (USD)", "avg_cost_usd", "${:.6f}"),
    ]
    for label, key, fmt in metrics:
        row = f"{label:<25}"
        for p in providers:
            val = summary[p].get(key, 0)
            row += f"  {fmt.format(val):>12}"
        print(row)

    # Per-question tool comparison
    print(f"\n{'=' * 60}")
    print("TOOL SELECTION COMPARISON")
    print(f"{'=' * 60}")
    for r in output["results"]:
        print(f"\n{r['id']} ({r['category']}): {r['question'][:50]}...")
        for p in providers:
            if p in r and "tools_planned" in r[p]:
                tools = r[p]["tools_planned"]
                print(f"  {p:>10}: {tools}")


def _write_report(output: dict, path: Path):
    """Write a readable markdown report."""
    providers = output["meta"]["providers"]
    models = output["meta"].get("models", {})
    lines = [
        f"# P28 模型MCP对比评估报告",
        f"",
        f"生成时间: {output['meta']['timestamp']}",
        f"问题数量: {output['meta']['questions_count']}",
        f"",
        f"## 模型信息",
        f"",
        f"| Provider | Model ID |",
        f"|----------|----------|",
    ]
    for p in providers:
        m = models.get(p, "unknown")
        if isinstance(m, dict):
            lines.append(f"| {p} | router=`{m['router']}`, answerer=`{m['answerer']}` |")
        else:
            lines.append(f"| {p} | `{m}` |")

    lines.extend([
        "",
        f"## 总览",
        f"",
        f"| 指标 | " + " | ".join(providers) + " |",
        f"|------|" + "|".join(["------"] * len(providers)) + "|",
    ])

    summary = output["summary"]
    for label, key, fmt in [
        ("总费用", "total_cost_usd", "${:.4f}"),
        ("总耗时", "total_time_s", "{:.1f}s"),
        ("平均耗时", "avg_time_s", "{:.2f}s"),
        ("总输入tokens", "total_input_tokens", "{:,}"),
        ("总输出tokens", "total_output_tokens", "{:,}"),
    ]:
        vals = " | ".join(fmt.format(summary[p].get(key, 0)) for p in providers)
        lines.append(f"| {label} | {vals} |")

    # ── Tool Selection Comparison Table ──
    lines.extend(["", "## 工具选择对比", ""])
    if len(providers) == 2:
        p1, p2 = providers
        lines.append(f"| 问题 | 类型 | {p1} 工具 | {p2} 工具 | 工具相同 |")
        lines.append(f"|------|------|----------|----------|----------|")
        same_count = 0
        total_count = 0
        for r in output["results"]:
            if p1 not in r or p2 not in r:
                continue
            if "error" in r[p1] or "error" in r[p2]:
                continue
            total_count += 1
            t1 = sorted(r[p1].get("tools_planned", []))
            t2 = sorted(r[p2].get("tools_planned", []))
            same = t1 == t2
            if same:
                same_count += 1
            t1_str = ", ".join(r[p1].get("tools_planned", []))
            t2_str = ", ".join(r[p2].get("tools_planned", []))
            match_icon = "YES" if same else "NO"
            lines.append(f"| {r['id']} | {r['category']} | {t1_str} | {t2_str} | {match_icon} |")
        if total_count > 0:
            lines.append(f"")
            lines.append(f"**工具选择一致率: {same_count}/{total_count} ({same_count/total_count*100:.0f}%)**")

    # ── Theory Section ──
    lines.extend([
        "",
        "## 核心结论：工具选择决定内容差异",
        "",
        "在 MCP 架构下，LLM 的作用分为两个阶段：",
        "",
        "1. **工具路由阶段**：LLM 根据问题决定调用哪些 MCP 工具（及参数）",
        "2. **回答生成阶段**：LLM 基于 MCP 返回的数据生成回答",
        "",
        "关键推理：**如果两个模型选择了完全相同的工具和参数，"
        "那么 MCP Server 返回的数据必然完全一致**——因为 MCP 工具是确定性函数，"
        "不关心调用者是哪个模型。此时，回答质量的差异仅来自第二阶段的文本生成能力。",
        "",
        "这意味着：",
        "- **工具选择是影响最终内容的第一决定因素**（决定了数据的完整性和相关性）",
        "- **回答生成是第二因素**（决定了对相同数据的组织和表达能力）",
        "- 在工具选择一致的情况下，模型差异的影响被大幅缩小",
        "- 优化 MCP 工具路由（如更好的工具描述、更智能的路由 prompt）"
        "可能比更换更贵的模型更具性价比",
        "",
    ])

    # ── Per-question details ──
    lines.extend(["## 逐题对比", ""])

    for r in output["results"]:
        lines.append(f"### {r['id']} ({r['category']})")
        lines.append(f"**问题**: {r['question']}")
        lines.append("")

        for p in providers:
            if p not in r or "error" in r[p]:
                lines.append(f"#### {p}: ERROR")
                if p in r:
                    lines.append(f"```\n{r[p].get('error', 'unknown')}\n```")
                continue

            d = r[p]
            m = models.get(p, "")
            m_str = f"router={m['router']}, ans={m['answerer']}" if isinstance(m, dict) else str(m)
            lines.append(f"#### {p} (`{m_str}`)")
            lines.append(f"- 工具选择: {d.get('tools_planned', [])}")
            lines.append(f"- 有效数据: {d.get('tools_data_count', 0)} 个查询返回数据")
            lines.append(f"- 耗时: {d.get('total_time_s', 0)}s (路由{d.get('route_time_s', 0)}s + 执行{d.get('exec_time_s', 0)}s + 回答{d.get('answer_time_s', 0)}s)")
            lines.append(f"- 费用: ${d.get('cost_usd', 0):.6f}")
            lines.append(f"- Tokens: 输入{d.get('total_input_tokens', 0):,} / 输出{d.get('total_output_tokens', 0):,}")
            lines.append("")
            lines.append(f"**回答:**")
            lines.append("")
            answer = d.get("answer", "")
            if len(answer) > 1500:
                answer = answer[:1500] + "\n\n... (截断)"
            lines.append(answer)
            lines.append("")

        lines.append("---")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="P28 模型MCP对比评估")
    all_providers = ["ds-flash", "ds-pro", "ds-hybrid", "claude"]
    parser.add_argument("--providers", default=None,
                        help=f"Comma-separated providers (choices: {','.join(all_providers)})")
    parser.add_argument("--limit", type=int, default=0, help="Limit to first N questions (0=all)")
    parser.add_argument("--output", default="comparison.json", help="Output filename")
    args = parser.parse_args()

    if args.providers:
        providers = [p.strip() for p in args.providers.split(",")]
    else:
        providers = ["ds-flash", "claude"]
    asyncio.run(run_comparison(providers=providers, limit=args.limit, output_name=args.output))
