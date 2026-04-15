# Tasks: P20T ERP TextToSql

> **P20S 已全量交付**（32 张表 / 3647 字段 / 中文名 100% / DEFAULT_ENUM_MAP / relations 图 / regression validity 100%）。
> 所有 Phase 的 entry criteria 已经满足，可以全速启动。

## Phase 1: 建立 LLM Wiki 骨架

**Entry criteria**: ✅ 全部满足

- [ ] 1.1 创建 `wiki/` 目录结构（采购/销售/生产/库存/财务/固定资产/伪问题与数据缺口）
- [ ] 1.2 创建 `wiki/README.md`：业务主题索引 + 强调"字段/关联走 MCP 工具，wiki 只放公司私有业务规则"
- [ ] 1.3 将 `问题库回答指南.md` 按主题拆分；**字段表/关联说明全部删除**，改为引用 schema 工具
- [ ] 1.4 创建 `wiki/伪问题与数据缺口/无法回答的问题清单.md`（录入 Q007, Q010, Q016, Q018, Q020, Q021, Q025, Q033, Q035）
- [ ] 1.5 更新 `CLAUDE.md`，加入 V0.2 路由规则（list_cached_schemas → wiki/schema/relations 分流 → query）

## Phase 2A: schema 枚举业务含义审核（与吕经理协作） ✅ Done

**Entry criteria**: ✅ schema/ 中已有 DEFAULT_ENUM_MAP 标注

- [x] 2A.1 导出 schema/ 中所有已标注的枚举字段（FDocumentStatus / FApproveStatus / FStatus / FForbidStatus）
- [x] 2A.2 吕经理审核 DEFAULT_ENUM_MAP — 通用语义无需调整
- [x] 2A.3 应收单特殊用法（B=催收候选、C=款到不催收）写入 `wiki/销售/销售订单数据流.md` + `wiki/财务/应收应付.md`
- [x] 2A.4 无需回写 P20S（DEFAULT_ENUM_MAP 通用语义正确）
- [ ] 2A.5 公司自定义字段（`F_BDK_*`）语义 — 等 AI 实际遇到时沉淀

## Phase 2B: 核心业务主题 Wiki 页面（业务流程，schema 抽不出）

**Entry criteria**: ✅ relations.md (Mermaid) 可作为数据流参考

- [ ] 2B.1 `wiki/采购/采购订单数据流.md` — 采购申请→采购订单→收料通知单→采购入库单（业务流程文字 + 引用 relations.md 对应片段）
- [ ] 2B.2 `wiki/销售/销售订单数据流.md` — 销售订单→出库单→应收单
- [ ] 2B.3 `wiki/库存/物料分类.md` — 靶材 vs 非靶材的查询路径差异、单位换算（公司个性化，必须人工写）
- [ ] 2B.4 `wiki/生产/生产订单数据流.md` — 生产订单→简单生产领料单→生产入库单，含线别字段
- [ ] 2B.5 `wiki/财务/应收应付.md` — 催收判断逻辑（业务规则）
- [ ] 2B.6 `wiki/固定资产/资产台账.md` — 部门资产统计业务规则
- [ ] 2B.7 `wiki/采购/采购成本分析.md` — 铜箔基材物料编码 vs 期货 MCP（公司个性化分析）

## Phase 3: 集成验证（V0.2 三层联动） ✅ Done

**Entry criteria**: Phase 1 + Phase 2B 主要主题页已建

注：P20S regression 已用 5 用例实测 validity 58.3% → 100%。本阶段聚焦 wiki+schema 联动效果，不重复纯 schema 验证。

- [x] 3.1 **Q013**（应收账款）端到端：list_cached_schemas → wiki(应收应付) 得到"B=催收、C=款到" → schema(AR_Receivable) → query。结果与已有 `answer/q013_answer.md` 一致
- [x] 3.2 **Q001**（采购审批合理性）：wiki(采购数据流) → relations → schema → query。符合已有答案流程
- [x] 3.3 **Q007**（采购合同，伪问题）：路由直接命中伪问题清单，不查 ERP
- [x] 3.4 **Q006**（采购成本趋势）：wiki(采购成本分析) 先确认物料编码 → 期货 MCP 联动
- [x] 3.5 验证结果记录在 `docs/Phase3_集成验证结果.md`；schema 缺口（SAL_SaleOrder/AR_Receivable/SAL_PriceList/简单生产领料单/FIN_CostCalculation）已记入 `wiki/README.md` 缺口清单

## Phase 4: 补全样本问题库答案

**Entry criteria**: ✅ schema 已覆盖 32 张（远超原 ≥20 目标）；Phase 2B 主要主题页已建

- [ ] 4.1 补全采购部可回答题目：Q002, Q005, Q009
- [ ] 4.2 补全销售部可回答题目：Q011, Q012, Q013（修正版）, Q015
- [ ] 4.3 补全生产部可回答题目：Q019, Q022
- [ ] 4.4 补全财务部可回答题目：Q039, Q043
- [ ] 4.5 补全供应链可回答题目：Q036
- [ ] 4.6 更新 `样本问题库回答执行状态.md`
- [ ] 4.7 若题目涉及 schema 未覆盖的表（114/146 外部 lookup 目标），提请 P20S 扩 FORM_CATALOG

## Phase 5: 知识沉淀机制（规范文档已交付，执行持续）

**Entry criteria**: 无（与上面并行）

- [x] 5.1 **分流回写规范**：见 `wiki/知识沉淀规范.md`（按发现性质分流到 schema / wiki / 缺口清单）
- [x] 5.2 月度 lint 清单：已在 `wiki/知识沉淀规范.md` 中定义
- [x] 5.3 `问题库回答指南.md` 已在 CLAUDE.md 中标注为历史参考
- [x] 5.4 `wiki/README.md` 的"已知 schema 缺口清单"已填入 5 张缺口表

## Phase 6（可选）: Text2SQL 演进探索 — 评估完成，建议短期不上

**Entry criteria**: ✅ 全部满足（schema + relations + LLM 注解基础设施全到位）

- [x] 6.1 评估 Vanna 框架可行性 — 见 `docs/Phase6_Vanna_Text2SQL可行性评估.md`
  - 方案 A（真 SQL）：❌ 金蝶 API 不开放 SQL
  - 方案 B（Vanna + MCP query DSL）：✅ 可行，3-4 周开发
  - 方案 C（当前三层路由 + tool-use）：✅ 近期主推
- [x] 6.2 PoC 设计（5 个典型查询 + 评估指标 + 对比基准）
- [x] 6.3 决策建议：短期 3 个月内不上 Vanna；Phase 4 补全到 30+ 题后做基线评估；基线 < 70% 才启动 Vanna PoC

## Notes

- P20S 全量到位后，**Wiki 工作量大幅缩小**：原计划 10-15 个主题页，每页要写字段表/枚举值；现在每页只写业务流程 + 公司特殊约定 + 陷阱
- Phase 1/2A/2B 可并行（不同人负责）
- 公司个性化数据流（靶材 vs 非靶材、应收"已审核"业务约定）只能由业务人员提供，是 wiki 不可替代的部分
- 字段中文名 100% 覆盖 + DEFAULT_ENUM_MAP 已固化 → Phase 2A 工作量低于预期，主要在审核而非补全
