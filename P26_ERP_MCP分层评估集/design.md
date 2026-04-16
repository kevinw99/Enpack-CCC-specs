# Design: P26 ERP MCP 分层评估集

## 核心思路

**从"是否依赖 ERP 数据"转向"答错时该归因到哪个能力缺失"**。每题打上层标签，让增益可归因、可解释、可迭代。

## 8 个价值维度（L1-L8）

### L1 控制组 · 简单单表查询

- **描述**: 查询标准字段（如 FNumber/FName/FSpecification），单表，无状态过滤
- **典型题**: "列出所有物料的编码和名称"
- **期望 P20S 增益**: 无（LLM 已能答对）
- **期望 P20T 增益**: 无
- **价值**: 回归基线，防止新能力引入回退

### L2 字段幻觉敏感 · 复杂单据 + 非 canonical 字段

- **描述**: 复杂单据（字段数 > 100）或本公司用非标准字段名（如 `FApplicationDeptId` 而非 `FDeptID`）
- **典型题**: Q013（采购申请单本月已审核 + 申请部门 + 申请人），Q019 采购订单分析
- **期望 P20S 增益**: **大** — 直接解决字段幻觉
- **期望 P20T 增益**: 小
- **价值**: P20S 的核心战场

### L3 JOIN 敏感 · 跨 2+ 表关联

- **描述**: 需要关联 2 张以上表（物料+供应商+采购+库存）
- **典型题**: "本月每个供应商的采购订单总额，按部门拆分"
- **期望 P20S 增益**: **中** — `kingdee_get_relations` 提供 JOIN 路径
- **期望 P20T 增益**: 小
- **价值**: 验证 relations.md 的实际价值

### L4 状态枚举敏感 · FStatus/FDocumentStatus 语义

- **描述**: 需要正确理解金蝶状态值（A/B/C/D 分别代表什么）
- **典型题**: "哪些采购订单还没审核完", "本月禁用了几个物料"
- **期望 P20S 增益**: **中** — DEFAULT_ENUM_MAP 提供通用语义
- **期望 P20T 增益**: **中** — Wiki 补充公司私有理解（"已审核=可供货"）
- **价值**: P20S/P20T 交界战场

### L5 自定义字段敏感 · F_BDK_* / 客户化扩展

- **描述**: 本公司在标准字段之外有自定义字段（如 `F_BDK_LXR` 联系人）
- **典型题**: "查询所有供应商的联系人和电话"（标准字段 FContact 可能为空，实际数据在 F_BDK_LXR）
- **期望 P20S 增益**: **大** — schema 直接暴露自定义字段
- **期望 P20T 增益**: 中 — Wiki 说明哪个字段有效
- **价值**: 本公司部署特有的价值点

### L6 业务规则敏感 · 公司私有约定

- **描述**: 需要本公司的业务约定才能正确答题，纯 schema 不够
- **典型题**: "这个采购订单能不能发货？"（需知道"已审核 + 已下推" 才是可发货）
- **期望 P20S 增益**: 小
- **期望 P20T 增益**: **大** — Wiki 的主要阵地
- **价值**: P20T 的核心战场

### L7 伪问题识别 · 无 ERP 数据 / 线下数据 / 跨系统

- **描述**: 问题听起来像 ERP 能答，但实际数据不在 ERP 里（研发 BOM、线下 Excel、其他系统）
- **典型题**: L5 分类的 18 题，如"本月研发立项数"（无 ERP 对应）
- **期望 P20S 增益**: 无
- **期望 P20T 增益**: **大** — Wiki 明确标注"伪问题"并给出正确去向
- **价值**: 考验"拒答 + 引导"能力（答错比答"不知道"伤害更大）

### L8 多步分析 · 需要组合多次查询 + 推理

- **描述**: 需要先取 A 数据，用 A 的结果构造 B 查询，最后综合判断
- **典型题**: "最近 3 个月哪个供应商供货最不稳定"（需先查订单 → 按供应商聚合 → 算变异系数）
- **期望 P20S 增益**: **中** — schema 减少每步的字段错误累积
- **期望 P20T 增益**: **大** — Wiki 提供"异常供应商"定义和分析模板
- **价值**: 高阶能力展示

## 题集分布建议

| 层 | 题数 | 来源（建议） |
|----|------|-------------|
| L1 控制组 | 5 | P18 中最简单的基础资料题 |
| L2 字段幻觉 | 10 | Q013, Q019, 采购/销售复杂单据题，部分从 regression_cases.json |
| L3 JOIN | 6 | P18 中需要跨表的题（物料+库存+供应商组合） |
| L4 状态枚举 | 5 | P18 中含"已审核 / 未审核 / 禁用"关键词的题 |
| L5 自定义字段 | 3 | 供应商联系人、物料扩展属性、自定义 HR 字段 |
| L6 业务规则 | 7 | P18 中需要"判断是否…"的题，吕经理标注新题 |
| L7 伪问题 | 6 | P19 标注的 A 类（KB 空缺且 ERP 也无） |
| L8 多步分析 | 4 | 成本对标、供应商评分、库存周转率等 |
| **合计** | **46** | |

## 分层指标定义

### field_validity_rate（P20S 直接指标）

- 定义: 答案中所有引用/查询的字段 key，在该 form 的真实 schema 里存在的比例
- 实现: 对答案做 regex 抽取 `F[A-Z][A-Za-z_]*` → 去重 → 对每个 form 查 schema 清单做匹配
- 范围: 0-1
- 自动评（不需要 LLM judge），是 P20S 的**廉价先导指标**
- 重点观测层: L2, L5

### factual_correctness（传统正确性）

- 定义: 答案中的事实陈述（数字、名称、数量）是否与实际 ERP 数据一致
- 实现: LLM-as-Judge 0-5 分制
- 需要参考答案（业务方审核）
- 重点观测层: L1-L4

### business_grounding（P20T 指标）

- 定义: 答案的业务判断是否符合公司规则（如"是否可发货"、"是否正常采购"）
- 实现: LLM-as-Judge，需要 Wiki 内容作为参考
- 重点观测层: L6, L8

### refusal_correctness（L7 专用）

- 定义: 对伪问题是否明确回复"此数据不在 ERP 中"并指向正确来源
- 实现: LLM-as-Judge 二值（正确识别 / 错误尝试回答）
- 重点观测层: L7

## 归因方法

### T0 → T1 delta（P20S 增益）

```
对每层 L:
    delta_L = mean(T1_score[L]) - mean(T0_score[L])
    
P20S 归因:
    L2 delta: 直接归因 P20S schema + 字段幻觉消除
    L3 delta: 直接归因 P20S relations
    L4 delta: 部分归因 P20S enum
    L5 delta: 直接归因 P20S 客户化字段暴露
    L1/L6/L7/L8 delta: 预期接近 0，若显著非零需排查副作用
```

### T1 → T2 delta（P20T 增益）

```
对每层 L:
    delta_L = mean(T2_score[L]) - mean(T1_score[L])
    
P20T 归因:
    L4 delta 的业务部分: Wiki 补充公司私有理解
    L6 delta: 直接归因 P20T Wiki
    L7 delta: 直接归因 P20T 的伪问题清单
    L8 delta: 归因 P20T 的分析模板
    L1/L2/L3/L5 delta: 预期接近 0
```

### 反常信号

- T1 某层下降: P20S 可能引入误导（如 schema 噪音让 LLM 分心）
- T2 L6/L7 未升: Wiki 内容不足或 LLM 未查 Wiki
- T0 L2 很高: 题目太简单，未充分挑战 P20S
- T1 validity 不是 100%: P20S 工具未被 LLM 使用

## 题目格式（每题 JSON）

```json
{
  "id": "L2-01",
  "layer": "L2",
  "source": "P18-Q013",
  "question": "查询本月已审核的采购申请单...",
  "expected_p20s_gain": "large",
  "expected_p20t_gain": "small",
  "required_forms": ["PUR_Requisition"],
  "required_fields_hint": ["FBillNo", "FDate", "FDocumentStatus",
                           "FApplicationDeptId.FName", "FApplicantId.FName"],
  "reference_answer_points": [
    "使用 FApplicationDeptId 而非 FDeptId",
    "FDocumentStatus='C' 代表已审核",
    "本月过滤: FDate >= 本月1日"
  ],
  "pseudo_question": false,
  "expected_refusal": null,
  "scoring_dimensions": ["field_validity_rate", "factual_correctness"]
}
```

## 目录结构

```
P26_ERP_MCP分层评估集/
├── requirements.md
├── design.md（本文件）
├── tasks.md
├── status.md
└── questions/
    ├── L1_control.json
    ├── L2_field_hallucination.json
    ├── L3_join_sensitive.json
    ├── L4_enum_semantic.json
    ├── L5_custom_field.json
    ├── L6_business_rule.json
    ├── L7_pseudo.json
    ├── L8_multi_step.json
    └── _all.json（合并版，harness 直接消费）
```

## 与 P23 的集成

### 最小改动方式

P23 的 harness 保持不变，只是：
1. 替换题集文件输入路径
2. 每题传入 `layer` 元信息
3. scorer 新增 `field_validity_rate` 维度（无需 LLM，纯字段存在性检查）
4. 产出的 scorecard 按 layer 聚合

### 评估脚本入口（概念）

```bash
# P23 harness 复用，只换题集
python -m eval.harness \
    --questions 规格/P26_ERP_MCP分层评估集/questions/_all.json \
    --mcp-config erp_mcp_t1.json \
    --tag T1 \
    --out results/T1/
```

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 题集设计偏主观，分层标准不一致 | 每题双人审核（技术 + 业务方），分层标准写明判例 |
| 伪问题识别难 LLM-as-Judge 评 | 先用二值判断，评判标准写死"是否出现'不在 ERP 中'类措辞" |
| P20T Wiki 未完成 → T2 无法跑 | 先只跑 T0/T1，T2 可延后 |
| 业务方审核慢 | MVP 阶段先用 AI 初稿，后续业务方迭代 |
