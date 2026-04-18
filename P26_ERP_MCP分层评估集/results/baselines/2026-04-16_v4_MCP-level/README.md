# P26 基线快照 · 2026-04-16 · v4 MCP-level（stage-specific prompt + tool quota）

> **不可变快照**。v3 修复了 L7 但 T0 持续退化且 prompt 规则仍被 LLM 忽略。v4 做两项修复：(1) B/C 约束仅注入 T1/T2 prompt (2) search_forms_online 代码层硬限 2 次。

## 快照身份

| 字段 | 值 |
|------|-----|
| baseline_id | `2026-04-16_v4_MCP-level` |
| 题集 | P26 V1 · 46 题 |
| 模型 | deepseek-chat, temperature=0 |
| 方法 | 真实 MCP-level · `scorer/mcp_runner.py` (v4) |
| MAX_TURNS | 12（同 v2/v3）|
| 变更 | (1) build_system_prompt(stage) — B/C 仅 T1/T2 (2) TOOL_QUOTAS: search_forms_online ≤ 2 |
| 耗时 | ~3.5h（09:45 → 13:15）|

## 五维整体均分

| 状态 | validity | hit_rate | L7_refusal | factual /5 | business /5 |
|------|----------|----------|------------|------------|-------------|
| T0 | 0.519 | 0.680 | 0.500 | 2.500 | 2.833 |
| T1 | 0.516 | 0.704 | 0.500 | **2.688** | **2.917** |
| T2 | 0.532 | 0.684 | 0.500 | **2.688** | **3.000** |

## 相对 v3 的变化

| 维度 | v3 T0 | v4 T0 | Δ | v3 T1 | v4 T1 | Δ | v3 T2 | v4 T2 | Δ |
|------|-------|-------|---|-------|-------|---|-------|-------|---|
| factual | 2.250 | **2.500** | **+0.250** | 2.594 | **2.688** | **+0.094** | 2.531 | **2.688** | **+0.157** |
| business | 3.000 | 2.833 | -0.167 | 2.750 | **2.917** | **+0.167** | 2.833 | **3.000** | **+0.167** |
| hit_rate | 0.663 | 0.680 | +0.017 | 0.703 | 0.704 | +0.001 | 0.685 | 0.684 | -0.001 |
| L7_refusal | 0.500 | 0.500 | 0 | **0.667** | 0.500 | **-0.167** | **0.833** | 0.500 | **-0.333** |

### 核心判读

✅ **T0 factual 恢复**：2.250 → 2.500（+0.250），stage-specific prompt 生效，T0 不再被 B/C 约束拖累。

✅ **factual 全线提升**：三阶段均 2.5+，且 T1/T2 均回到 v2 水平（2.688）。

✅ **business T1/T2 提升**：T1 2.917（并列 v2 最佳）、T2 3.000（四版最佳）。search_forms_online 硬限回收了 turn budget，让 LLM 有更多轮做实际数据查询。

⚠️ **L7 回归重现**：T1 0.667→0.500、T2 0.833→0.500。L7-01 (T1) 和 L7-03/L7-06 (T2) 重新被 LLM 当作可查询题处理。这是 search_forms_online 硬限的间接后果 — LLM 不再因为搜索耗尽 turn 而"自动放弃"伪问题，反而有余力去尝试 query。

## 与 v2 的关系

v4 在 factual/business 上**回到 v2 水平**，但同样继承了 v2 的 L7 问题。这证实：factual 高分和 L7 高分之间存在 prompt 层面的结构性矛盾 — 推动 LLM 更积极查询（利 factual）必然减弱拒答意愿（害 L7）。

## v5 建议

L7 问题已第三次出现，仅靠 prompt 无法同时满足"积极查询"和"坚决拒答"的双向约束。后续选项：

1. **代码层拒答**：在 runner 中用关键词预筛 L7 类题目，直接返回拒答，不经 LLM
2. **few-shot 示例**：在 prompt 中加 2 个正反例，让 LLM 学会区分
3. **接受 trade-off**：L7 refusal 0.500 = 3/6 正确，作为 factual/business 全面达标的代价可能是合理的

## 文件清单

```
2026-04-16_v4_MCP-level/
├── README.md
├── SCORECARD.json
├── comparison_mcp.md
├── T0/  answers.jsonl + 4 json
├── T1/
└── T2/
```
