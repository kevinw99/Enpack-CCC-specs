# Design: P28 模型MCP对比评估

## 架构

```
问题集 → [Router LLM] → 工具调用计划
                            ↓
                     [KB MCP 工具] + [ERP MCP 工具]  (直接调用，非 MCP 协议)
                            ↓
                     MCP 返回数据 → [Answerer LLM] → 回答
                            ↓
                     对比报告 (DeepSeek vs Claude Opus)
```

## 两种模式

### Mode A: DeepSeek 全链路
- Router: DeepSeek → 规划工具调用
- 执行: 直接调用 KB/ERP 工具函数
- Answerer: DeepSeek → 基于 MCP 数据生成回答

### Mode B: Claude Opus 全链路
- Router: Claude Opus → 规划工具调用
- 执行: 同样的工具函数（保证数据源一致）
- Answerer: Claude Opus → 基于 MCP 数据生成回答

## 复用策略

直接复用 P21/P23 的：
- `common.llm_client` — LLM 调用封装
- KB 工具函数 (search_knowledge_base 等)
- ERP 工具函数 (query_materials, query_bills 等)
- ERP router prompt 模式

新增：
- 统一路由器（同时覆盖 KB + ERP 工具）
- 对比输出格式
- 成本/延迟统计

## 问题集设计

混合 KB 和 ERP 场景，分 3 类：

1. **KB-only**: 公司背景、产品、行业（复用 P21 问题）
2. **ERP-only**: 库存、采购、财务（复用 P23 问题）
3. **KB+ERP 混合**: 需要同时用两类工具的问题（新增）

## 输出格式

```json
{
  "meta": {"timestamp": "...", "questions_count": 10},
  "results": [
    {
      "id": "KB-01",
      "question": "...",
      "category": "kb_only",
      "deepseek": {
        "tools_planned": [...],
        "tools_data_count": 3,
        "answer": "...",
        "input_tokens": 1200,
        "output_tokens": 800,
        "total_time_s": 5.2,
        "cost_usd": 0.0004
      },
      "claude": {
        "tools_planned": [...],
        "tools_data_count": 3,
        "answer": "...",
        "input_tokens": 1200,
        "output_tokens": 600,
        "total_time_s": 8.1,
        "cost_usd": 0.0126
      }
    }
  ],
  "summary": {
    "deepseek": {"total_cost": 0.005, "avg_time": 4.8},
    "claude": {"total_cost": 0.15, "avg_time": 7.2}
  }
}
```
