# Status: P20T TextToSql

## Current Status
**Overall**: Planning
**Started**: 2026-04-15
**Last Updated**: 2026-04-15

## Completed Work

- 2026-04-15: 创建规格文档（requirements, design, tasks, status）

## Current Work

- 规格文档已完成，等待确认后开始 Phase 1

## Remaining Work

- [ ] Phase 1: 建立 LLM Wiki 骨架
- [ ] Phase 2: 核心业务主题 Wiki 页面
- [ ] Phase 3: 集成验证
- [ ] Phase 4: 补全样本问题库答案
- [ ] Phase 5: 知识沉淀机制

## Session Notes

### Session 2026-04-15
- Accomplished: 基于讨论记录和 ERP MCP 建设现状文档，创建 P20T 规格
- Findings:
  - 当前 V0.1 方案（单文件指南）已验证可行但有三个明确瓶颈
  - 52 题中约 24 题可通过 ERP 回答，其余为伪问题/数据缺口/外部数据
  - Q013 的三次修正是典型案例，说明语义层缺失的代价
  - 讨论中提到 Vanna/Text2SQL 方向，但当前阶段 LLM Wiki 更轻量可行
- Next steps: 确认 Wiki 存放位置，开始 Phase 1
- Blockers: 枚举值需要业务人员（吕经理）配合确认

## Key Metrics（目标）

| 指标 | 当前 | 目标 |
|------|------|------|
| 已完成答案题数 | 10/52（19%） | 34/52（65%，可回答题全覆盖） |
| Q013 式错误复现 | 有 | 零 |
| Wiki 主题页面数 | 0 | 10+ |
| 伪问题显式标注 | 部分（问题库备注） | 全部（Wiki 清单） |
