# Tasks: ERP MCP问答质量评估 (ERP MCP Q&A Quality Evaluation)

## Phase 0: Prerequisites — 待ERP MCP就绪
- [ ] Task 0.1 - 确认ERP MCP支持的模块范围 (采购/销售/生产/库存/财务)
- [ ] Task 0.2 - 确认ERP MCP的接入方式 (MCP tools? API? 搜索注入?)
- [ ] Task 0.3 - 确认测试环境 (测试数据库 vs 生产系统只读?)

## Phase 1: 测试集准备 — ✅ 完成 (2026-04-13)
- [x] Task 1.1 - 从P18问题库筛选B类缺口问题 (P19标注的ERP数据依赖型)
- [ ] Task 1.2 - 按ERP MCP已支持模块进一步筛选可评估问题 (待ERP MCP就绪)
- [x] Task 1.3 - 标注每题所需的ERP数据类型 (采购记录/库存/订单/财务等)
- [x] Task 1.4 - 确定最终测试集: 28题 (7采购+5销售+6生产+5供应链+4财务+1管理)

**测试集统计**: 28题, B类21题+B+C类7题, 高优先级18题, 覆盖6部门

## Phase 2: 框架适配 — 部分完成
- [x] Task 2.1 - 新建 `eval/questions_erp.py` (28题ERP问题子集)
- [ ] Task 2.2 - 适配 `eval/harness.py` Config B: 调用ERP MCP获取数据 (待ERP MCP就绪)
- [x] Task 2.3 - 改进 `eval/scorer.py` 评委提示: 增加可信度评分说明
- [ ] Task 2.4 - 验证工具链: 试跑2-3题确认端到端流程 (待ERP MCP就绪)

## Phase 3: 评估执行
- [ ] Task 3.1 - 运行完整评估: DeepSeek生成 + DeepSeek评委
- [ ] Task 3.2 - 交叉验证: Claude生成 + Claude/DeepSeek双评委
- [ ] Task 3.3 - 生成记分卡和失败分析

## Phase 4: 分析与报告
- [ ] Task 4.1 - ERP MCP评估报告 (维度分析、覆盖度分析)
- [ ] Task 4.2 - 与P21 KB MCP结果对比分析
- [ ] Task 4.3 - 可选: KB+ERP联合评估 (两个MCP同时启用)
- [ ] Task 4.4 - 综合建议: ERP MCP优化方向

## Notes

- 依赖永志的ERP MCP分支达到可评估状态
- Phase 1-2可提前完成（不需要ERP MCP就绪）
- P21 eval工具链位于 `源代码/mcp-kb-server/eval/`
