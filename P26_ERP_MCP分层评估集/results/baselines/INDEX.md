# P26 基线快照索引

每次 P20S / P20T / P23 harness 有重大改动、或方法学调整后，冻结一份新基线到此目录。**旧快照永不覆盖**，只新增。

## 命名规范

`YYYY-MM-DD_vN_<level>[-<状态>]/`

- `level`: `LLM-level`（schema 直接注入 prompt）/ `MCP-level`（走 P23 harness + MCP 工具）
- 可选状态后缀：`-T2` 表示含 T2 (P20T wiki)

## 快照清单

| 快照 | 日期 | 类型 | 关键均分 (T1) | 说明 |
|------|------|------|----------------|------|
| [2026-04-15_v1_LLM-level](./2026-04-15_v1_LLM-level/) | 2026-04-15 | LLM-level 模拟 T0+T1 | validity 0.829 / factual 3.531 / business 2.667 | P26 V1 首个基线，P20S schema 直注 prompt（上限） |
| [2026-04-15_v1_MCP-level](./2026-04-15_v1_MCP-level/) | 2026-04-15 | **真实 MCP-level** T0+T1+T2 | validity 0.529 / factual 1.344 / business 2.833 | P26 V1 真实链路基线；揭示 turn budget 瓶颈、P20T wiki 误用 L8；**business +0.250 是唯一干净增益** |
| [2026-04-16_v2_MCP-level](./2026-04-16_v2_MCP-level/) | 2026-04-16 | MCP-level T0+T1+T2 · P0 修复后 | validity 0.526 / **factual 3.031** / business 2.917 / hit 0.737 | MAX_TURNS 8→12 + 幂等性+抗伪问题 prompt。factual T1 翻倍、L4/L6/L8 灾难修复；新回归：L7 refusal -0.333 全线 |
| [2026-04-16_v3_MCP-level](./2026-04-16_v3_MCP-level/) | 2026-04-16 | MCP-level T0+T1+T2 · L7 窄修 | validity 0.492 / factual 2.594 / business 2.750 / **L7 0.667** | 双向约束（正面拒答清单 A + 客观交易必须 query B）。L7 T1 0.167→0.667、T2 0.500→0.833 全线回归修复；factual T1 -0.437 但仍 ≥2.5 |
| [2026-04-16_v4_MCP-level](./2026-04-16_v4_MCP-level/) | 2026-04-16 | MCP-level T0+T1+T2 · stage prompt + tool quota | validity 0.516 / **factual 2.688** / **business 2.917** / hit 0.704 | B/C 约束仅 T1/T2 + search_forms_online 硬限 2 次。T0 factual +0.250 恢复；T1/T2 factual/business 回到 v2 水平；L7 再次 0.500（结构性矛盾确认）|
| [2026-04-18_v5_MCP-level](./2026-04-18_v5_MCP-level/) | 2026-04-18 | MCP-level T0+T1+T2 · **L7 pre-filter + schema 37** | **validity 0.641** / factual 2.531 / **business 3.000** / **hit 0.767** / **L7 1.000** | 代码层伪问题预筛（L7 满分）+ schema 32→37。validity/hit/L7/business 四项五版最佳；factual T1 2.531 轻微低于 v2 |
| [2026-04-19_v6_MCP-level](./2026-04-19_v6_MCP-level/) | 2026-04-19 | MCP-level T0+T1+T2 · **60题 + docstring** | **validity 0.751** / **factual 2.870** / business 2.316 / hit 0.752 / **L7 1.000** | 题集 46→60 + query_bills docstring 优化。**validity 六版最佳**（全层上升）；L1 factual 翻倍 4.14；T1 business -0.684 回归待查 |
| [2026-04-19_v7_MCP-level](./2026-04-19_v7_MCP-level/) | 2026-04-19 | MCP-level T0+T1+T2 · **自适应 turn routing** | validity 0.717 / **factual 3.000** / **business 2.947** / **hit 0.772** / **L7 1.000** | SIMPLE(8T)/MEDIUM(12T)/COMPLEX(16T)/PSEUDO(0T)。**T1 business +0.631 修复 v6 回归**；factual 首破 3.0；L4 factual +2.00；T2 factual 3.087 / business 3.316 七版最佳 |

## 使用规则

1. **跑新评估**：用工作目录 `results/T0` `results/T1`（可覆盖）
2. **对比**：`diff` 工作目录结果 ↔ 最新基线的 `SCORECARD.json`
3. **显著变动**（任一维 ±0.05 以上）→ 冻结为新快照，更新本表
4. **回归判定**：新 T1 validity/hit/refusal < 旧基线 同维 → 阻塞发布，查原因
