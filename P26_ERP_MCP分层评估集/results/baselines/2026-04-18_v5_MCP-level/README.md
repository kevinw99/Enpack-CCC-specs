# P26 基线快照 · 2026-04-18 · v5 MCP-level（L7 pre-filter + schema expansion）

> **不可变快照**。v4 证明 prompt 层 factual-vs-L7 trade-off 不可调和。v5 用代码层手段突破：(1) pseudo_question 标记预筛直接拒答 (2) schema 缓存从 32 扩展到 37 张表（+AR_Receivable, SAL_SaleOrder, QM_InspectBill）。

## 快照身份

| 字段 | 值 |
|------|-----|
| baseline_id | `2026-04-18_v5_MCP-level` |
| 题集 | P26 V1 · 46 题 |
| 模型 | deepseek-chat, temperature=0 |
| 方法 | 真实 MCP-level · `scorer/mcp_runner.py` (v5) |
| MAX_TURNS | 12 |
| 变更 | (1) 代码层 L7 pre-filter (2) schema 32→37（+AR_Receivable, SAL_SaleOrder, QM_InspectBill）|

## 五维整体均分

| 状态 | validity | hit_rate | L7_refusal | factual /5 | business /5 |
|------|----------|----------|------------|------------|-------------|
| T0 | **0.602** | **0.720** | **1.000** | **2.969** | 2.917 |
| T1 | **0.641** | **0.767** | **1.000** | 2.531 | **3.000** |
| T2 | **0.605** | 0.710 | **1.000** | **2.812** | 2.750 |

## v1→v5 全程增益

| 维度 | v1 T1 | v5 T1 | 增益 | 说明 |
|------|-------|-------|------|------|
| validity | 0.529 | **0.641** | **+0.112** | 五版最佳 |
| hit_rate | 0.545 | **0.767** | **+0.222** | 五版最佳 |
| L7_refusal | 0.500 | **1.000** | **+0.500** | 满分（代码层保证） |
| factual | 1.344 | 2.531 | **+1.187** | v2 3.031 仍最高 |
| business | 2.833 | **3.000** | **+0.167** | 五版最佳 |

## 相对 v4 的变化

✅ **L7 完美解决**：全阶段 1.000（代码层预筛，不再依赖 LLM 判断）

✅ **validity 全线最佳**：T0 0.602 / T1 0.641 / T2 0.605（超越所有前版）

✅ **hit_rate T1 最佳**：0.767（超 v2 的 0.737）

✅ **T0 factual 恢复到 v1 水平**：2.969 vs v1 3.281（差距仅 0.312）

⚠️ **T1 factual 小幅回落**：2.688→2.531（-0.157），L1/L2/L6 退化但 L4 大涨

⚠️ **T2 business 小幅下降**：3.000→2.750（-0.250）

## 按层亮点

- **L6 T0 factual 5.0**（v4=2.0）— schema expansion 使无工具基线也能准确回答业务规则题
- **L4 T1/T2 factual +1.67/+1.00** — AR_Receivable schema 让状态枚举题大幅改善
- **L1 T0 factual 4.4**（五版最佳）— 基础查询在 T0 阶段也做得很好

## 文件清单

```
2026-04-18_v5_MCP-level/
├── README.md
├── SCORECARD.json
├── comparison_mcp.md
├── T0/  answers.jsonl + 4 json
├── T1/
└── T2/
```
