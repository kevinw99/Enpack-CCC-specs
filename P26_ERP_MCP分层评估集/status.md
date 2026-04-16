# Status: P26 ERP MCP 分层评估集

## Current Status

**Overall**: Phase 0-4 + Phase 6 V0.5 完成（评分器 v2 升级：refusal gating + hit_rate；演进报告 V0.5 中期版发出；等 P20E 真实整合 + P20T 上线后补 T2 + V1）
**Started**: 2026-04-15
**Last Updated**: 2026-04-15

## Completed Work

- 2026-04-15: 规格初稿（requirements / design / tasks / status）
- 2026-04-15: **Phase 0 事后分层** — `layering_P23_28q.md`，28 题按 L1-L8 打标，识别 L2/L5 严重空白
- 2026-04-15: **Phase 1 题集 V1 46 题** — `questions/L1-L8_*.json` + `_all.json`（L1:5, L2:10, L3:6, L4:5, L5:3, L6:7, L7:6, L8:4）
- 2026-04-15: **Phase 2A validity 评分器** — `scorer/validity.py`，复用 P20S schema/{form}.md 字段池
- 2026-04-15: **Phase 2B refusal 启发式评分器** — `scorer/refusal.py`，关键词 + 反向信号
- 2026-04-15: **Phase 2C 分层汇总 + 对比** — `scorer/aggregate.py`，T0/T1/T2 三段对比 + delta
- 2026-04-15: **Phase 3 T0 基线** — 46 题 LLM-level T0（无 schema 注入） → `results/T0/validity.json`
- 2026-04-15: **Phase 4 T1 预览** — 46 题 LLM-level T1（注入 schema）→ `results/T1/validity.json`
- 2026-04-15: **T0→T1 对比报告** — `results/T0_T1_baseline_report.md`，L2/L4/L8 验证 P20S 价值，L5 发现评分器漏洞并修复（F_BDK_* 字段）
- 2026-04-15: **评分器 v2 升级** — refusal gating（picked=[] 剔除）+ hit_rate 指标（对 required_fields_hint 命中）
- 2026-04-15: **重跑 T0/T1 并更新报告** — validity 整体 +0.233 → **+0.336**；L1/L3/L6 真相浮出
- 2026-04-15: **Phase 6 V0.5 中期报告** — `results/能力演进报告_V0.5.md`（T0+T1 LLM-level，T2 待补）
  - 背景: P23 用 P19 标注的 28 题跑了一轮基线评估，结果良好
  - 动机: 28 题按"是否依赖 ERP 数据"筛选，不能暴露 P20S/P20T 的增益维度
  - 核心设计:
    - 8 个价值维度（L1-L8）：控制组 / 字段幻觉 / JOIN / 枚举 / 自定义字段 / 业务规则 / 伪问题 / 多步分析
    - 4 个分层指标：field_validity_rate（P20S 直接）/ factual_correctness / business_grounding / refusal_correctness
    - 三段评估：T0（P20E 原样）/ T1（整合 P20S）/ T2（整合 P20S+P20T）
    - 归因方法: 每层 delta 按预期 P20S/P20T 增益维度分解

## Current Work

- T0/T1 LLM-level 基线已产出，核心假设得到验证（P20S 对 L2/L4/L8 有显著增益）
- 待业务方（吕经理）审核 L5/L6 题目的业务准确性
- 待 P20E 整合 P20S 完成后补跑真实 MCP-level T1，与 LLM-level T1 做交叉验证
- 待 P20T 完成后跑 T2（Wiki 注入），重点看 L4/L6/L7/L8 的增益

## Remaining Work

- [ ] Phase 0: 对齐 P23 结果（事后分层）
- [ ] Phase 1: 题集 V1（A 分层、B 新增、C 标注）
- [ ] Phase 2: 指标实现（validity / refusal / 分层汇总）
- [ ] Phase 3: T0 基线
- [ ] Phase 4: T1 评估（需 P20E 整合 P20S）
- [ ] Phase 5: T2 评估（需 P20T 完成 + P20E 整合 P20T）
- [ ] Phase 6: 三段对比报告
- [ ] Phase 7: 持续运营

## Key Design Decisions

### Decision 1: 新规格 vs 扩展 P23
- 选: **新规格 P26**
- 理由: P23 作为评估框架/harness 保持稳定；P26 独立演进题集与分层方法
- P23 28 题基线结果保留为 T0 参考点

### Decision 2: 编号选择
- 选: **P26**（P24 已被"KB 适配问题集生成"占用，P25 是"团队全员会议"）
- 和 P24 关系: 可能有重叠方法论（都是题集设计），但 P24 针对 KB，P26 针对 ERP MCP，场景不同

### Decision 3: T0/T1/T2 分离评估
- 选: **三段分离跑**
- 理由: 避免 P20S 和 P20T 的增益混淆，每步可归因
- 成本: 题集 × 3 次跑，但可分期执行

### Decision 4: validity 作为先导指标
- 选: **field_validity_rate 优先**
- 理由: 自动可评（不需 LLM judge），廉价，直接对应 P20S 核心价值
- 风险: 有效性≠正确性（真实字段 + 错误数据也 validity=100%），需配合 factual_correctness

### Decision 5: 伪问题的权重
- L7 单独成层而不是混入 L6
- 理由: "正确拒答"是 P20T 独特能力，混入会稀释归因

## Open Questions

1. 题集合计 46 题是否合适？更少会缺分辨率，更多会超预算
2. `expected_p20s_gain` 定性（none/small/medium/large）是否够，是否需要数值化
3. T1 评估时，P20E 集成 P20S 的"验收标准"是什么？（CLAUDE.md 改 + tool 描述改 + N 个样本答案翻新 ≥ 多少？）
4. 吕经理审核能否跟上 Phase 1C 节奏？若不能，MVP 先用 AI 初稿

## Session Notes

### Session 2026-04-15
- Context: 用户询问 P20S/P20T 完成后，P23 的 28 题评估是否能反映能力提升
- Finding 1: 28 题按"数据来源"筛选，不按"能力缺失归因"筛选，对 P20S/P20T 增益不敏感
- Finding 2: 即使 P20S 代码已落地并注册了新工具，只要 P20E 的 CLAUDE.md / tool docstring / 样本答案不改，LLM 不会主动使用新工具 → 评估结果不会变
- Decision: 需要新评估题集（P26）+ P20E 整合层改动（属 P20E，待 P23 评估后安排）
- Next steps: 等 P23 评估结束 → Phase 0 事后分层 → Phase 1 题集构建

## Relationship Summary

```
   P20E（MCP Server + 工具）
     ├── P20S（Schema 抽取）→ 影响 L2/L3/L4/L5 得分
     └── P20T（Wiki/Text2SQL）→ 影响 L4/L6/L7/L8 得分

   P18（52 题题池）
     ↓
   P19（KB/ERP 依赖分类）
     ↓
   P23（评估框架 harness，已跑 28 题）
     ↓
   ★ P26（分层题集 + 分层指标 + 三段归因）← 本规格
```
