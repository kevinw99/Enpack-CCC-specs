# Phase 6: Vanna/Text2SQL 可行性评估

> P20S 全量交付后，Vanna/Text2SQL 路径的历史障碍（DDL 缺失）已消除。本文评估是否值得引入。

## P20S 交付后的新前提

| 关键前提 | 以前状态 | 现在状态 |
|---------|---------|---------|
| 完整 DDL/schema | ❌ 无 | ✅ 32 张表 / 3647 字段 / 100% 中文名 |
| 枚举值清单 | ❌ 不全 | ✅ 4 个状态字段全覆盖 + DEFAULT_ENUM_MAP 通用语义 |
| 表关联图 | ❌ 无 | ✅ 385 条 relation 边（Mermaid） |
| 业务语义层 | ❌ 无 | ✅ wiki/（公司特殊约定 + 业务流程） |

Vanna 框架对"schema + examples"有强依赖。上述前提全部到位后，切入成本明显下降。

## Vanna 的典型工作机制（回顾）

```
用户问题
    ↓
Vanna 框架（RAG + LLM）
    ├── 检索 schema（DDL）
    ├── 检索业务文档
    ├── 检索历史 Q&A 对
    ↓
生成 SQL
    ↓
执行 SQL，返回数据
```

**关键障碍**：金蝶云星空**不允许直接 SQL**（REST API 封装）。

## 可行性分析

### 方案 A: 标准 Vanna + 真 SQL（不可行）
- 金蝶 API 不开放 SQL，除非申请只读 DB 账号
- 即使拿到 DB 账号，SQL 仍需绕过金蝶本身的视图/权限封装
- **结论**：短期不可行

### 方案 B: Vanna 思路 + MCP query DSL（可行，推荐）
- 不生成 SQL，改生成**金蝶 `QueryBillsData` 的参数包**：
  ```json
  {
    "FormId": "AR_Receivable",
    "FieldKeys": ["FID,FCustomerId,FDocumentStatus,FAllAmountFor,FEndDate_H"],
    "FilterString": "FDocumentStatus='B' AND FCancelStatus='A' AND FEndDate_H<?"
  }
  ```
- 训练数据：已有 10 个 `answer/q*.md` 问题-答案对 + schema + wiki
- 输出：直接喂给 `kingdee_query` MCP 工具
- **结论**：可行；本质是"query-DSL 生成器"

### 方案 C: 直接增强 LLM 的 tool-use（已经在做的路径）
- 当前就是这个：LLM 拿 schema + wiki，决定调哪个工具
- 优点：轻量、已有基础
- 缺点：每次要把 schema 塞进上下文，随表数增长会碰到 context 上限
- **结论**：近期主推；Vanna 作为"上下文压缩 + 样本学习"的增强层

## PoC 设计（方案 B）

### 测试题（5 个已有 ground truth）

| 题目 | 难度 | Ground truth |
|------|------|-------------|
| Q001 采购审批合理性 | 中（多表 JOIN） | `answer/q001_answer.md` |
| Q006 铜箔基材采购趋势 | 中（物料确认+时间聚合） | `answer/q006_answer.md` |
| Q009 采购到货及时性 | 中（交货日期 vs 入库日期） | `answer/q009_answer.md` |
| Q013 应收账款催收 | 高（需用 wiki 里的公司特殊约定） | `answer/q013_answer.md` |
| Q022 PET 薄膜消耗 | 高（BOM 拆解 + 靶材路径判断） | 部分有 |

### 评估指标

- **字段有效率**（与 P20S regression 对齐）：生成的 FieldKeys 是否都在 schema 中存在
- **过滤正确率**：FilterString 的字段/枚举值是否符合业务约定（特别是 Q013 要选 B 而非 C）
- **数据一致率**：生成的 query 实际执行结果 vs 手写答案
- **人工干预次数**：从问题到正确答案需几轮修正

### 对比基准

- **Baseline**: 当前 CLAUDE.md V0.2 三层路由（schema + wiki + tool-use）
- **Vanna-style**: schema + wiki + Vanna-like RAG + query DSL 生成

## 决策建议

### 短期（3 个月内）
- **不引入 Vanna**
- 继续用三层路由 + tool-use
- 理由：当前 32 张表 / 问题规模（52 题），轻量方案足够
- 待验证：答题准确率是否能达到 80%+（见 Phase 4 补全后回测）

### 中期（若问题规模扩大）
- 若表数扩至 100+，上下文不够
- 若问题数扩至 200+，样本学习价值凸显
- 此时评估 Vanna 方案 B（query DSL 生成器）

### 长期
- 若公司有数据仓库（Hive/Doris 等）同步金蝶数据
- 方案 A（真 SQL）变可行，Vanna 价值最大化

## 开发成本估算（方案 B）

| 组件 | 工作量 | 备注 |
|-----|-------|------|
| 训练集构建（schema + wiki + answer 转为 Vanna 训练格式） | 1 周 | 已有素材，只需转换 |
| 向量检索器（可用本地 embedding） | 3 天 | 避免外部依赖 |
| query DSL 生成器（LLM 模板 + 后处理） | 1 周 | 关键验证点 |
| 与 MCP `kingdee_query` 集成 | 2 天 | 较简单 |
| 评估脚本（复用 P20S `regression.py`） | 3 天 | 改写 case 定义 |
| **合计** | **3-4 周** | 全职一人 |

## 风险

| 风险 | 缓解 |
|-----|-----|
| LLM 生成 QueryDSL 容易漏字段/错字段 | 后处理校验 + schema 对照 |
| 公司特殊业务约定难以 RAG 检索命中 | wiki 做结构化索引，关键词触发强制读 |
| 向量检索噪声大 | 分类问题后只检索对应主题 wiki（路由在前 + RAG 在后） |

## 建议下一步

- [ ] 等 Phase 4 补全至 30+ 题后，用基线方案做一次端到端评估
- [ ] 若基线 > 80% 准确率 → 维持现状，不上 Vanna
- [ ] 若基线 < 70% → 启动 Vanna PoC
- [ ] 任何情况下：持续沉淀业务规则到 wiki，这是两种方案共同的基础
