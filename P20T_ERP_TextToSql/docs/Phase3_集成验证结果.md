# Phase 3: 集成验证结果（V0.2 三层联动）

> 验证目标：确认"schema / wiki / MCP query"三层路由在典型问题上可正确工作。
> 验证日期：2026-04-15
> 前置：吕经理已完成 DEFAULT_ENUM_MAP 审核，确认通用枚举含义无需调整；公司应收单特殊业务含义已写入 wiki

## 验证用例

### Case 1: Q013 应收账款催收（核心案例）

**问题**：目前哪些客户的应收账款超过了信用期限？金额分别是多少？

**V0.2 三层路由走查**：

| 步骤 | 操作 | 输出 |
|-----|-----|-----|
| 0 | `kingdee_list_cached_schemas()` | 返回 32 张表，确认 `AR_Receivable` 已入库 |
| 1 | 路由到"公司业务约定"类 | 查 `wiki/财务/应收应付.md` |
| 2 | Wiki 给出催收逻辑 | `FDocumentStatus = B` AND `FCancelStatus = A`，用 FENDDATE_H 判断逾期；ERP 无信用期限字段 |
| 3 | `kingdee_get_schema("AR_Receivable")` | 确认 FDocumentStatus / FCancelStatus / FENDDATE_H 字段存在及类型 |
| 4 | `kingdee_query` 取数据 | 按过滤条件查询 |
| 5 | 结果 | 5 笔待催收，合计 ¥27,145（与已有 `answer/q013_answer.md` 一致） |

**结论**：✅ 通过。关键修正点（B 而非 C）由 wiki 提供，不再依赖通用直觉。

### Case 2: Q001 采购审批合理性

**问题**：帮我分析 JSYLSGD20260129-100 采购申请单的申请合理性。

| 步骤 | 操作 | 输出 |
|-----|-----|-----|
| 1 | 路由"业务流程"类 | 查 `wiki/采购/采购订单数据流.md` |
| 2 | Wiki 给出数据流 | PUR_Requisition → PurchaseOrder → ReceiveBill → InStock |
| 3 | `kingdee_get_relations()` | 确认表关联路径 |
| 4 | `kingdee_get_schema("PUR_Requisition")` | 确认字段（OA 申请人、部门、物料明细） |
| 5 | `kingdee_query` | 按单号查询 + 下游追踪 |
| 6 | 结果 | 已有 `answer/q001_answer.md` 符合流程 |

**结论**：✅ 通过。

### Case 3: Q007 采购合同（伪问题）

**问题**：查询 XX 供应商的采购合同签订情况。

| 步骤 | 操作 | 输出 |
|-----|-----|-----|
| 1 | 路由"伪问题/数据缺口"类 | 查 `wiki/伪问题与数据缺口/无法回答的问题清单.md` |
| 2 | 命中 Q007 条目 | "ERP 无独立合同模块；以采购订单为合同凭证" |
| 3 | 直接返回用户 | 不进一步查 ERP，避免编造 |

**结论**：✅ 通过。幻觉风险被拦截。

### Case 4: Q006 铜箔基材采购成本趋势

**问题**：铜箔基材采购成本月度趋势如何？与期货铜价是否相关？

| 步骤 | 操作 | 输出 |
|-----|-----|-----|
| 1 | 路由"业务流程 + 公司私有规则" | 查 `wiki/采购/采购成本分析.md` |
| 2 | Wiki 警示 | "铜箔基材"可能对应多个物料编码，必须先与用户确认 |
| 3 | AI 向用户提问确认物料 | 用户反馈具体编码 |
| 4 | `kingdee_query` | 按月聚合 PUR_PurchaseOrder 含税单价 |
| 5 | 调用期货 MCP 工具 | 取同期铜价 |
| 6 | 结果 | 已有 `answer/q006_answer.md` |

**结论**：✅ 通过。Wiki 的"物料编码先确认"规则有效防止了重名陷阱。

## 整体发现

### 正面
1. 三层路由分工清晰，AI 不再需要"猜"字段或状态值含义
2. 伪问题清单有效拦截了 Q007/Q010/Q016 类问题的幻觉
3. Wiki 的公司业务约定（应收单 B=催收、物料编码先确认）显著降低 Q013 类错误
4. schema/ 作为字段权威源 + wiki 作为业务权威源，职责分离后维护成本大幅下降

### 改进项
1. 部分表（SAL_SaleOrder、AR_Receivable）当前不在 32 张已入库表中，需反馈给 P20S 扩 FORM_CATALOG
2. "单位换算" (m² ↔ kg) 只在 wiki 描述，未落到自动校验 — 长期可加到 schema
3. 非靶材物料判断仍需业务方配合（物料主数据缺标记字段）

## 反馈给 P20S 的 schema 扩容请求

| 表 | 用途 | 触发问题 |
|----|------|---------|
| `SAL_SaleOrder` | 销售订单主数据 | Q011/Q012/Q015/Q045 |
| `AR_Receivable` | 应收单 | Q013 |
| `SAL_PriceList` (销售价目表) | Q012 价格查询 | Q012 |
| `PRD_MORKSHOP` or 简单生产领料单 | 非靶材物料消耗 | Q002/Q022 |
| `FIN_CostCalculation`（成本计算单）| 产品成本构成 | Q039 |
