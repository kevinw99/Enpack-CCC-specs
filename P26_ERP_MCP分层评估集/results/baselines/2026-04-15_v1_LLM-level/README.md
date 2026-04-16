# P26 基线快照 · 2026-04-15 · v1 LLM-level

> **不可变快照**。目录一旦落盘，**不要覆盖**。未来跑评估时应 diff 本快照，而不是改它。
> 若修复了评分器 bug / 换题集，须开新快照目录（e.g. `2026-05-01_v2_LLM-level` 或 `2026-05-01_v1_MCP-level`）。

## 快照身份

| 字段 | 值 |
|------|-----|
| baseline_id | `2026-04-15_v1_LLM-level` |
| 题集 | P26 V1 · 46 题 (`questions/_all.json`, commit 见 git log) |
| 模型 | deepseek-chat, temperature=0 |
| 方法 | **LLM-level 模拟**（schema 直接注入 prompt，未经 MCP 工具）|
| scorer 版本 | F_BDK_* 正则 + refusal gating + LLM-as-Judge (factual+business) |

## 四维整体均分

| 状态 | validity | hit_rate | L7_refusal | factual /5 | business /5 |
|------|----------|----------|------------|------------|-------------|
| T0 (无 schema) | 0.493 | 0.471 | 0.833 | 3.656 | 2.833 |
| T1 (+P20S schema) | **0.829** | **0.577** | 0.833 | 3.531 | 2.667 |
| Δ T0→T1 | **+0.336** | **+0.106** | 0 | -0.125 | -0.166 |

分层明细见 `SCORECARD.json`（机器可读）与 `comparison.md`（报告）。

## 未来如何使用本基线

**场景 1：P20S 代码改了（比如 schema 抽取优化），重跑 P26 LLM-level**
```bash
# 1. 在工作目录重跑（会覆盖 results/T0 results/T1）
bash scorer/run_all.sh   # WITH_JUDGE=1 跑四维

# 2. diff 本基线
python3 -c "
import json
old = json.load(open('results/baselines/2026-04-15_v1_LLM-level/SCORECARD.json'))
new_t1 = json.load(open('results/T1/validity.json'))['summary']
print('validity T1:', old['states']['T1']['overall']['validity_rate'], '→', new_t1['validity_overall_mean'])
"
```
若新数 < 旧数 → 回归；若显著上升 → 写新快照并记录原因。

**场景 2：跑真实 MCP-level T1（P23 harness + P20E/P20S/P20T）**
- 不要改本快照；新建 `2026-MM-DD_v1_MCP-level/`
- 差距 = MCP 整合损耗，见 `P23_harness_patch_plan.md` "验证项"

**场景 3：T2（P20T wiki 注入）完成**
- 新建 `2026-MM-DD_v1_LLM-level-T2/`，包含 T0/T1/T2 三状态
- 关键观测：L7_refusal 能否从 0.833 → ≥0.95；business L6 能否从 2.429 → ≥4.0

## 已知注意事项（不要在本基线上调）

1. **hint 错漏 22 条**（见 `../../hint_validation.json`）— 会轻微压低 L2/L3 hit_rate，但不影响跨版本可比性（只要后续快照用同一题集）
2. **T1 factual/business 轻微下降**（-0.125/-0.166）— 非 bug，详见 `../../T0_T1_baseline_report.md` "关于 factual/business 微降" 一节
3. **LLM-level 天花板**：本快照是**上限**，真实 MCP-level T1 只会 ≤ 本快照

## 文件清单

```
2026-04-15_v1_LLM-level/
├── README.md              ← 你在读
├── SCORECARD.json         ← 机器可读四维 + 分层均分
├── comparison.md          ← 生成时的对比报告
├── T0/                    ← 原始产出（answers + 四维 json）
└── T1/
```
