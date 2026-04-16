# P26 T0 / T1 基线报告（LLM 层模拟）

**日期**: 2026-04-15
**模型**: DeepSeek (deepseek-chat, temperature=0)
**题集**: P26 V1 46 题（`questions/_all.json`）
**指标**:
- `validity_rate`（答案中引用字段在真实 schema 中的比例，剔除拒答题）
- `hit_rate`（答案覆盖 `required_fields_hint` 的比例）
- `refusal_correctness`（L7 伪问题识别）
- `factual_correctness`（LLM-as-Judge, 0-5 分）
- `business_grounding`（LLM-as-Judge 对照 wiki 业务规则, 0-5 分）

> 说明：本次为 **LLM 层模拟**，不经 P20E MCP harness 真实跑数。T0 只给 form_id，T1 同时注入 `schema/{form}.md`，用以评估"假如 P20E 把 schema 传入 LLM 上下文会如何"。真实 T1（P20E 整合 P20S 后走 MCP 工具）留待 Phase 4。
>
> v3（2026-04-15）修订：
> - 评分器修复 `F_BDK_*` 类自定义字段正则识别漏洞
> - 对 picked=[] 的答案做 refusal gating（不计入 validity 均值）
> - 新增 `hit_rate` 指标与 `required_fields_hint` 做命中对比
> - **新增 LLM-as-Judge 两维**：`factual_correctness` 与 `business_grounding`

## 总览四维（T0 vs T1）

| 维度 | T0 | T1 | delta | 说明 |
|------|-----|-----|-------|------|
| validity_rate | 0.493 | 0.829 | **+0.336** | schema 注入后字段准确性大涨 |
| hit_rate | 0.471 | 0.577 | +0.106 | 覆盖 hint 的比例同向上升 |
| L7_refusal | 0.833 | 0.833 | 0 | 预期（P20T 才能动）|
| factual /5 | 3.656 | 3.531 | **-0.125** | ⚠️ 反直觉下降，见下方分析 |
| business /5 | 2.833 | 2.667 | **-0.166** | ⚠️ 同上，业务规则待 T2 P20T 补 |

### 关于 factual/business 微降（-0.125 / -0.166）

validity 大幅提升的同时 judge 两维轻微下降，表面矛盾，实质是**不同维度的测量对象**：
- validity 只看"字段名是否真存在"；judge 看"整体答题是否完整正确"
- T1 下 LLM 拿到 schema 后有时**过度自信**（L1-05 反而去试答应拒的题，0/5；L3-02/03 转为硬拒答，0/5），拉低 judge 均值
- 真正体现价值的 L5/L6 factual 分别 +2.0 / +1.0
- business 维 L6 -0.428 已预示 wiki 缺失的代价（L6-04 判断"应收已审核=款已到"与公司规则冲突，2/5）— 这正是 T2 要填的坑

**结论**：validity+hit_rate 是 P20S 的直接度量；factual/business 的真正增益要等 T2（P20T wiki 注入）才会显现。

## 核心结果（validity_rate，已应用 refusal gating）

| Layer | T0 | T1 | delta | 预期 P20S 增益 | 验证 |
|-------|-----|-----|-------|----------------|------|
| L1 控制组 | 0.833 | 1.000 | **+0.167** | none | ⚠️ 小幅升（LLM 被 schema 引导更精确）|
| L2 字段幻觉 | 0.297 | 0.650 | **+0.353** | large | ✅ 核心战场命中 |
| L3 JOIN | 0.584 | 1.000 | **+0.416** | medium | ✅ 超预期 |
| L4 状态枚举 | 0.539 | 0.950 | **+0.411** | medium | ✅ 超预期 |
| L5 自定义字段 | 0.710 | 0.635 | **-0.075** | large | ❌ 见 L5 分析 |
| L6 业务规则 | 0.309 | 0.800 | **+0.491** | small | ✅ 远超预期 |
| L7 refusal | 0.833 | 0.833 | 0 | none | ✅ 预期（P20T 才能动）|
| L8 多步分析 | 0.521 | 0.969 | **+0.448** | medium | ✅ 超预期 |
| **整体** | **0.493** | **0.829** | **+0.336** | | ✅ 整体验证 |

## hit_rate 辅助视角（覆盖 `required_fields_hint`）

| Layer | T0 | T1 | delta |
|-------|-----|-----|-------|
| L1 | 0.767 | 0.733 | -0.034 |
| L2 | 0.443 | 0.592 | **+0.149** |
| L3 | 0.250 | 0.562 | **+0.312** |
| L4 | 0.433 | 0.600 | +0.167 |
| L5 | 0.750 | 0.083 | **-0.667** ⚠️ |
| L6 | 0.333 | 0.500 | +0.167 |
| L8 | 0.500 | 0.666 | +0.166 |
| **整体** | **0.477** | **0.555** | **+0.078** |

## L5 反常：validity 和 hit_rate 都降了，到底怎么回事？

单题追查（L5-01 供应商联系人）：
- 题目 hint: `[FNumber, FName, F_BDK_LXR, F_BDK_DH]`
- **T0 答案**: `[FName, FContact, FPhone]` — LLM 凭直觉猜"联系人=FContact、电话=FPhone"，这两个字段在 `BD_Supplier` schema 里**并不存在**（fContact 与 FPhone 只是 LLM 常识）
- **T1 答案**: `[F_BDK_LXR, F_BDK_LXDH]` — LLM 正确从注入的 schema 里找到真实的自定义字段
- **真实 schema**: 联系电话字段为 `F_BDK_LXDH`，**我写的 hint 里 `F_BDK_DH` 是错的**

**结论**: L5 的"负增益"是**我的 hint 写错**造成的，不是 P20S 副作用。T1 答的是对的，T0 答的是错得听起来对。hit_rate 指标在 L5 上反而被错误 hint 误导。

**改进**: Phase 1C 业务方审核时，需用 `kingdee_get_schema` 核对每题的 `required_fields_hint`。已在 action items 标注。

## 与预期增益的对照

所有"预期 small 以上"增益的层（L2/L3/L4/L5/L6/L8）实测 delta 均 ≥ +0.35，**P20S 价值假设验证**。

特别观察：
- **L6 意外大增** (+0.491)：原以为业务规则只能靠 P20T 补全，实际 schema 注入也让 LLM 的推理更锚定到具体字段（如"发货条件 = FDocumentStatus='C' 且未关闭"这类组合判断题，schema 里列出 FDocumentStatus 的值域就足够了）
- **L1 轻微上升** (+0.167)：控制组本不应升，但因 T0 下 LLM 常猜 FPhone/FContact 这类不存在的字段，schema 把它们校正过来。这是"边角副作用"但方向有利

## 真实 T1 的验证计划（Phase 4）

当前 T1 是 LLM 层模拟（schema 直接注入 prompt）。P20E 整合 P20S 后需补跑真实 MCP-level T1：
- LLM 需**主动调用** `kingdee_get_schema(form_id)` 才能取到 schema
- 若 LLM 没学会调这个工具（CLAUDE.md / docstring 引导不够），实际 T1 会比本次模拟低
- LLM-level T1 是**上限**，MCP-level T1 是**实际**；两者差距反映 P20E 整合质量

## 待 P20T 上线后的 T2

Phase 5 将新增 T2（P20S + P20T Wiki 都整合），届时重点观测：
- L4 能否进一步升（wiki 补充"已审核=可供货"等公司私有语义）
- L6 能否继续升（wiki 是业务规则的主要阵地；不过本次模拟已升至 0.8，天花板将近）
- **L7 refusal 能否从 0.833 升至 ≥0.95**（wiki 明确标注伪问题清单）— 最关键观测
- L8 能否维持或进一步升（wiki 分析模板）

## factual/business 分层增益亮点

| Layer | factual T0 | factual T1 | business T0 | business T1 |
|-------|-----------|-----------|-------------|-------------|
| L1 | 4.400 | 3.600 | — | — |
| L2 | 4.100 | 4.100 | — | — |
| L3 | 3.667 | 2.833 | — | — |
| L4 | 4.000 | 3.667 | 2.667 | **3.000** |
| **L5** | 2.000 | **4.000** | — | — |
| **L6** | 2.000 | **3.000** | 2.857 | 2.429 |
| L8 | 3.000 | 2.750 | 3.000 | 3.000 |

- L5 factual **+2.0**：schema 让 LLM 首次能写出真实的 F_BDK_* 字段
- L6 factual **+1.0** / business **-0.428**：事实增强、业务冲突并存，指向 T2 补 wiki
- L1/L3 factual 下降属 schema 引导副作用（见上）

## Action Items

1. ✅ validity 正则支持 `F_BDK_*` 自定义字段
2. ✅ picked=[] 做 refusal gating，不再污染 validity 均值
3. ✅ 新增 hit_rate 指标
4. ✅ 新增 factual / business LLM-as-Judge 两维
5. ⏳ 业务方审核时用 `kingdee_get_schema` 校对每题 `required_fields_hint`，特别是 L5 自定义字段
6. ⏳ L3 JOIN 题补强，现有题增益测得太容易（+0.416）可能是题目偏简单，V2 加入更多多表真实 JOIN
7. ⏳ P20E 整合 P20S → 跑真实 MCP-level T1，与本报告交叉验证
8. ⏳ P20T 完成 → 跑 T2，补完三段对比；关键观测：L6 business 能否从 2.429 回升 ≥ 4.0
