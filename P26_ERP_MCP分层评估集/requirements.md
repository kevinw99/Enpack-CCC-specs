# Requirements: P26 ERP MCP 分层评估集

## Overview

设计一套**按 P20S/P20T 价值维度分层**的评估题集，让 P23 评估结果能**可归因地**反映 ERP MCP 能力演进。区别于 P23 当前使用的 28 题（按"是否依赖 ERP 数据"筛选），P26 按"**哪种能力缺失会让这题答错**"分层设计。

## Business Context

### 动机

P23 首轮评估用了 P19 标注的 28 个"B 类 ERP 依赖题"。这套题能回答"ERP MCP 能不能回答 ERP 问题"，但**不能回答**下面两个更关键的问题：

1. P20S 的字段抽取 / 关联关系 / 枚举语义，在多大程度上**消除了 Q013 式错误**？
2. P20T 的 LLM Wiki / Text2SQL，在多大程度上**覆盖了公司私有业务规则**？

原因：28 题没有按这些能力维度分层。如果 28 题里大多数是简单单表查询（模型不靠 P20S 也能答对），P20S 的增益就测不出来。

### 评估状态矩阵

P26 要支持对 ERP MCP 在以下三个集成状态的差异化评估：

| 状态 | 描述 | 测试对象 |
|-----|------|---------|
| T0 | P20E 原样（仅原 8 个工具 + 手工指南） | 基线（= P23 已跑结果） |
| T1 | P20E 整合 P20S（CLAUDE.md 改指引 + 3 新工具推荐使用） | P20S 增量 |
| T2 | P20E 整合 P20S + P20T Wiki / Text2SQL | P20T 增量 |

## Functional Requirements

### F1: 分层题集设计

- F1.1 按 **8 个价值维度**组织题目（L1-L8，定义见 design.md）
- F1.2 每层至少 3 题，总题数 40-55
- F1.3 每题标注：
  - 所属层（L1-L8）
  - 期望 P20S 增益（none / small / medium / large）
  - 期望 P20T 增益（none / small / medium / large）
  - 必需的表单（form_id 列表）
  - 必需的字段（key 列表，用于 validity 评分）
  - 参考答案要点（用于 LLM-as-Judge）

### F2: 分层指标

- F2.1 **field_validity_rate** — 答案中引用/查询的字段 key 是否真实存在于该 form 的 schema（P20S 直接指标，可自动评）
- F2.2 **factual_correctness** — 数据内容是否正确（LLM-as-Judge）
- F2.3 **business_grounding** — 业务判断是否符合公司规则（LLM-as-Judge，P20T 指标）
- F2.4 **refusal_correctness** — 对伪问题是否正确识别并给出"无法回答"的合理解释（L7 专用）
- F2.5 每层汇总指标（均值 + 分布）
- F2.6 整体加权分（权重可调）

### F3: 归因分析

- F3.1 T0→T1 delta 按层分解，归因到 P20S 的具体能力
- F3.2 T1→T2 delta 按层分解，归因到 P20T 的具体能力
- F3.3 反常信号识别（某层 T1 降了 → P20S 负作用；某层 T2 没升 → P20T 未覆盖）

### F4: 题目来源

- F4.1 从 P18 52 题中挑选符合分层标准的题
- F4.2 从 P20S 已有的 `regression_cases.json` 吸收 5 个初始用例
- F4.3 新增题目（L7 伪问题、L6 业务规则、L8 多步分析）
- F4.4 Q013 / Q019 / Q011 等已知难题必入 L2

## Non-Functional Requirements

- **可复用性**: 与 P23 的 harness（LLM-as-Judge + scorecards）兼容，只替换题集文件
- **可迭代性**: 每轮评估后可调整题集，版本化管理
- **成本可控**: 40-55 题 × 2 模型 × 2 评委 = 160-220 次 LLM 调用，单次评估成本 < ¥50
- **透明**: 每题的分类、期望增益、评分标准对业务方可见，便于审核

## Success Criteria

- [ ] 题集 V1 完稿并经业务方（吕经理）审核
- [ ] T0 基线跑通（可直接复用 P23 的现有结果 + 补充新题）
- [ ] T1（P20S 整合后）跑通，能**可归因地**展示 P20S 在 L2/L3/L5 的增益
- [ ] T2（P20T 整合后）跑通，能**可归因地**展示 P20T 在 L6/L7/L8 的增益
- [ ] 产出《ERP MCP 能力演进报告》，含 T0/T1/T2 三段对比

## Out of Scope

- 评估框架本身（归 P23 维护）
- 模型选型 / 评委选型（归 P23 维护）
- P20E 的代码改造（归 P20E）
- KB MCP 评估（归 P21）

## Relationship to Other Specs

- **P23_ERP_MCP问答质量评估**: 提供评估框架和 harness；P26 是对其题集维度的升级
- **P19_知识库缺口分析**: P26 的 B 类题来源之一；P26 更关注"为什么答错"而非"是否该由 ERP 回答"
- **P18_样本问题收集**: 题目选择池
- **P20S_ERP_Schema抽取**: 产出 schema / relations / enum，是 L2-L5 层的主要增益来源
- **P20T_ERP_TextToSql**: 产出 Wiki / Text2SQL，是 L6-L8 层的主要增益来源
- **P20E_ERP_MCP服务**: 被评估对象；整合层（T1/T2）需要其代码改动
