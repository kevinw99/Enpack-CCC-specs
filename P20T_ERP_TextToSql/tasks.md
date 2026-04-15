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

## Phase 2A: schema 枚举业务含义审核（与吕经理协作）

**Entry criteria**: ✅ schema/ 中已有 DEFAULT_ENUM_MAP 标注

- [ ] 2A.1 导出 schema/ 中所有已标注的枚举字段（FDocumentStatus / FApproveStatus / FStatus / FForbidStatus）
- [ ] 2A.2 吕经理审核 DEFAULT_ENUM_MAP 是否符合公司实际用法，发现偏差
- [ ] 2A.3 偏差/特殊用法（如"我们公司'已审核'=发票+收款都确认"）写入 wiki 对应主题页"公司特殊业务约定"段
- [ ] 2A.4 通用纠正回写 P20S（提请更新 DEFAULT_ENUM_MAP）
- [ ] 2A.5 公司自定义字段（`F_BDK_*`）的业务含义写入 wiki

## Phase 2B: 核心业务主题 Wiki 页面（业务流程，schema 抽不出）

**Entry criteria**: ✅ relations.md (Mermaid) 可作为数据流参考

- [ ] 2B.1 `wiki/采购/采购订单数据流.md` — 采购申请→采购订单→收料通知单→采购入库单（业务流程文字 + 引用 relations.md 对应片段）
- [ ] 2B.2 `wiki/销售/销售订单数据流.md` — 销售订单→出库单→应收单
- [ ] 2B.3 `wiki/库存/物料分类.md` — 靶材 vs 非靶材的查询路径差异、单位换算（公司个性化，必须人工写）
- [ ] 2B.4 `wiki/生产/生产订单数据流.md` — 生产订单→简单生产领料单→生产入库单，含线别字段
- [ ] 2B.5 `wiki/财务/应收应付.md` — 催收判断逻辑（业务规则）
- [ ] 2B.6 `wiki/固定资产/资产台账.md` — 部门资产统计业务规则
- [ ] 2B.7 `wiki/采购/采购成本分析.md` — 铜箔基材物料编码 vs 期货 MCP（公司个性化分析）

## Phase 3: 集成验证（V0.2 三层联动）

**Entry criteria**: Phase 1 + Phase 2B 主要主题页已建

注：P20S regression 已用 5 用例实测 validity 58.3% → 100%。本阶段聚焦 wiki+schema 联动效果，不重复纯 schema 验证。

- [ ] 3.1 用 **Q013**（应收账款）端到端验证：list_cached_schemas → schema(SAL_Receivable) → wiki 公司"已审核"业务约定 → 不再 B/C 混淆
- [ ] 3.2 用 **Q001**（采购审批合理性）：wiki 采购数据流 → schema → relations → query 取数
- [ ] 3.3 用 **Q007**（采购合同，伪问题）：路由直接命中伪问题清单
- [ ] 3.4 用 **Q006**（采购成本趋势）：wiki 采购成本分析（铜箔基材物料编码） → 期货 MCP
- [ ] 3.5 记录验证结果，分流回写：字段级 → 反馈 P20S；业务级 → 追加 wiki

## Phase 4: 补全样本问题库答案

**Entry criteria**: ✅ schema 已覆盖 32 张（远超原 ≥20 目标）；Phase 2B 主要主题页已建

- [ ] 4.1 补全采购部可回答题目：Q002, Q005, Q009
- [ ] 4.2 补全销售部可回答题目：Q011, Q012, Q013（修正版）, Q015
- [ ] 4.3 补全生产部可回答题目：Q019, Q022
- [ ] 4.4 补全财务部可回答题目：Q039, Q043
- [ ] 4.5 补全供应链可回答题目：Q036
- [ ] 4.6 更新 `样本问题库回答执行状态.md`
- [ ] 4.7 若题目涉及 schema 未覆盖的表（114/146 外部 lookup 目标），提请 P20S 扩 FORM_CATALOG

## Phase 5: 知识沉淀机制（持续）

**Entry criteria**: 无（与上面并行）

- [ ] 5.1 **分流回写规范**：
  - 字段级新发现（新枚举值/新关联/中文名缺失）→ 提 P20S issue / 重跑 enum_scanner / 扩 FORM_CATALOG
  - 业务级新发现（数据流变化/陷阱/公司私有规则）→ 追加对应 wiki 主题页
- [ ] 5.2 每月 lint 检查：AI 检查 wiki 是否与 schema 矛盾
- [ ] 5.3 将 `问题库回答指南.md` 标注为"已迁移，历史参考"
- [ ] 5.4 在 wiki/README.md 维护"已知 schema 缺口清单"反馈给 P20S 持续运营

## Phase 6（可选）: Text2SQL 演进探索

**Entry criteria**: ✅ 全部满足（schema + relations + LLM 注解基础设施全到位）

P20S 已消除 Vanna 路径的全部历史障碍。本阶段评估是否值得引入：

- [ ] 6.1 评估 Vanna 框架可行性
- [ ] 6.2 选 5 个典型查询做 PoC：wiki+schema 路由 vs Vanna 自动生成 SQL
- [ ] 6.3 评估准确率、开发成本、维护成本，决定是否切换

## Notes

- P20S 全量到位后，**Wiki 工作量大幅缩小**：原计划 10-15 个主题页，每页要写字段表/枚举值；现在每页只写业务流程 + 公司特殊约定 + 陷阱
- Phase 1/2A/2B 可并行（不同人负责）
- 公司个性化数据流（靶材 vs 非靶材、应收"已审核"业务约定）只能由业务人员提供，是 wiki 不可替代的部分
- 字段中文名 100% 覆盖 + DEFAULT_ENUM_MAP 已固化 → Phase 2A 工作量低于预期，主要在审核而非补全
