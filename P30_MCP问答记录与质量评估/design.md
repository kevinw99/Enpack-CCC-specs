# Design: P30 MCP 问答记录与质量评估系统

## 架构

```
Pipeline (pipeline.py)
  │
  ├─ run_query() 开始 → recorder.start_session(question)
  │
  ├─ function calling 循环中:
  │   └─ 每个 tool_call 执行后 → recorder.record_tool_call(...)
  │
  └─ run_query() 结束 → recorder.end_session(answer, tokens, cost, ...)
       │
       ├──→ 写入本地 SQLite (data/recorder.db)
       │    同步调用，不阻塞 LLM 流程
       │
       └──→ 异步同步到 Supabase
            recorder.flush_to_supabase()
            批量上传，后台任务
              │
              ▼
         Supabase Postgres
         (AI-ALL 已有实例)
              │
              ▼
     ┌────────────────────────────┐
     │  评估流水线                   │
     │                              │
     │  1. 自动指标计算              │
     │  2. LLM-as-Judge 评分        │
     │  3. 抽样人工复核              │
     └────────────────────────────┘
```

## 模块设计

```
源代码/mcp-recorder/
├── __init__.py
├── recorder.py         # MCPRecorder — 核心类，管理 session 生命周期
├── models.py           # Pydantic 数据模型
├── store_sqlite.py     # SQLiteStore — 本地写入
├── store_supabase.py   # SupabaseStore — 异步批量同步
├── schema.sql          # DDL (sessions + tool_calls + evaluations)
├── evaluator.py        # 评估管道（自动指标 + LLM-as-Judge）
└── config.py           # 配置管理
```

### recorder.py — MCPRecorder

```python
class MCPRecorder:
    def start_session(self, question: str, source: str) -> str:
        """生成 session_id，写入 sessions 表 (status=running)"""

    def record_tool_call(
        self, session_id: str, round: int,
        tool_name: str, tool_args: dict,
        result: str, latency_ms: int, success: bool
    ):
        """写入 tool_calls 表"""

    def end_session(
        self, session_id: str, answer: str,
        model: str, latency_ms: int,
        prompt_tokens: int, completion_tokens: int,
        cost_usd: float, round_count: int,
        status: str = "complete"
    ):
        """更新 sessions 表，写入最终字段"""

    def flush_to_supabase(self):
        """异步批量同步未上传的记录到 Supabase"""
```

### models.py

```python
class SessionRecord(BaseModel):
    session_id: str
    timestamp: str
    source: str              # aliyun | cloudflare
    user_question: str
    final_answer: str | None
    model: str | None
    total_latency_ms: int | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    cost_usd: float | None
    round_count: int | None
    status: str              # running | complete | truncated | error | timeout

class ToolCallRecord(BaseModel):
    session_id: str
    round: int
    tool_name: str
    tool_args: str           # JSON string
    result_size: int | None
    latency_ms: int | None
    success: bool

class EvalRecord(BaseModel):
    session_id: str
    evaluator: str           # llm_judge | human
    accuracy: int | None
    specificity: int | None
    business_grounding: int | None
    source_attribution: int | None
    refusal_correctness: int | None
    overall_score: int | None
    eval_notes: str | None
    eval_timestamp: str
```

## 数据库 Schema

SQLite 和 Supabase 使用相同结构：

```sql
CREATE TABLE sessions (
    session_id         TEXT PRIMARY KEY,
    timestamp          TEXT NOT NULL,
    source             TEXT NOT NULL,
    user_question      TEXT NOT NULL,
    final_answer       TEXT,
    model              TEXT,
    total_latency_ms   INTEGER,
    prompt_tokens      INTEGER,
    completion_tokens  INTEGER,
    total_tokens       INTEGER,
    cost_usd           REAL,
    round_count        INTEGER,
    status             TEXT DEFAULT 'running',
    synced_to_supabase INTEGER DEFAULT 0
);

CREATE TABLE tool_calls (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id    TEXT NOT NULL REFERENCES sessions(session_id),
    round         INTEGER NOT NULL,
    tool_name     TEXT NOT NULL,
    tool_args     TEXT NOT NULL,
    result_size   INTEGER,
    latency_ms    INTEGER,
    success       INTEGER DEFAULT 1
);

CREATE INDEX idx_tool_calls_session ON tool_calls(session_id);
CREATE INDEX idx_sessions_timestamp ON sessions(timestamp);
CREATE INDEX idx_sessions_source ON sessions(source);

CREATE TABLE evaluations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id          TEXT NOT NULL REFERENCES sessions(session_id),
    evaluator           TEXT NOT NULL,
    accuracy            INTEGER,
    specificity         INTEGER,
    business_grounding  INTEGER,
    source_attribution  INTEGER,
    refusal_correctness INTEGER,
    overall_score       INTEGER,
    eval_notes          TEXT,
    eval_timestamp      TEXT NOT NULL
);

CREATE INDEX idx_evaluations_session ON evaluations(session_id);
```

## 集成点

### pipeline.py 改动

```python
# 初始化
from mcp_recorder import MCPRecorder
recorder = MCPRecorder(enabled=config.MCP_RECORDER_ENABLED)

# run_query() 中
session_id = recorder.start_session(
    question=user_query,
    source="aliyun"  # 或从环境变量读取
)

# function calling 循环中
for round_num, response in enumerate(llm_responses):
    for tool_call in response.tool_calls:
        start = time.time()
        result = mcp_manager.call_tool(tool_call.name, tool_call.args)
        elapsed = int((time.time() - start) * 1000)
        recorder.record_tool_call(
            session_id=session_id,
            round=round_num,
            tool_name=tool_call.name,
            tool_args=tool_call.args,
            result=result,
            latency_ms=elapsed,
            success=(result is not None)
        )

# 结束时
recorder.end_session(
    session_id=session_id,
    answer=final_answer,
    model=model_name,
    latency_ms=total_latency_ms,
    prompt_tokens=usage.prompt_tokens,
    completion_tokens=usage.completion_tokens,
    cost_usd=cost,
    round_count=len(llm_responses),
    status="truncated" if truncated else "complete",
)
```

### MAX_TOOL_ROUNDS 兜底分支（防幻觉）

主循环使用 `for ... else` 结构：仅当 10 轮跑完仍未收敛（无 break）才进入 `else` 兜底。兜底逻辑：

1. 置 `truncated = True`，向 stderr 输出告警（含 session_id）
2. 向 `messages` 追加一条 system 消息，约束模型行为：
   - 基于已收集到的工具结果直接作答
   - 信息不足时必须明确说明 `"根据已查询到的信息无法完整回答，缺少：<具体缺失项>"`
   - 禁止编造、推测或脑补未在工具结果中出现的事实
3. 以 `tool_choice="none"` 调用 LLM 强制收敛产出文字答案
4. 该次调用的 token/延迟仍计入总账
5. `end_session(status="truncated")` 入库，`PipelineResult.truncated=True` 透出给上层

**为什么需要：** 进入兜底说明模型仍想调工具但额度耗尽，此时直接禁用工具最容易出现幻觉。追加的 system 指令把模型推向"承认缺失"而非"硬答"；`status="truncated"` 标记使后续可通过 `SELECT count(*) WHERE status='truncated'` 监控触发频率，频繁触发则提示需要提升 `MAX_TOOL_ROUNDS` 或优化工具/prompt 设计。

## 评估流水线

### 自动指标

```python
# SQL 查询直接计算，无需额外存储
SELECT
    date(timestamp) as day,
    COUNT(*) as total_questions,
    ROUND(AVG(total_latency_ms)) as avg_latency_ms,
    ROUND(AVG(round_count), 1) as avg_rounds,
    ROUND(SUM(cost_usd), 4) as total_cost,
    ROUND(AVG(cost_usd), 6) as avg_cost,
    SUM(CASE WHEN status='error' THEN 1 ELSE 0 END) as error_count,
    SUM(CASE WHEN status='truncated' THEN 1 ELSE 0 END) as truncated_count
FROM sessions
GROUP BY date(timestamp);
```

### LLM-as-Judge

- 复用 P26 的 scoring prompt 模式
- 输入：user_question + final_answer（可选 + tool_calls 上下文）
- 输出：五维度评分 + 理由简述
- 模型：DeepSeek（成本优先），可通过配置切换
- 写入 evaluations 表

### 人工复核

- 脚本 `sample_for_review.py`：按条件抽选（如：低分记录、新问题类型、随机采样）
- Markdown 格式输出，供人工打分
- `import_reviews.py`：导入人工评分到 evaluations 表

## 配置

```python
# config.py
import os

MCP_RECORDER_ENABLED = os.getenv("MCP_RECORDER_ENABLED", "true").lower() == "true"
MCP_RECORDER_STORE = os.getenv("MCP_RECORDER_STORE", "both")  # sqlite | supabase | both
MCP_RECORDER_SAMPLE_RATE = float(os.getenv("MCP_RECORDER_SAMPLE_RATE", "1.0"))
MCP_RECORDER_DB_PATH = os.getenv("MCP_RECORDER_DB_PATH", "data/recorder.db")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
```

## Key Decisions

- **只改 Pipeline，不动 MCP Server**: Pipeline 拥有完整上下文（问题→工具调用→答案→Token→费用），MCP Server 只能看到孤立工具调用
- **SQLite 本地 + Supabase 集中**: 兼顾写入可靠性（SQLite 同步）和分析便利性（Supabase SQL + Dashboard）
- **复用 AI-ALL Supabase**: 不新增基础设施，与另一个仓库共享 Postgres 实例
- **记录层不影响 LLM 调用路径**: SQLite 写入是同步的（确保不丢数据），但写入在 LLM 调用之外，不增加 API 调用延迟
- **评估级独立于记录级**: 记录是实时的，评估是异步的。系统不强制每次记录后立即评估
- **兜底分支防幻觉**: MAX_TOOL_ROUNDS 触顶时，禁用工具的兜底调用前显式追加"信息不足请直接说"的 system 指令，并将会话状态标记为 `truncated`，避免模型在数据不全时硬答

## Risk Mitigation

- **SQLite 文件增长**: 预估每天 200 条 × 365 天 = 73k 条/年，SQLite 轻松支持百万级。定期归档旧数据到 Supabase 即可
- **Supabase 同步失败**: SQLite 保留全量数据作为原始数据源，同步失败不丢数据，重试机制保证最终一致
- **PII/敏感数据**: user_question 和 final_answer 可能包含业务敏感信息。Supabase 端需开启 RLS，确保只有授权用户可读取
