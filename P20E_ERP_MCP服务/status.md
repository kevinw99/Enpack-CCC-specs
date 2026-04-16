# Status: P20E ERP MCP 服务

## Current Status

**Overall**: P20S/P20T 工具级整合完成（Phase 8.1-8.6），等跑 P26 real MCP-level T1/T2 做 gap 分析
**Started**: 2026-03-25（`yongzhi_erp_mcp_0325` 分支创建）
**Retrofit spec created**: 2026-04-15
**Last Updated**: 2026-04-15

## Completed Work

- 2026-03-25 ~ 2026-04-14: MCP Kingdee Server 核心开发
  - 金蝶 API 客户端、数据模型、8 个 ERP 工具
  - 期货模块（独立）
  - Claude Desktop / Claude Code 配置脚本
  - 完整文档体系（README + 9 个 docs）
- 2026-04-14 前: 完成样本问题答案 10 题（q001, q002, q004, q005, q006, q009, q011, q012, q013, q019）
- 2026-04-15: 回顾性创建本规格文档

## Current Work

- 持续编写样本问题答案（剩余可回答题约 14 题）
- 本规格作为 retrofit 记录已完成工作

## Remaining Work

- 样本问题答案 ~14 题
- `describe_form` 响应体积优化
- 与 P20T_ERP_TextToSql 对接（V0.2 方案演进）
- 与 P23 评估规格对接

## Session Notes

### Session 2026-04-15（P20S/P20T 工具级整合 — Phase 8）
- Context: 用户确认下一步应在 P26 T2 之前做 P20E 整合，因为 LLM-level T1 模拟（validity 0.829）是 ceiling，real MCP-level T1 需要整合才能跑
- Accomplished:
  - **Tool docstring 重写**（`src/tools/schema.py` 三个 P20S 工具、`src/tools/master_data.py` 的 describe_form）
    - `kingdee_get_schema` 加【P20S · 字段查询首选】强引导 + "何时用/何时不用"分工表
    - `kingdee_list_cached_schemas` 加 V0.2 六步路由推荐顺序
    - `kingdee_describe_form` 降级为【⚠️ 遗留兜底 · 不建议常用】
  - **新增 `kingdee_get_wiki` 工具**（`src/tools/wiki.py`）
    - 暴露 P20T wiki/ 的业务语义层给 LLM
    - topic="" 返回主题索引（11 个主题），topic="财务/应收应付" 返回正文
    - 路径穿越防护（拒绝 `..` 和 `/` 开头）
    - 注册到 `src/server.py`；venv python3.13 烟测通过
  - **CLAUDE.md V0.2 路由更新**：wiki 访问走 `kingdee_get_wiki`，明确禁止文件系统 Read wiki/schema
  - **q001/q013 答案刷新**：显式展示 6 步 MCP 工具链；q013 附加"为什么 wiki 必须先于 schema"的 Q013 教训说明，作为少样本示范
  - **P20E tasks.md 新增 Phase 8**：记录 8.1-8.6 已完成、8.7-8.10 待跑（P26 real T1 / T2 / P23 回测）
- Key design choice: 用 MCP 工具暴露 wiki（方案 a）而非让 LLM 直接文件系统 Read（方案 b），理由是评估可归因 + 统一入口 + 路径安全
- Next steps:
  - 8.7 跑 P26 real MCP-level T1（46 题），和 LLM-level T1 的 0.829 ceiling 对比
  - 若 gap ≤ 0.10，即可直接跑 8.9 T2（P20T wiki 已经集成）
  - 8.10 P23 28 题回测作为头条指标校验

### Session 2026-04-15
- Accomplished: 为已完成的 `源代码/mcp-kingdee-server/` 创建回顾性规格文档
- Context: 本分支（`yongzhi_erp_mcp_0325`）原将该工作归入 P18，现在做如下区分：
  - **P20E**（本规格）= 已完成的 V0.1 方案（MCP Server + 手工指南）
  - **P20T_ERP_TextToSql** = V0.2 演进方向（LLM Wiki / Text2SQL）
  - **P23_ERP_MCP问答质量评估** = 对本服务的质量评估框架（在 main 分支）
- Next steps: 将 retrofit spec 与源码目录交叉链接，确保文档可追溯

## Key Metrics

| 指标 | 当前 | 目标 |
|------|------|------|
| ERP 工具数 | 8 | 8（已达成） |
| 期货工具 | ✅ | ✅ |
| 答案覆盖率 | 10/52 (19%) | 24/52 (46%) |
| 文档数 | 10+ | 持续维护 |
| 已知缺陷 | 4 项（T1-T4） | 逐步由下一代规格解决 |
