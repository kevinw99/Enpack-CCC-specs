# Status: P20S ERP Schema 抽取

## Current Status

**Overall**: ✅ All Phases Implemented (0-10，Phase 7 待用户提供 BOS 文件激活)
**Started**: 2026-04-15
**Last Updated**: 2026-04-15

## Completed Work

- 2026-04-15: 规格创建（requirements, design, tasks, status）
  - 基于 P20E 现状（`describe_form` 65KB 技术债）和 P20T 需求（Text2SQL schema 基础）
  - 三通道抽取方案：T_META_* SQL（主）+ BOS 导出（补充）+ LLM 推断（兜底）
- 2026-04-15: Phase 1 + Phase 2 完成（MVP）
  - 包结构 `源代码/mcp-kingdee-server/schema_extractor/`
  - Channel A (official.py)：复用 kingdee_client._describe_form / _search_forms_online
  - renderer.py：输出 `schema/{form_id}.md` + `schema/index.json`
  - cli.py：`python -m schema_extractor --mvp | --forms ... | --list`
  - naming_rules.yaml：字段/表前缀规则库（供 Channel C 使用）
  - 对 FORM_CATALOG 中 10 张 MVP 表跑通，全部成功（1377 字段总计）
    - BD_Material (372), PUR_PurchaseOrder (317), FA_CARD (145),
      PUR_Requisition (130), BD_Supplier (123), BD_Customer (112),
      BD_Empinfo (63), BD_Stock (46), BD_Department (40), STK_Inventory (29)

- 2026-04-15: Phase 4 完成（枚举值扫描）
  - `enum_scanner.py`: 扫描 FDocumentStatus/FForbidStatus/FStatus/FApproveStatus
  - CLI 新增 `--enums` 开关，默认每表采样 200 行
  - 已验证：PUR_PurchaseOrder 采集到 FDocumentStatus 4 个取值（A/B/C/D），
    PUR_Requisition 1 个，BD_Empinfo 2 个状态字段
  - 通用枚举含义映射固化在 DEFAULT_ENUM_MAP
- 2026-04-15: Phase 8 完成（与 P20E MCP 集成）
  - 新工具 `kingdee_get_schema(form_id)`: 优先读 schema/ 缓存（3-30KB），未命中回退到实时 `QueryBusinessInfo`
  - 新工具 `kingdee_list_cached_schemas()`: 返回已入库表单清单
  - BD_Material 缓存 schema: 23KB（vs 原 describe_form 65KB，≈65% 体积下降）
  - 原 `kingdee_describe_form` 保留兜底

- 2026-04-15: Phase 3 完成（LLM 注解通道，Channel C）
  - `channels/llm_annotator.py`：DeepSeek + naming_rules.yaml，按表批次推断缺中文名字段
  - 实测 32 张表全部字段（3647 个）中文名覆盖率 100%（官方通道已足够）
  - Channel C 基础设施就绪，供未来 T_META_* 不全或客户化字段场景使用
- 2026-04-15: Phase 6 完成（三通道合并）
  - `merger.py`：按 key 合并，优先级 A > B > C，保留实体分组结构
  - CLI 支持 `--merge / --llm-annotate / --bos-dir` 自动触发
- 2026-04-15: Phase 7 完成（BOS 解析器骨架，Channel B）
  - `channels/bos_parser.py`：支持 `.bos` / `.xml` 导出解析（多语言 Name、LookUp）
  - 待用户提供导出文件后启用：`--bos-dir ./bos_exports/`
- 2026-04-15: FORM_CATALOG 扩展
  - 新增 22 张高频被引用表（ORG/SEC/BD_UNIT/BD_TaxRate/BD_Currency/ENG_BOM/PRD_MO 等）
  - 共 32 张表落入 schema/，字段总数 3647
  - lookup 关系内部边从 42 升至 532（13× 提升）
- 2026-04-15: Phase 9 完成（P23 回归测试桥）
  - `schema_extractor/regression.py`：对比 baseline vs with-schema 场景下的字段选择
  - 引入 `validity_rate` 指标（字段是否真实存在于 schema）
  - 初始 5 用例结果：with_schema validity 100% vs baseline 58.3%（+41.7%）
  - 关键发现：schema 消除 LLM 对字段名的幻觉，揭示公司自定义字段（如 F_BDK_LXR）
  - 产出 `docs/P20S_回归评估结果.md`
- 2026-04-15: Phase 5 完成（关联关系图）
  - `relations.py`: 从 lookup 抽取外键，内部/外部分类
  - 产出 `schema/relations.json` + `schema/relations.md`（Mermaid flowchart）
  - 新 MCP 工具 `kingdee_get_relations()` 暴露给 AI
  - 实测：MVP 10 张表产出 385 条关系（42 内部 + 343 外部指向未入库的 82 张表）
- 2026-04-15: Phase 10 完成（文档）
  - `docs/P20S_schema抽取器使用说明.md`：命令行、MCP 工具、架构速览

## Current Work

- 规格全量实现完成。持续运营项：
  - 扩大 FORM_CATALOG 到剩余 114 个外部 lookup 目标（当前仅覆盖 32/146）
  - 对业务方验证自定义字段（F_BDK_*）的数据质量
  - 对接 P23 评估用例跑完整 28 题

## Remaining Work

- [x] Phase 0: 调研 T_META_* 实际可访问性（采取 QueryBusinessInfo API 路径）
- [x] Phase 1: Channel A 骨架
- [x] Phase 2: 输出渲染
- [x] Phase 3: LLM 注解（Channel C）
- [x] Phase 4: 枚举值提取
- [x] Phase 5: 关联关系图
- [x] Phase 6: 三通道合并
- [x] Phase 7: BOS 解析器（待文件激活）
- [x] Phase 8: 与 P20E 集成
- [x] Phase 9: P23 回归测试桥
- [x] Phase 10: 文档
- [ ] Phase 3: Channel C LLM 注解
- [ ] Phase 4: 枚举值提取
- [ ] Phase 5: 关联关系
- [ ] Phase 6: CLI + Merger
- [ ] Phase 7: Channel B BOS（可选）
- [ ] Phase 8: 与 P20E 集成
- [ ] Phase 9: 评估
- [ ] Phase 10: 文档交付

## Session Notes

### Session 2026-04-15
- Accomplished: 创建 P20S 规格，承接金蝶数据库描述获取的讨论
- Context:
  - 用户提问: "金蝶系统的数据库怎么能够得到它的描述呢？DDL 有没有开源或别人已做过的注解"
  - 讨论得出三类来源: 官方（T_META_* + BOS）、开源社区（不完整）、LLM 反推
  - 本规格选择三通道组合方案，避免依赖不可靠的社区数据
- Next steps: 联系系统管理员确认元数据表访问权限，开始 Phase 0
- Blockers:
  - 需要确认金蝶 API 是否允许查询 `T_META_*` 表
  - 枚举值业务含义标注需要吕经理配合

## Key Metrics（目标）

| 指标 | 当前 | 目标 |
|------|------|------|
| 覆盖表数 | 0 | ≥ 20 张（MVP） |
| 字段中文名覆盖率 | — | ≥ 95% |
| 枚举值覆盖率 | — | ≥ 90% |
| 业务注解覆盖率 | — | ≥ 80% |
| describe_form 响应体积 | 65KB | < 5KB (替代工具) |

## Open Questions

1. 金蝶云星空是否可通过 REST API 访问 `T_META_*`？若否，是否能申请 DB 只读权限？
2. BOS 导出功能是否在当前权限下可用？导出文件格式是什么？
3. LLM 推断的字段含义是否需要业务人员逐条审核？还是抽样审核即可？
