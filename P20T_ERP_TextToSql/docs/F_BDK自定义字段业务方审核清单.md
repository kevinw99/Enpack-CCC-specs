# F_BDK_* 自定义字段业务方审核清单

> 致业务方：以下为公司在金蝶云星空中自定义的字段（以 `F_BDK_` 前缀标识）。虽然 schema 抽取已获取字段中文名，但**字段的实际业务语义、使用场景、取值范围**只有业务方能确认。请按表格逐项审核，重点是**标 ⚠️ 的字段**（字段名含糊或业务含义可能变化）。
>
> 审核后将结果回给 AI 团队，用于完善 `wiki/{主题}/` 的"公司私有字段"段（参考 `wiki/知识沉淀规范.md`）。
>
> 完成日期目标：本批次 ~90 个字段分布在 12 个表，建议按表分批审核（每次 1 个表，半小时）。

## 审核方法

对每个字段，请回答：
1. **字段含义**：schema 抽出的中文名是否准确？如不准确，实际含义是？
2. **取值范围**：典型取值 / 是否有枚举清单？
3. **使用场景**：什么业务场景下会填写 / 变更？
4. **业务规则**：有无特殊规则（如"必填"、"某条件下不能为空"、"跨表传递"）？
5. **已废弃？** 若不再使用请明确标注。

## 按表审核

### 1. AP_Payable（应付单）— 7 字段

| 字段 | 抽取中文名 | 关联 | 审核重点 |
|------|-----------|------|----------|
| F_BDK_invoice | 发票号 | — | ⚠️ 与标准 FInvoiceNumber 的差异？ |
| F_BDK_SGRK_YWLX | 采购入库业务类型 | (枚举) | ⚠️ 枚举取值？催收/对账关联？ |
| F_BDK_XTGLID | 下推关联编号 | — | |
| F_BDK_XTLY | 系统来源 | — | 哪些来源值？OA/手工/API？ |
| F_BDK_FPLX | 发票类型 | — | 枚举取值？ |
| F_BDK_GCXM | 在建工程 | BOS_ASSISTANTDATA_SELECT | |
| F_BDK_GDZC | 固定资产 | FA_CARDVIEW | |

### 2. BD_Material（物料）— 6 字段

| 字段 | 抽取中文名 | 关联 | 审核重点 |
|------|-----------|------|----------|
| F_BDK_FK | 幅宽 | — | ⚠️ 单位（mm/m）？靶材/非靶材规则不同？ |
| F_BDK_PP | 品牌 | — | |
| F_BDK_BPRemark | 备品用途 | — | |
| F_BDK_CSXX | 厂商信息 | — | 与 FSupplierId 的差异？ |
| F_BDK_Base | 上道工序物料编码 | BD_MATERIAL | ⚠️ 用于 BOM 工序链；关键字段 |
| F_BDK_OADateTime | OA判断日期 | — | OA 同步时间戳？ |

### 3. BD_Supplier（供应商）— 4 字段

| 字段 | 抽取中文名 | 关联 | 审核重点 |
|------|-----------|------|----------|
| F_BDK_LXR | 联系人 | — | 与 FContact 差异？ |
| F_BDK_LXDH | 联系电话 | — | |
| F_BDK_ZZSDate | 转正式日期 | — | ⚠️ 供应商从"潜在→正式"的业务流？ |
| F_BDK_GYSState | 供应商状态 | — | ⚠️ 枚举取值？与 FForbidStatus 的差异？ |

### 4. ENG_BOM — 2 字段

| 字段 | 抽取中文名 | 关联 | 审核重点 |
|------|-----------|------|----------|
| F_BDK_DEPTID | 设备 | BD_Department | ⚠️ "设备"为何指向 BD_Department？公司是否把设备建在部门表里？ |
| F_BDK_XB_ENTRY | 线别 | (枚举) | ⚠️ 线别枚举清单？产能/排产的关键维度 |

### 5. PRD_MO（生产订单）— 33 字段（**重点审核表**）

**工序计划/实际量**（溅射/水镀/分切三工序）—— 请确认工序命名与用量单位：

| 字段 | 抽取中文名 |
|------|-----------|
| F_BDK_SPUINPUTQTY / F_BDK_SPUOUTPUTQTY / F_BDK_SPUACTINPUTQTY / F_BDK_SPUACTOUTPUTQTY | 溅射 计划/实际 投入/产出 |
| F_BDK_WAPLINPUTQTY / F_BDK_WAPLOUTPUTQTY / F_BDK_WAACTINPUTQTY / F_BDK_WAACTOUTPUTQTY | 水镀 计划/实际 投入/产出 |
| F_BDK_CUTPLINPUTQTY / F_BDK_CUTPLOUTPUTQTY / F_BDK_CUTACTINPUTQTY / F_BDK_CUTACTOUTPUTQTY | 分切 计划/实际 投入/产出 |
| F_BDK_JSSYqty / F_BDK_SDSYqty / F_BDK_FQSYQTY | 溅射/水镀/分切 剩余数量 |

- ⚠️ 单位统一吗？（m² / kg / 片？）
- ⚠️ "剩余数量" = 计划 - 实际投入，还是工序级在制品？

**其他 PRD_MO 字段**：

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_Remarks | 工单性质说明 | |
| F_BDK_Combo | 研发立项项目 | ⚠️ 与 F_BDK_LXXM 的差异？ |
| F_BDK_DJLX / F_BDK_billtype | 生产订单单据类型 / 单据类型 | ⚠️ 两个字段职责差异？ |
| F_BDK_LXXM | 立项项目 | |
| F_BDK_ZDSB / F_BDK_ZDXB | 指定设备（→BD_Department）/ 指定线别 | ⚠️ 排产关键字段 |
| F_BDK_ZSH / F_BDK_DDJY | 总损耗 / 订单结余(减损耗) | ⚠️ 计算公式？ |
| F_BDK_TOTALOUTPUT / F_BDK_SURLUS / F_BDK_SDGX_WZSL | 上道工序累计产出 / 工序结余 / 上道工序未转数量 | ⚠️ 公式？工序链依赖关系 |
| F_BDK_BLSL / F_BDK_RETURNQTY / F_BDK_QTCKqty / F_BDK_CHSL | 补料 / 退料 / 其他出库 / 超耗数量 | ⚠️ 用于损耗分析 |
| F_BDK_SCCJBILL | 生产车间编号 | |

### 6. PRD_PPBOM（生产用料清单）— 6 字段

与 PRD_MO 重叠：F_BDK_ZDSB / F_BDK_ZDXB / F_BDK_DJLX / F_BDK_LXXM / F_BDK_DEPTID / F_BDK_XB_ENTRY

⚠️ 这些字段在 MO 和 PPBOM 中的含义是否完全一致？（通常 PPBOM 为 MO 的分录继承）

### 7. PUR_PurchaseOrder（采购订单）— 6 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_Remarks | 备注 | |
| F_BDK_Text | 申购单号 | ⚠️ 为什么不用标准 FSourceBillNo？ |
| F_BDK_SFYF | 是否预付 | 枚举（是/否）？ |
| F_BDK_MBBZJC | 套打备注是否加长 | 打印相关，可忽略 |
| F_BDK_YSYQ | 验收要求 | |
| F_BDK_QRJQ | 确认交期 | ⚠️ 与 FDeliveryDate 差异？Q009 到货及时性会用 |

### 8. PUR_ReceiveBill（收料通知单）— 1 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_Date | 预定到货日期（调整后） | ⚠️ 与 PO 的 FDeliveryDate 关系？Q009 及时性分析需要 |

### 9. PUR_Requisition（采购申请单）— 3 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_Text | 物料分类 | ⚠️ 枚举？ |
| F_BDK_OASQR | OA申请人 | ⚠️ 与标准 FApplicantId 差异？OA 集成 |
| F_BDK_JYYQ | 检验要求 | |

### 10. SAL_OUTSTOCK（销售出库单）— 5 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_FKDecimal | 幅宽小数（作废） | ⚠️ 已作废确认 |
| F_BDK_FKFZ | FK辅助（作废） | ⚠️ 已作废确认 |
| F_BDK_length | 长度(m) | ⚠️ 靶材/卷材出货专用？ |
| F_BDK_weight | 重量(kg) | ⚠️ 长度 × 重量是否用于单位换算（m² ↔ kg）？ |
| F_BDK_KHYQ | 客户要求 | |

### 11. STK_MisDelivery（杂项出库）— 11 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_CKLX | 出库类型 | ⚠️ 枚举清单？区分生产领料/其他出库 |
| F_BDK_YDJLXBM | 源单据类型编码 | |
| F_BDK_CHRK | 不良品 | |
| F_BDK_RKBILLNO | 入库单号 | 反向关联 |
| F_BDK_SCDD / F_BDK_SCDDseq / F_BDK_SCDDCPBM / F_BDK_Integer / F_BDK_Integer1 | 生产订单相关 5 字段 | ⚠️ 冗余设计是否用于性能？或是简单生产领料单的替代？ |
| F_BDK_ZCB | 制程别 | |
| F_BDK_XB | 线别 | |

### 12. STK_TransferDirect（直接调拨单）— 2 字段

| 字段 | 抽取中文名 | 审核重点 |
|------|-----------|----------|
| F_BDK_Assistant | 调拨类型 | ⚠️ 枚举？ |
| F_BDK_Base | 收料人 | 关联 BD_Empinfo |

## 回填规则

- 每张表的"公司私有字段语义"沉淀到对应 `wiki/{主题}/{数据流}.md` 的新增段落
- 已废弃字段在 schema 层面建议过滤（提 P20S 维护方）
- 枚举字段的实际值清单可按 `python3 -m schema_extractor --forms {form_id} --enums --enum-limit 500` 扫描补全
- 审核过程中如发现 AI 对字段理解的错误回答，记入 `wiki/{主题}/` 的"已知陷阱 ⚠️"段

## 审核统计（填写用）

- [ ] AP_Payable（7）
- [ ] BD_Material（6）
- [ ] BD_Supplier（4）
- [ ] ENG_BOM（2）
- [ ] PRD_MO（33）
- [ ] PRD_PPBOM（6）
- [ ] PUR_PurchaseOrder（6）
- [ ] PUR_ReceiveBill（1）
- [ ] PUR_Requisition（3）
- [ ] SAL_OUTSTOCK（5）
- [ ] STK_MisDelivery（11）
- [ ] STK_TransferDirect（2）

**共计 ~86 个 F_BDK_* 字段，分布在 12 张表。**
