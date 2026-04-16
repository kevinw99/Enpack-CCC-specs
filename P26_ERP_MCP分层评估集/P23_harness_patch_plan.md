# P23 Harness 接入 P26 题集 & P20S 工具 — Patch 计划

**前提**: 其他会话完成 P20E ↔ P20S/P20T 整合。
**目的**: 让 P23 harness 能消费 P26 题集并暴露 P20S 的 3 个新工具给 LLM Router，产出真实 MCP-level T1（对照本次 LLM-level T1）。

## 文件触点

| 文件 | 改动 |
|------|------|
| `源代码/mcp-kb-server/eval/harness_erp.py` | 新增 3 个工具路由（schema / relations / list_cached）、新增 `--questions` 参数支持 P26 题集 |
| `源代码/mcp-kb-server/eval/questions_p26.py`（新） | 加载 `规格/P26/questions/_all.json` 为 ERPQuestion 兼容结构 |
| `源代码/mcp-kb-server/eval/scorer.py` | 评分器调用 P26 的 validity/refusal/judge |
| `源代码/mcp-kb-server/eval/report_erp.py` | 按 L1-L8 分层聚合 |

## harness_erp.py 具体 diff（建议顺序）

### 1. 扩展 ROUTER_SYSTEM 工具清单（第 80-104 行附近）

```diff
-"可用工具：\n"
-"1. query_materials(keyword) ...\n"
+"可用工具：\n"
+"1. kingdee_get_schema(form_id) - 获取表单字段/枚举/业务含义的结构化 schema（P20S 产出）\n"
+"   必须在用 query_bills 前先调用，以确认字段存在\n"
+"2. kingdee_get_relations() - 获取跨表 JOIN 路径图（P20S 产出）\n"
+"3. kingdee_list_cached_schemas() - 列出已缓存的 schema 表单（32 张）\n"
+"4. kingdee_get_wiki(topic) - 获取业务规则/公司约定/伪问题清单（P20T 产出）\n"
+"   空 topic 返回目录；具体 topic 返回正文\n"
+"5. query_materials(keyword) ...\n"
```

### 2. 新增路由器的 prompt 提示词（第 91-95 行附近）

```diff
 "规则：\n"
-"- 最多规划3个工具调用步骤\n"
+"- 最多规划 5 个工具调用步骤\n"
+"- 涉及具体字段查询时，必须先 kingdee_get_schema 确认字段存在，再 query_bills\n"
+"- 跨表 JOIN 前先 kingdee_get_relations 看路径\n"
 "- 如果步骤之间有依赖，用 step_ref 标注\n"
```

### 3. execute_erp_step 新增 3 个 tool 分支（第 126-200 行附近）

```python
elif tool == "kingdee_get_schema":
    form_id = params.get("form_id", "")
    schema_path = _kingdee_root / "schema" / f"{form_id}.md"
    if schema_path.exists():
        return {"tool": tool, "params": params, "reason": reason,
                "data": {"form_id": form_id, "schema_md": schema_path.read_text(encoding="utf-8")}}
    else:
        # fallback 到原 describe_form
        result = await _describe_form(form_id)
        return {"tool": tool, "data": {"form_id": form_id, "raw": result}, "fallback": True}

elif tool == "kingdee_get_relations":
    p = _kingdee_root / "schema" / "relations.md"
    return {"tool": tool, "data": {"relations_md": p.read_text(encoding="utf-8")}}

elif tool == "kingdee_list_cached_schemas":
    p = _kingdee_root / "schema" / "index.json"
    return {"tool": tool, "data": json.loads(p.read_text(encoding="utf-8"))}

elif tool == "kingdee_get_wiki":
    topic = params.get("topic", "")
    wiki_dir = _kingdee_root / "wiki"
    if not topic:
        # 返回目录清单
        topics = [str(p.relative_to(wiki_dir)) for p in wiki_dir.rglob("*.md")]
        return {"tool": tool, "data": {"index": topics}}
    # 按 topic 路径查
    target = wiki_dir / f"{topic}.md"
    if not target.exists():
        # 模糊匹配
        matches = list(wiki_dir.rglob(f"*{topic.split('/')[-1]}*.md"))
        if matches:
            target = matches[0]
    if target.exists():
        return {"tool": tool, "data": {"topic": topic, "content": target.read_text(encoding="utf-8")}}
    return {"tool": tool, "data": None, "error": f"topic not found: {topic}"}
```

### 4. 引入 `--questions` CLI 参数（替代硬编码 QUESTIONS_ERP）

```python
parser.add_argument("--questions", type=Path, default=None,
                    help="P26 题集 JSON；未提供则用 P23 QUESTIONS_ERP")
# 入口处：
if args.questions:
    from questions_p26 import load_p26
    questions = load_p26(args.questions)
else:
    questions = QUESTIONS_ERP
```

### 5. 新建 `questions_p26.py`

```python
"""Load P26 questions/_all.json into ERPQuestion-compatible structure."""
from pathlib import Path
import json
from questions_erp import ERPQuestion

def load_p26(path: Path) -> list[ERPQuestion]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = []
    for q in data:
        out.append(ERPQuestion(
            id=q["id"],
            question=q["question"],
            department=q.get("layer", "P26"),  # 复用 department 字段装 layer
            complexity="P26",
            answer_type="查询",
            gap_type="B",
            erp_modules=q.get("required_forms", []),
            priority="高",
        ))
    return out
```

## 输出路径

```
源代码/mcp-kb-server/eval/results/p26_T1/answer_pairs.json   # Vanilla + MCP 答案对
源代码/mcp-kb-server/eval/results/p26_T1/scores.json         # 5 维主观评分
源代码/mcp-kb-server/eval/results/p26_T1/answers.jsonl       # 转给 P26 scorer 用
```

## 与 P26 scorer 的衔接

运行完 harness 后跑:

```bash
cd 规格/P26_ERP_MCP分层评估集
# answers.jsonl 从 answer_pairs.json 中抽"MCP"侧答案
python3 -m scorer.validity --answers ../../源代码/mcp-kb-server/eval/results/p26_T1/answers.jsonl \
    --questions questions/_all.json \
    --schema-dir ../../源代码/mcp-kingdee-server/schema \
    --out results/T1_real/validity.json
python3 -m scorer.refusal --answers ... --out results/T1_real/refusal.json
python3 -m scorer.judge --metric factual --answers ... --out results/T1_real/factual.json
python3 -m scorer.judge --metric business --answers ... --wiki-dir 源代码/mcp-kingdee-server/wiki --out results/T1_real/business.json
python3 -m scorer.aggregate --t0 results/T0 --t1 results/T1_real --out results/comparison_real.md
```

## 验证项（跑完后看）

| 观察点 | 期望 |
|--------|------|
| LLM 是否主动调 `kingdee_get_schema`？ | ≥ 70% 题主动调用（看 plan 日志）|
| T1_real validity 相对 LLM-level T1 | 差距 < 0.1 为通过 |
| L4 / L5 / L6 的 delta | 不小于 LLM-level 模拟 |
| L7 refusal | 与 LLM-level 持平（P20T 是否起效） |

## 阻塞解除信号

- [x] `源代码/mcp-kingdee-server/src/tools/schema.py` 已注册（P20S Phase 8）
- [x] `源代码/mcp-kingdee-server/CLAUDE.md` V0.2 路由段落存在
- [ ] `kingdee_get_wiki` 工具注册（P20T 接入，另一会话进行中）
- [ ] wiki/ 目录生成（P20T 产出）
- [ ] sample answer 翻新、旧 describe_form 降级为 fallback（另一会话进行中）
