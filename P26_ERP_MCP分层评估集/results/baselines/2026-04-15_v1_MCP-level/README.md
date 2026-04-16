# P26 基线快照 · 2026-04-15 · v1 MCP-level

> **不可变快照**。真实 MCP 工具链下的首份基线（对比 `2026-04-15_v1_LLM-level` 上限基线）。

## 快照身份

| 字段 | 值 |
|------|-----|
| baseline_id | `2026-04-15_v1_MCP-level` |
| 题集 | P26 V1 · 46 题 |
| 模型 | deepseek-chat, temperature=0 |
| 方法 | **真实 MCP-level** · `scorer/mcp_runner.py` · stdio 协议接 `src.server` |
| MAX_TURNS | 8（已达瓶颈，100% 题命中上限）|
| 耗时 | ~1h45m（T0+T1+T2 生成 + 6 路 judge + aggregate）|

## 五维整体均分

| 状态 | validity | hit_rate | L7_refusal | factual /5 | business /5 |
|------|----------|----------|------------|------------|-------------|
| T0（旧态） | 0.637 | 0.713 | 0.833 | 3.281 | 2.583 |
| T1（+P20S） | 0.529 | 0.545 | 0.500 | 1.344 | 2.833 |
| T2（+P20T） | 0.506 | 0.508 | 0.833 | 1.594 | 2.833 |
| Δ T0→T2 | -0.131 | -0.205 | 0 | -1.687 | **+0.250** |

## 核心发现

1. **LLM-level 模拟 overestimate**：LLM-level T1 validity 0.829 vs MCP-level T1 0.529，落差 0.300 是 P20E 整合损耗
2. **Turn budget 是瓶颈**：100% 题命中 MAX_TURNS=8，schema/wiki 工具被广泛调用（96%/85%）但挤占了 query 的 turns
3. **唯一干净正增益**：business_grounding T0→T2 **+0.250**（L6 +0.428），wiki 对业务判断有效
4. **T2 灾难**：L8 多步分析 factual 从 2.750 → 0.000（wiki 被 LLM 误用作逃避"伪问题"的借口）

详细分析见 `../../MCP_level_full_run_report.md`。

## 下次重跑的比较目标

P0 修复后（MAX_TURNS↑ + 工具幂等性 prompt + wiki 伪问题约束）应观察：
- factual T1 ≥ 2.5（从 1.344 回升）
- L8 T2 factual ≥ 2.0（从 0 回升）
- validity T2 ≥ 0.75（从 0.506 回升）

命中任一目标即冻结新快照 `YYYY-MM-DD_v2_MCP-level/`。

## 文件清单

```
2026-04-15_v1_MCP-level/
├── README.md
├── SCORECARD.json
├── comparison.md (= comparison_mcp.md)
├── T0/  answers + 4 json
├── T1/
└── T2/
```
