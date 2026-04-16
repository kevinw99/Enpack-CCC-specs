# P26 MCP-level 全量评估报告（真实工具链）

**日期**: 2026-04-16 完成（跑于 2026-04-15 23:18 → 2026-04-16 01:03，共约 1h45m）
**题集**: P26 V1 · 46 题
**模型**: deepseek-chat, temperature=0, 经 MCP stdio 协议调真实工具
**Runner**: `scorer/mcp_runner.py`（P26 自产）
**Stage 工具白名单**:
- T0：`query_* + describe_form + search_forms_online`（6 个，P20S/P20T 未上线状态）
- T1：T0 + `kingdee_get_schema / _relations / _list_cached_schemas`（P20S 上线）
- T2：T1 + `kingdee_get_wiki`（P20T 上线）

---

## 1. 五维总览：真实 MCP-level vs LLM-level 模拟

| 维度 | T0 (MCP) | T1 (MCP) | T2 (MCP) | T0→T1 | T1→T2 | T0→T2 | 参考：T1 LLM-level |
|------|----------|----------|----------|-------|-------|-------|---------------------|
| validity_rate | 0.637 | 0.529 | 0.506 | **-0.108** | -0.023 | -0.131 | 0.829 |
| hit_rate | 0.713 | 0.545 | 0.508 | **-0.168** | -0.037 | -0.205 | 0.577 |
| L7_refusal | 0.833 | **0.500** | 0.833 | -0.333 | +0.333 | 0 | 0.833 |
| factual /5 | 3.281 | **1.344** | 1.594 | **-1.937** | +0.250 | -1.687 | 3.531 |
| business /5 | 2.583 | 2.833 | 2.833 | **+0.250** | 0 | **+0.250** | 2.667 |

### 颠覆性发现

**LLM-level 模拟与 MCP-level 实测呈现完全相反的趋势。** LLM-level 模拟显示 T0→T1 validity +0.336（P20S schema 注入显著增益），但真实 MCP 路径反而 **-0.108**。

根因：LLM-level 是"把 schema 直接灌进 prompt"的上限测试；MCP-level 要求 LLM **自主调用 get_schema 并在 turn budget 内消化**，现实中不成立。

---

## 2. 瓶颈定位：Turn Budget

### 工具采纳率

| 维度 | T0 | T1 | T2 |
|------|-----|-----|-----|
| `kingdee_get_schema` 采纳 | 24%* | **96%** | **96%** |
| `kingdee_get_wiki` 采纳 | 2% | 0% | **85%** |
| `kingdee_get_relations` 采纳 | 0% | 20% | 11% |
| 平均使用轮数 | 7.9 | 8.0 | 8.0 |
| **命中 MAX_TURNS=8 上限比例** | **93%** | **100%** | **100%** |

\* T0 阶段 `get_schema` 未在白名单内，24% 可能为 LLM 解释 question 文本时的误报匹配；不影响结论。

**核心矛盾**：
- T1/T2 下 LLM 几乎每题都用到了新工具（schema 96%、wiki 85%）→ **P20S/P20T 的可发现性没问题**
- 但 100% 题命中 8 轮上限 → **LLM 把 turn budget 花在反复试探工具（`get_schema`→`list_cached`→`describe_form`→`search_forms_online`），真正执行 `query_bills` 的机会被挤占**

### 可观测的失败模式

| 模式 | 例子 |
|------|------|
| **重复 schema 调用**：同一表单调 `get_schema` 多次 | L1-02 T1：get_schema ×3, list_cached ×1, describe_form ×1 → 只剩 3 轮做查询 |
| **Schema miss 后级联降级**：cache 不中 → describe_form → search_forms_online → 放弃 | L8-01 T1：cache 中没 SAL_SaleOrder → search_forms_online ×N → 最终 picked=[] |
| **Wiki 误用**：找不到 schema 时用 wiki 判"伪问题"逃避复杂题 | L8 T2：4/4 题全部宣称"数据不在 ERP"（实际是多步分析题，非伪问题）|

---

## 3. 分层结果（validity / hit / factual）

### L1 控制组

- validity T0 0.881 → T1 0.536（**-0.345**）→ T2 0.653
- factual T0 4.800 → T1 1.000 → T2 2.400
- 预期应≈0 的控制组，真实 MCP 下 delta 高达 **-3.8**（factual）
- 归因：T0 下 LLM 直接调 `query_materials`；T1/T2 被新工具引诱，浪费 turns 后没结果

### L2 字段幻觉 / L3 JOIN

- validity 都轻微下滑，hit_rate 下滑明显（L2 0.838 → 0.570；L3 0.396 → 0.208）
- **LLM-level 模拟预测的 P20S "核心战场胜利"没有在真实 MCP 路径兑现**
- 根因：LLM 拿到 schema 后仍要花 turns 构造 filter/join，turn budget 不够收尾

### L4 状态枚举

- T0 factual 2.667 → T2 0.000（4 题全挂）
- T2 下 LLM 读完 wiki 后反而对"已审核=？"产生新困惑，延展试探导致超时

### L5 自定义字段

- validity T0 0.849（LLM 在 T0 居然就答对了？）→ T1 0.709 → T2 0.660
- 原因反常但合理：T0 无 schema 工具，LLM 退回到直接 `query_bills` 查 BD_Supplier 全字段，误打误撞命中 F_BDK_LXR 这类字段；T1/T2 下 LLM 反复调 schema 读定义，结果 turns 耗尽没出数据

### L6 业务规则 ★ 唯一 business 正增益

- **business 从 2.429 → 2.714 → 2.857（T0→T2 +0.428）** — wiki 真的在帮公司规则判断
- factual 同时剧降（3.000 → 0.000 → 2.000）：wiki 读懂了但 turns 耗尽，具体事实层崩塌
- **这题验证了 P20T 的定位：业务判断层是正向，事实层需要 turn budget 配套才能兑现**

### L7 伪问题识别

- T1 refusal **崩到 0.500**（新工具让 LLM 犹豫，尝试搜索而非直接拒答）
- T2 refusal **回到 0.833**（wiki 的"伪问题与数据缺口"目录起效，LLM 学会直接引用）
- **P20T 对 L7 的回升是本次最干净的正面结果之一**

### L8 多步分析 ★ T2 灾难

- factual T0 2.750 → T1 1.500 → T2 **0.000**（4 题全 picked=[]）
- **失败模式**：L8-01/02/03/04 在 T2 全部宣称"伪问题、数据不在 ERP"
- 实际 L8-04 是"本周经营简报" — T0 下 LLM 凑出了合理的对比数据（1.5-2w 营收、4 笔订单），T2 下却说"SAL_SaleOrder 不在 cache，故无法回答"
- **wiki 工具给了 LLM 一个逃避复杂题的快捷理由**

---

## 4. 与 LLM-level 基线的对比

| 维度 | LLM-level T1（2026-04-15 v1）| MCP-level T1（本次）| 落差 |
|------|------------------------------|----------------------|------|
| validity | 0.829 | 0.529 | **-0.300** |
| hit_rate | 0.577 | 0.545 | -0.032 |
| factual | 3.531 | 1.344 | **-2.187** |
| business | 2.667 | 2.833 | +0.166 |
| L7_refusal | 0.833 | 0.500 | -0.333 |

LLM-level validity/factual 是**上限**（schema 预灌），MCP-level 是**实际**。差距 -0.300（validity）、-2.187（factual）是 **P20E 整合损耗** 的第一次量化。

---

## 5. 行动项（按影响度）

### P0 — 必须修（决定 P20S/P20T 能否交付价值）

1. **提高 MAX_TURNS 至 12-15 并优化 system prompt** — 现在 100% 命中 8 轮上限，改善空间最大；预期 factual +1.0 以上
2. **加工具幂等性提示** — system prompt 明确"同一 form_id 不重复调 get_schema"；现在 96% 的题重复调 2-3 次
3. **修 L8 T2 伪问题误判** — wiki system prompt 加硬约束："只有题目明确不涉及任何 ERP 数据时才宣称伪问题；涉及 PO/销售订单/库存的分析类题目必须尝试查询"

### P1 — 修复 P20S 覆盖缺口

4. **扩 schema cache 覆盖**：SAL_SaleOrder / AR_receivable / AP_PAYBILL 不在 32 张 cache 内，导致 L2/L3/L8 relevant 题频繁降级到 describe_form → search_forms_online → 放弃
5. **索引友好化**：`kingdee_list_cached_schemas` 在 LLM 视角下应附带"已缓存哪些业务域"的元信息，降低它瞎试的欲望

### P2 — 方法学改进

6. `mcp_runner` 加记录 **turns_breakdown**（发现/查询/思考各占几轮），便于诊断
7. 为每 stage 单独记录 **tool-adoption × outcome-quality** 相关性
8. 完成 P26 Phase 1C 业务审阅（吕经理），校验 L8 的评分标准

---

## 6. P26 假设的重新校准

| 原假设 | 真实结果 | 状态 |
|--------|----------|------|
| P20S schema 注入 → validity 显著正增益 | MCP-level **反而 -0.108** | ❌ 条件成立才为真：需要足够 turn budget |
| P20T wiki → L7 refusal ≥0.95 | T2 仅回到 0.833（= T0）| ⚠️ 部分成立：wiki 避免了 T1 的退化，但没超过 T0 |
| P20T wiki → L6 business 显著升 | T0 2.429 → T2 2.857 (+0.428) | ✅ 唯一干净正增益 |
| P20S/P20T 联合 → L8 多步分析显著升 | T2 factual 崩到 0 | ❌ 反向效应，wiki 被误用作逃避工具 |

**结论**：P26 框架揭示了 P20S/P20T 在真实 MCP 链路下的**隐性假设**——它们只有在 turn budget 充分 + prompt 约束精细的条件下才能兑现价值。**LLM-level 模拟得出的"显著增益"结论需要修订为"上限增益"**。

---

## 7. 产物

```
results/baselines/2026-04-15_v1_MCP-level/   ← 不可变基线
├── SCORECARD.json                            ← 机器可读五维 + 分层
├── comparison.md                             ← T0/T1/T2 对比表
├── T0/T1/T2/                                 ← 原始 answers + 4 judge json
results/comparison_mcp.md                     ← 工作目录同版
results/mcp_full_run.log                      ← 完整跑批日志
```

下一步：按 P0 action items 改 runner，重跑，对比本基线（应看到 factual 从 1.344 显著回升）。
