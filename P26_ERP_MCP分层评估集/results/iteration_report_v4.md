# P26 MCP-level 迭代报告：v1 → v2 → v3 → v4

**时间范围**：2026-04-15 23:18 → 2026-04-16 13:15（约 14 小时，4 次完整跑批 + 3 次迭代）

---

## TL;DR

| 版本 | factual T1 | business T2 | L7 T2 | 主要变更 |
|------|-----------|-------------|-------|----------|
| v1 | 1.344 | 2.833 | 0.833 | 初始（MAX_TURNS=8）|
| v2 | **3.031** | 2.833 | 0.500 | turns 12 + 幂等 + 抗逃避 |
| v3 | 2.594 | 2.833 | **0.833** | 双向约束（L7 修复）|
| v4 | 2.688 | **3.000** | 0.500 | stage-specific prompt + tool quota |

**核心发现**：factual/business 与 L7 refusal 存在 **prompt 层面的结构性矛盾**。v2/v4 优化了前者但 L7=0.500；v3 优化了后者但 factual 退让。4 轮迭代证明 prompt-only 调优已到极限。

**推荐**：
- **综合最优发布基线**：选 v3（L7 最干净）还是 v4（factual/business 最优）取决于业务优先级
- **v3 适合**：重视伪问题拒答准确性的场景（对外演示、合规展示）
- **v4 适合**：重视实际查询能力的场景（日常使用、数据分析）

---

## 1. 四版五维总览

### T0（无新工具基线）

| 指标 | v1 | v2 | v3 | v4 | v1→v4 |
|------|-----|-----|-----|-----|-------|
| validity | 0.637 | 0.507 | 0.532 | 0.519 | -0.118 |
| hit_rate | 0.713 | 0.662 | 0.663 | 0.680 | -0.033 |
| L7_refusal | 0.833 | 0.500 | 0.500 | 0.500 | -0.333 |
| factual | 3.281 | 2.719 | 2.250 | **2.500** | -0.781 |
| business | 2.583 | 2.667 | 3.000 | 2.833 | +0.250 |

v4 的 stage-specific prompt 让 T0 factual 从 v3 的 2.250 回升到 2.500（+0.250），验证了 B/C 约束确实在拖累 T0。但 T0 仍未回到 v1 水平——其余 prompt 改动（幂等性、turn 预算等）对 T0 也有轻微负面。

### T1（+P20S Schema）

| 指标 | v1 | v2 | v3 | v4 | v1→v4 |
|------|-----|-----|-----|-----|-------|
| validity | 0.529 | 0.526 | 0.492 | 0.516 | -0.013 |
| hit_rate | 0.545 | **0.737** | 0.703 | 0.704 | +0.159 |
| L7_refusal | 0.500 | 0.167 | **0.667** | 0.500 | 0 |
| factual | 1.344 | **3.031** | 2.594 | 2.688 | **+1.344** |
| business | 2.833 | 2.917 | 2.750 | **2.917** | +0.084 |

v4 T1 factual 2.688 和 business 2.917 都是仅次于 v2 的最佳记录。hit_rate 0.704 稳定在 v2 级别。

### T2（+P20S +P20T Wiki）

| 指标 | v1 | v2 | v3 | v4 | v1→v4 |
|------|-----|-----|-----|-----|-------|
| validity | 0.506 | 0.532 | 0.519 | 0.532 | +0.026 |
| hit_rate | 0.508 | 0.663 | 0.685 | 0.684 | +0.176 |
| L7_refusal | 0.833 | 0.500 | **0.833** | 0.500 | -0.333 |
| factual | 1.594 | 2.688 | 2.531 | **2.688** | +1.094 |
| business | 2.833 | 2.833 | 2.833 | **3.000** | **+0.167** |

v4 T2 business 3.000 是四版最佳——search_forms_online 硬限回收的 turn 让 LLM 有更多轮调用 wiki，business grounding 受益。

---

## 2. v4 变更生效验证

| 变更 | 预期 | 实际 |
|------|------|------|
| B/C 约束仅 T1/T2 | T0 factual 回升 | ✅ T0 factual +0.250（2.250→2.500）|
| search_forms_online ≤ 2 | 减少 turn 浪费，factual 提升 | ✅ T1 factual +0.094、T2 +0.157；T2 business +0.167 |
| 不影响 L7 | L7 维持 v3 水平 | ❌ L7 T1 -0.167、T2 -0.333 |

### L7 再次回归的根因

search_forms_online 硬限实际上*间接*影响了 L7：在 v3 中，LLM 遇到伪问题时会调 search_forms_online 多次、耗尽 turn、被迫 forced_summary（间接拒答）。v4 堵住了这条"浪费路径"后，LLM 有了充足 turn 去尝试 query_bills——对真实题有利（factual 上升），对伪问题有害（L7 下降）。

这确认了 **factual ↗ 和 L7 ↗ 在当前 prompt 架构下是互斥方向**。

---

## 3. 四版对比结论

### Pareto 前沿

```
         factual T1
    3.1  ┤        v2●         ← factual 最强，L7 最差
    2.9  ┤
    2.7  ┤              v4●   ← factual+business 均衡，L7 一般
    2.5  ┤        v3●         ← L7 最强，factual 可接受
    2.3  ┤
    1.3  ┤  v1●               ← 基线
         └──┬──┬──┬──┬──┬──→ L7 refusal T2
           0.5 0.6 0.7 0.8 0.9
```

v2/v3/v4 形成 Pareto 前沿，v1 被支配。三者之间的选择是**优先级权衡**，不是"哪个更好"。

### 推荐选择

| 用途 | 推荐版本 | 理由 |
|------|----------|------|
| 对外展示/合规演示 | **v3** | L7 refusal T2=0.833 最干净 |
| 日常数据分析使用 | **v4** | factual/business 最优、T0 恢复 |
| factual 上限参考 | v2 | T1 3.031 历史最高 |

---

## 4. 下一步决策点

**Prompt-only 迭代已收敛**（4 轮，Pareto 前沿稳定），后续进展需要换层：

| 选项 | 层级 | 预期收益 | 工作量 |
|------|------|----------|--------|
| 代码层 L7 预筛 | runner 代码 | L7→0.83+ 不影响 factual | 小（关键词匹配） |
| Few-shot 示例 | prompt | L7 +0.1~0.2（不确定） | 小 |
| 扩充 Schema 缓存 | src.server | factual 全线 +（更多表可查） | 中（需梁咏芝配合） |
| Vanna Text2SQL 集成 | 架构层 | 绕过 turn 瓶颈，直接生成 SQL | 大 |

---

## 5. 产物清单

- `results/baselines/2026-04-15_v1_MCP-level/` — 首个真实基线
- `results/baselines/2026-04-16_v2_MCP-level/` — factual 最强
- `results/baselines/2026-04-16_v3_MCP-level/` — L7 最强
- `results/baselines/2026-04-16_v4_MCP-level/` — factual+business 均衡、T0 恢复
- `results/baselines/INDEX.md` — 索引（5 个快照）
- `results/final_three_baseline_report.md` — v1-v3 报告（历史保留）
- `results/iteration_report_v4.md` — 本文件（v1-v4 总报告）
- git commits: `5276459` (v1+P0) → v2 freeze → `7d783c9` (v3) → `3b3e03b` (v4 prep) → v4 freeze
