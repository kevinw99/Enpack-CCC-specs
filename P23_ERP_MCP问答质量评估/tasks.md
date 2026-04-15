# Tasks: ERP MCP问答质量评估 (ERP MCP Q&A Quality Evaluation)

## Phase 0: Prerequisites — ✅ 完成 (2026-04-15)
- [x] Task 0.1 - 确认ERP MCP支持的模块范围: 6个金蝶工具 + 4个期货工具
- [x] Task 0.2 - 确认ERP MCP的接入方式: 直接调用金蝶API函数 (LLM路由器 + 数据注入)
- [x] Task 0.3 - 确认测试环境: 金蝶云星空生产系统只读查询

## Phase 1: 测试集准备 — ✅ 完成 (2026-04-13)
- [x] Task 1.1 - 从P18问题库筛选B类缺口问题 (P19标注的ERP数据依赖型)
- [x] Task 1.2 - 按ERP MCP已支持模块进一步筛选可评估问题: 28题
- [x] Task 1.3 - 标注每题所需的ERP数据类型 (采购记录/库存/订单/财务等)
- [x] Task 1.4 - 确定最终测试集: 28题 (7采购+5销售+6生产+5供应链+4财务+1管理)

**测试集统计**: 28题, B类21题+B+C类7题, 高优先级18题, 覆盖6部门

## Phase 2: 框架适配 — ✅ 完成 (2026-04-15)
- [x] Task 2.1 - 新建 `eval/questions_erp.py` (28题ERP问题子集)
- [x] Task 2.2 - 新建 `eval/harness_erp.py`: LLM路由器 + ERP API直调 + 数据注入
- [x] Task 2.3 - 改进 `eval/scorer.py` 评委提示: 增加可信度评分说明
- [x] Task 2.4 - 验证工具链: 试跑确认端到端流程
- [x] Task 2.5 - 新建 `eval/report_erp.py`: 适配ERP维度的报告生成器

## Phase 3: 评估执行 — ✅ DeepSeek完成 (2026-04-15)
- [x] Task 3.1 - 运行完整评估: DeepSeek生成 + DeepSeek评委 (28题, 82%胜率)
- [ ] Task 3.2 - 交叉验证: Claude生成 + Claude/DeepSeek双评委 (可选)
- [x] Task 3.3 - 生成记分卡和失败分析

## Phase 4: 分析与报告 — ✅ 主体完成 (2026-04-15)
- [x] Task 4.1 - ERP MCP评估报告: `results.md` (维度分析、覆盖度分析、失败模式)
- [x] Task 4.2 - 与P21 KB MCP结果对比分析 (包含在 results.md 第7节)
- [ ] Task 4.3 - 可选: KB+ERP联合评估 (两个MCP同时启用)
- [x] Task 4.4 - 综合建议: ERP MCP优化方向 (包含在 results.md 第8节)

## 核心结果

| 指标 | 值 |
|------|-----|
| ERP MCP 胜率 | **82%** (23胜 / 4负 / 1平) |
| 综合均分 (MCP) | **4.70** / 5.0 |
| 综合均分 (Vanilla) | 4.01 / 5.0 |
| 综合提升 | **+0.69** (+17.2%) |
| 最大维度提升 | 可操作性 +1.11 |
| 复杂问题胜率 | 100% (7/7) |

详细结果见 `results.md`

## Notes

- ERP MCP工具链: `eval/harness_erp.py` → `eval/scorer.py` → `eval/report_erp.py`
- 数据文件: `eval/results/answer_pairs_erp_deepseek.json`, `scores_erp_deepseek.json`
- P21 eval工具链位于 `源代码/mcp-kb-server/eval/`
