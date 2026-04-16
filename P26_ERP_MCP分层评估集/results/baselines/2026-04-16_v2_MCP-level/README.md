# P26 基线快照 · 2026-04-16 · v2 MCP-level（P0 修复后）

> **不可变快照**。v1 的首轮实测发现 turn-budget 瓶颈 + wiki 误用，P0 修复后重跑。

## 快照身份

| 字段 | 值 |
|------|-----|
| baseline_id | `2026-04-16_v2_MCP-level` |
| 题集 | P26 V1 · 46 题 |
| 模型 | deepseek-chat, temperature=0 |
| 方法 | 真实 MCP-level · `scorer/mcp_runner.py` (P0 修复后) |
| MAX_TURNS | **12**（v1=8）|
| Prompt 变更 | 幂等性+抗伪问题误判+cache miss fallback（见 git commit `5276459`）|
| 耗时 | 2h08m |

## 五维整体均分

| 状态 | validity | hit_rate | L7_refusal | factual /5 | business /5 |
|------|----------|----------|------------|------------|-------------|
| T0 | 0.507 | 0.662 | 0.500 | 2.719 | 2.667 |
| T1 | 0.526 | **0.737** | 0.167 | **3.031** | 2.917 |
| T2 | 0.532 | 0.663 | 0.500 | 2.688 | 2.833 |

## 相对 v1 MCP-level 的改进

✅ factual T1 **1.344 → 3.031 (+1.687)** · 翻倍达成
✅ factual T2 **1.594 → 2.688 (+1.094)** · L4/L6/L8 三大灾难全部修复
✅ hit_rate T1 **0.545 → 0.737 (+0.192)**
⚠️ L7 refusal 全线 **-0.333** · v3 待修的新回归

详见 `../../iteration_report.md` 第 4 节。

## 停止条件

- 自动迭代规则 A 触发：factual T1 ≥ 2.5 → 本次停止，等用户复核
- v3 已有窄修建议（伪问题正面清单）待审批

## 文件清单

```
2026-04-16_v2_MCP-level/
├── README.md
├── SCORECARD.json
├── comparison.md (= comparison_mcp.md)
├── T0/  answers + 4 json
├── T1/
└── T2/
```
