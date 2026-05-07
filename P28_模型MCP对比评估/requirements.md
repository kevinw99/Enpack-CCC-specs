# Requirements: P28 模型MCP对比评估

## 目标

对比 DeepSeek 和 Claude Opus 两种模型在调用 MCP Server（知识库 + ERP）时的效果差异，量化不同模型对 MCP 工具链的利用能力。

## 背景

- P21 已验证 KB MCP 对知识问答的增益（vanilla vs MCP-augmented，同一模型）
- P23 已验证 ERP MCP 对业务问答的增益
- 但尚未对比不同模型在 MCP-augmented 场景下的表现差异
- DeepSeek 成本低但推理能力有限，Claude Opus 成本高但推理强

## 核心问题

1. 工具路由差异：两种模型是否选择不同的 MCP 工具？选择的合理性？
2. 上下文利用差异：相同的 MCP 返回数据，两种模型的回答质量差异多大？
3. 成本效益：Claude Opus 更高的成本是否带来显著的质量提升？

## 测试范围

### 两个 MCP Server
- **KB MCP** (enpack-kb-server): search_knowledge_base, get_document, list_topics, get_company_profile, lookup_product, lookup_competitor, get_industry_context
- **ERP MCP** (kingdee_mcp): kingdee_get_schema, kingdee_get_relations, kingdee_get_wiki, query_materials, query_inventory, query_bills, query_fixed_assets, futures_spot, futures_analysis

### 两种模型
- **DeepSeek** (deepseek-chat): 成本敏感，OpenAI 兼容 API
- **Claude Opus** (claude-opus-4-20250514): 高推理能力，Anthropic API

## 评估维度

| 维度 | 说明 |
|------|------|
| tool_selection | 路由器选择了哪些工具，是否合理 |
| answer_quality | 回答的准确性和完整性 (1-5 分) |
| data_utilization | 对 MCP 返回数据的利用程度 |
| latency | 端到端响应时间 |
| token_usage | 输入/输出 token 数 |
| cost | 美元成本 |

## 交付物

1. 对比脚本 `compare.py`
2. 包含 KB + ERP 混合问题的测试集
3. JSON 格式的原始结果
4. 可读的对比报告
