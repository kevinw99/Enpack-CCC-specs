# Tasks: P26 ERP MCP 分层评估集

## Phase 0: 对齐 P23 评估结果（前置）

- [x] 等 P23 当前轮评估完全收尾（2026-04-15 确认 `P23/results.md` 已发布，82% 胜率）
- [x] 读 P23 结果，标注 28 题每题属于 L1-L8 哪层（事后分层，建立对照）→ `layering_P23_28q.md`
- [x] 识别 P23 28 题中各层分布缺口 → L2/L5 严重空白，L3/L8 过载

## Phase 1: 题集构建 V1

### Phase 1A: 从现有题池分层

- [x] 读 `源代码/mcp-kb-server/eval/questions_erp.py` 的 28 题，按 L1-L8 打层标签
- [ ] 读 P18 样本问题库 52 题，挑选填补缺口的题（尤其 L5/L6/L7/L8）
- [x] 吸收 P20S `regression_cases.json` 的用例（Q013 → L2-01）

### Phase 1B: 新增题目

- [x] L5（自定义字段）3 题 — 基于 `F_BDK_LXR/F_BDK_DH` 设计
- [x] L6（业务规则）7 题 — 草稿，**待吕经理审核**
- [x] L7（伪问题）6 题 — 研发立项/OEE/考勤/竞品等
- [x] L8（多步分析）4 题 — 供应商评分、期货对比、经营简报

### Phase 1C: 题目标注

- [x] 每题按 design.md 的 JSON 格式编写
- [ ] 业务方审核 `reference_answer_points` 和 `required_fields_hint`（待吕经理）
- [x] 标注 `expected_p20s_gain` / `expected_p20t_gain`
- [x] 生成 `questions/L{N}_*.json` 和合并版 `_all.json`（46 题）

## Phase 2: 指标实现

### Phase 2A: field_validity_rate 自动评分

- [x] 实现字段 key 抽取器（`scorer/validity.py`：正则 `F[A-Z][A-Za-z0-9_]*`）
- [x] 对每 form 查 `schema/{form_id}.md` 的字段清单做匹配
- [x] 输出每题的 validity_rate 值 + 分层 summary
- [x] 与 P20S 的 `regression.py` 复用提取规则

### Phase 2B: refusal_correctness 评判

- [ ] LLM-as-Judge prompt 编写（可选二段）
- [x] 启发式关键词清单（"不在 ERP 中"、"建议查"、MES/CRM/PLM/HR/OA 等） → `scorer/refusal.py`
- [x] L7 题目启发式跑通（smoke test 1/6 正确拒答）

### Phase 2C: 分层汇总脚本

- [x] 按 layer 聚合 scorecard（`scorer/aggregate.py`）
- [x] T0 vs T1 vs T2 差异表 + delta
- [x] 归因提示模板

## Phase 3: T0 基线（复用 + 补充）

- [x] 复用 P23 28 题的 T0 结果（事后分层，见 `layering_P23_28q.md`）
- [x] 对 46 题跑 LLM-level T0（`scorer/runner.py --mode T0`）
- [x] 产出 `results/T0/validity.json` + `refusal.json`
- [x] 标注每层基线水平：L1 0.833 / L2 0.297 / L3 0.584 / L4 0.539 / L5 0.710 / L6 0.309 / L7 refusal 0.833 / L8 0.521

**Entry criteria**: Phase 1 完成、P23 当前轮结束、无 P20S/P20T 增量 ✅

## Phase 4: T1 评估（P20S 整合后）

- [x] **LLM-level T1** 先行（给 LLM 注入 schema 上下文模拟 P20E 整合效果）
- [ ] 等待 P20E 代码整合 P20S（CLAUDE.md 改指引、tool docstring 更新、样本答案翻新）
- [ ] 跑真实 MCP-level T1（状态 B）
- [x] 产出 `results/T1/validity.json` + `refusal.json` + `comparison.md`
- [x] 按层做 T0→T1 delta 分析，写归因报告 → `results/T0_T1_baseline_report.md`

**主要发现**:
- L2 +0.353（字段幻觉 ✅）, L4 +0.411（枚举 ✅）, L8 +0.448（多步 ✅）
- L6 +0.262（业务规则意外收益）
- L1 -0.033（可接受抖动，无副作用）
- L5 -0.075（评分器假象，非 P20S 问题 —— 见报告第 3 节）
- L7 refusal 不变（预期，P20T 才能动）

**Entry criteria for real T1**: P20E 整合 P20S 完成

## Phase 5: T2 评估（P20S + P20T 整合后）

- [ ] 等待 P20T Wiki / Text2SQL 落地
- [ ] 等待 P20E 集成 P20T（Wiki 工具或 context 注入）
- [ ] 跑 T2（状态 C）
- [ ] 产出 `results/T2/scorecard_by_layer.json`
- [ ] T1→T2 delta 分析，完成三段对比报告

**Entry criteria**: P20T 完成 + P20E 集成 P20T

## Phase 6: 报告与复盘

- [x] 《ERP MCP 能力演进报告》**V0.5 中期** — `results/能力演进报告_V0.5.md`（T0+T1 LLM-level）
- [ ] V1 正式版（需补真实 MCP-level T1 + T2）
- [x] 按层归因到 P20S（T0→T1） — 报告第 2 节
- [x] 反常信号分析（L5 hint 误写，L1/L3 超预期，L6 意外大增）
- [x] 题集缺口复盘（L3 过简、L5 hint 错、L1 略多） — 报告第 5.3 节
- [ ] V2 题集迭代计划（待业务方审核后定稿）

## Phase 7: 持续运营

- [ ] 新发现的典型错误 → 补入 P26 题集
- [ ] 季度复评（当 ERP MCP 有大改动时）
- [ ] 维护 `expected_*_gain` 的校准（若实际增益长期偏离预期，重新分层）

## Dependencies

| Phase | 依赖 |
|-------|------|
| Phase 0 | P23 当前轮评估完成 |
| Phase 1A-C | P18 题库、P19 分类、P20S regression_cases |
| Phase 2A | P20S schema/ 产出（已完成） |
| Phase 3 | Phase 1 完成，P23 harness 可用 |
| Phase 4 | P20E 代码整合 P20S（新任务，归 P20E） |
| Phase 5 | P20T 完成 + P20E 集成 P20T |

## Notes

- P26 专注"题集 + 指标 + 归因"，harness 复用 P23
- 所有代码改动与 P23 评估期隔离（P23 跑完再动手）
- T1/T2 的跑需要 P20E 代码整合完成，P26 无法单独完成这些
