# Status: P20T ERP TextToSql

## Current Status
**Overall**: Ready to Execute（V0.3 设计已对齐 P20S 实际交付；entry criteria 全部满足，可启动 Phase 1/2A/2B）
**Started**: 2026-04-15
**Last Updated**: 2026-04-15

## Completed Work

- 2026-04-15: 创建规格文档 V0.1（requirements, design, tasks, status）
- 2026-04-15: 重命名 P18 → P20T_TextToSql
- 2026-04-15: 重命名 P20T_TextToSql → P20T_ERP_TextToSql（含 P20E/P20S 交叉引用更新）
- 2026-04-15: **设计 V0.2 更新** — 基于 P20S 目标态接口契约重写
  - design.md 新增 Prerequisites 段，显式列出对 P20S 的依赖（已交付/进行中/未启动）
  - 架构从两层升级为三层（Schema 层 / 业务语义层 / 执行层）
  - Wiki 页面格式精简：字段表移除，改为引用 schema/{form_id}.md
  - 路由规则 V0.2：字段查询走 kingdee_get_schema，wiki 只承载业务语义
  - 新增 Decision 6/7（职责分离原则）
  - tasks.md 重组：Phase 2 拆为 2A（枚举业务含义）+ 2B（业务流程页），新增 Phase 6（Text2SQL 演进）
  - 每个 Phase 标注 entry criteria，明确对 P20S 阶段的依赖

## Current Work

- P20S 全量交付完成（10 phases / 32 tables / 100% 中文名 / DEFAULT_ENUM_MAP / relations / regression validity 100%）
- P20T 所有 Phase 的 entry criteria 已满足，可全面启动
- 下一步：启动 Phase 1（Wiki 骨架）+ Phase 2B（业务主题页）

## Remaining Work（P20S 交付后所有 entry criteria 已满足）

- [x] Phase 1: 建立 LLM Wiki 骨架（wiki/ 目录 + README + 伪问题清单 + CLAUDE.md V0.2 路由规则）
- [ ] Phase 2A: schema 枚举业务含义审核（已生成给吕经理的审核请求文档，待回收）
- [x] Phase 2B: 核心业务主题 Wiki 页面（采购数据流/销售数据流/物料分类/生产数据流/应收应付/资产台账/采购成本分析 共 7 页已建）
- [ ] Phase 3: 集成验证（V0.2 三层联动） — 需 Phase 2A 回收后做 Q013 端到端
- [ ] Phase 4: 补全样本问题库答案 ✅ schema 已覆盖 32 张
- [ ] Phase 5: 知识沉淀机制（持续）
- [ ] Phase 6（可选）: Text2SQL 演进 ✅ ready（schema + relations + LLM 注解全到位）

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

### Session 2026-04-15（Phase 1 + Phase 2B 实施）
- Accomplished:
  - 创建 `源代码/mcp-kingdee-server/wiki/` 目录骨架（采购/销售/生产/库存/财务/固定资产/伪问题与数据缺口）
  - `wiki/README.md`：业务主题索引 + AI 检索决策树 + 职责分离表 + 知识沉淀回路
  - `wiki/伪问题与数据缺口/无法回答的问题清单.md`：分类录入 Q007/Q010/Q016/Q018/Q020/Q021/Q030/Q034/Q038/Q040/Q041/Q049-Q051
  - 7 个核心业务主题页：
    - 采购/采购订单数据流.md（PUR_Requisition → PurchaseOrder → ReceiveBill → InStock）
    - 采购/采购成本分析.md（铜箔基材物料确认 + 期货 MCP 联动）
    - 销售/销售订单数据流.md（含 Q013 公司"已审核 = 发票+收款"约定）
    - 库存/物料分类.md（靶材 vs 非靶材判断 + 单位换算陷阱）
    - 生产/生产订单数据流.md（标准路径 + 简单生产路径 + 线别字段）
    - 财务/应收应付.md（催收逻辑 + Q013 教训）
    - 固定资产/资产台账.md（骨架，待业务方补充）
  - 更新 `源代码/mcp-kingdee-server/CLAUDE.md`：
    - 问题回答指引 V0.2 — 6 步路由规则（list_cached_schemas → wiki/schema/relations 分流）
    - 写答案前必须步骤 V0.2 — kingdee_get_schema 替代 describe_form
    - 标注 `问题库回答指南.md` 已分流到 wiki/，仅作历史参考
- Key design decision applied:
  - Wiki 页**完全不写字段表**，全部引用 `kingdee_get_schema(form_id)`
  - 公司私有规则（"应收单已审核 = 发票+收款"、"靶材 vs 非靶材路径"、"单位换算 m² ↔ kg"）显式写入对应 wiki 主题页
  - 伪问题清单按业务原因分类（伪问题/数据缺口/线下数据/外部数据）
- Next steps:
  - 等吕经理回收 DEFAULT_ENUM_MAP 审核结果后，进入 Phase 3 集成验证（Q013 端到端）
  - Phase 4：补全样本问题库剩余答案（基于新的三层路由）
  - Phase 5：建立知识沉淀回路实操规范

### Session 2026-04-15（V0.3 设计对齐 — P20S 全量交付后）
- Context: 用户告知"P20S 的功能已经完全实现"，要求重新更新 P20T
- P20S 实际交付（核对自其 status.md / tasks.md）：
  - 全部 10 个 Phase 完成（Phase 7 BOS 待文件激活）
  - 32 张表 / 3647 字段（远超 MVP ≥20 目标）
  - 字段中文名覆盖率 **100%**（QueryBusinessInfo 官方通道已足够，未触发 LLM 兜底）
  - DEFAULT_ENUM_MAP 已固化金蝶通用枚举语义
  - 关联关系图 385 条边，新工具 `kingdee_get_relations()`
  - P23 回归桥实测 validity 58.3% → **100%**（+41.7%）
- Accomplished:
  - design.md Prerequisites 表全部更新为 ✅，列出实际工具签名和指标
  - 架构层增加 `kingdee_get_relations` 工具
  - 路由规则升级到 6 步：list_cached_schemas → wiki/schema/relations 分流 → query
  - Decision 4 重写：通用业务含义已在 schema (DEFAULT_ENUM_MAP)，wiki 只补**公司私有**部分（如 F_BDK_* 自定义字段、应收"已审核"业务约定）
  - tasks.md 重写 Phase 2A：从"补全枚举含义"改为"审核 DEFAULT_ENUM_MAP + 标注公司私有"
  - tasks.md Phase 2B 新增 2B.7 采购成本分析；Phase 4 新增 4.7（提请扩 FORM_CATALOG）
  - tasks.md Phase 6 entry criteria 全部满足，可探索 Vanna/Text2SQL
  - status.md Overall 改为 "Ready to Execute"
- Key insight: P20S 中文名 100% + DEFAULT_ENUM_MAP + relations → Wiki 工作量比 V0.1 设计大幅缩小，Wiki 主要承载**公司私有业务规则**而非"金蝶字段说明"
- Next steps: 启动 Phase 1（Wiki 骨架）+ Phase 2B（业务主题页）+ Phase 2A（与吕经理审核）
- Blockers: 仅剩业务人员配合（吕经理审核 DEFAULT_ENUM_MAP 是否符合公司用法）

### Session 2026-04-15（V0.2 设计更新）
- Context: 用户提出"假定 P20S 全部完成现在就更新 P20T，可以吗"，确认采用此方式
- Accomplished:
  - design.md 加 Prerequisites 段，列出 P20S 依赖（已交付 ✅ / 进行中 ⏳ / 未启动 📋）
  - 架构升级为三层（Schema 层 / 业务语义层 / 执行层），职责分离
  - Wiki 页面格式重写：移除字段表，引用 schema 文件
  - 路由规则 V0.2：字段类问题走 kingdee_get_schema，不走 Wiki
  - 新增 Decision 6（不重复 schema）+ Decision 7（字段查询强制走工具）
  - tasks.md 重组：Phase 2 拆 2A/2B；每 Phase 标 entry criteria；新增 Phase 6 Text2SQL 演进
- Caveat:
  - **本次更新基于 P20S 的目标态接口契约，并行于 P20S 的实现 session**
  - 若 P20S 实际交付的接口形态/字段/工具签名与本规格假设有偏差，需回溯调整
  - 当前 P20S 状态：Phase 1+2+4+8 Done（10 张 MVP 表 + enum 原始扫描 + MCP 集成）
  - 待 P20S 收敛后做一次"实际接口 vs P20T Prerequisites 假设"的对账
- Next steps: 等 P20S Phase 3/5 完成后，回头校对 design 和 tasks 的细节
- Blockers:
  - P20S 进行中的 Phase 3（LLM 注解）和 Phase 5（关联关系）—— 非阻塞 Phase 1/2，但阻塞 Phase 6
  - 枚举值业务含义仍需吕经理配合（Phase 2A）

## Key Metrics（目标）

| 指标 | 当前 | 目标 |
|------|------|------|
| 已完成答案题数 | 10/52（19%） | 34/52（65%，可回答题全覆盖） |
| Q013 式错误复现 | 有 | 零 |
| Wiki 主题页面数 | 0 | 10+ |
| 伪问题显式标注 | 部分（问题库备注） | 全部（Wiki 清单） |
