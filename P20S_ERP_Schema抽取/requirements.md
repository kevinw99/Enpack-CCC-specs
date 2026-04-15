# Requirements: P20S ERP Schema 抽取（金蝶 DB 元数据获取）

## Overview

构建一套自动化机制，从金蝶云星空系统抽取表和字段的 **DDL + 业务描述**（中文名、含义、
枚举值、关联关系），输出为结构化的 Schema 知识库，为下游的 P20T_TextToSql 和
P20E_ERP_MCP服务 提供权威的元数据底座。

## Business Context

- P20E 现有 `kingdee_describe_form` 工具返回 65KB 全量字段，上下文消耗大（技术债 T1）
- P20E `问题库回答指南.md` 中的字段映射、状态值枚举完全靠人工维护（技术债 T2）
- AI 在字段选择上不稳定（如 Q013 反复修正 3 次），根因是缺乏结构化的字段语义
- P20T_TextToSql 方向要求有完整 schema 标注才能跑通
- 金蝶 ERP 有几百张表，人工标注工作量巨大，必须有自动化抽取

## Functional Requirements

### F1: 元数据抽取（主通道）

- F1.1 从金蝶 `T_META_*` 系列元数据表读取：
  - `T_META_OBJECTTYPE` — 业务对象定义
  - `T_META_TABLE` — 表定义
  - `T_META_FIELD` — 字段定义（含 `FFIELDNAME_L2` 中文名）
  - 相关关联表（枚举值、外键关系）
- F1.2 支持按模块（采购/库存/财务/基础资料）分批抽取
- F1.3 输出标准化 JSON/Markdown schema 清单

### F2: BOS 设计器导出（补充通道）

- F2.1 支持导入 BOS 设计器导出的业务对象元数据文件
- F2.2 合并 BOS 元数据与 T_META_* 数据（BOS 优先，T_META 兜底）

### F3: LLM 辅助注解（兜底通道）

- F3.1 针对元数据缺失或中文描述不清的字段，用 LLM 基于命名规则反推
- F3.2 利用表前缀规则（`T_BD_*` 基础 / `T_SAL_*` 销售 / `T_PUR_*` 采购 /
  `T_IM_*` 库存 / `T_AP_*` 应付 / `T_AR_*` 应收 / `T_GL_*` 总账）
- F3.3 利用字段前缀规则（`FNumber` 编码 / `FName` 名称 / `FDate` 日期 / `FAmount` 金额）
- F3.4 LLM 生成的注解需标注"⚠️ AI 推断"，与官方元数据区分
- F3.5 支持少量真实数据样本作为 LLM 推断的额外上下文

### F4: 枚举值/状态值提取

- F4.1 识别状态字段（如 `FStatus`, `FApproveStatus`, `FDocumentStatus`）
- F4.2 从元数据表或真实数据中提取所有出现过的枚举值
- F4.3 业务人员补充每个枚举值的业务含义（人工回路）

### F5: 关联关系抽取

- F5.1 从元数据识别外键字段（`F*Id` 命名约定）
- F5.2 生成表间 JOIN 路径图谱
- F5.3 标注主数据 vs 业务单据的关联

### F6: 输出格式

- F6.1 每个表一个 `schema/{form_id}.md` 文件（人类可读）
- F6.2 汇总 JSON：`schema/index.json`（程序读取）
- F6.3 向量化索引（可选）：供 P20T Text2SQL RAG 检索

## Non-Functional Requirements

- **认证**: 复用 P20E 的金蝶 API 凭证
- **运行位置**: 独立脚本（CLI），产出物存入版本控制
- **增量更新**: 支持检测元数据变更，只更新变化的表
- **数据隔离**: 不记录任何业务数据，只记录 schema 结构

## Success Criteria

- [ ] 覆盖 P20E 8 个工具涉及的核心表（物料、库存、采购申请、固定资产等）≥ 20 张
- [ ] 每张表包含：中文名、字段清单（中英文名+类型+含义）、枚举值、关联关系
- [ ] 枚举值覆盖率 ≥ 90%（至少字段名+出现过的值）
- [ ] 业务注解覆盖率 ≥ 80%（官方 + LLM 推断）
- [ ] Q013 式字段选择错误在有 schema 支持时不再复现（由 P23 评估）

## Out of Scope

- 业务规则/流程建模（由 P20T 处理）
- 多版本金蝶兼容（当前只支持在用的星空版本）
- 图形化 schema 浏览 UI

## Relationship to Other Specs

- **P20E_ERP_MCP服务**: 本规格产出物可替换/优化 P20E 的 `describe_form` 工具
- **P20T_TextToSql**: 本规格是 Text2SQL 的 schema 基础设施
- **P23_ERP_MCP问答质量评估**: 用 Q013 等案例验证本规格的价值
