# Status: P20S ERP Schema 抽取

## Current Status

**Overall**: Phase 1+2 Done (MVP)
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

## Current Work

- MVP 已产出，下一步可选：
  - Phase 3（LLM 注解）：为缺中文名字段补全
  - Phase 4（枚举值提取）：扫描 FStatus/FDocumentStatus 等字段真实取值
  - Phase 8（与 P20E 集成）：新增 `kingdee_get_schema(form_id)` 工具返回精简 schema

## Remaining Work

- [x] Phase 0: 调研 T_META_* 实际可访问性（采取 QueryBusinessInfo API 路径）
- [x] Phase 1: Channel A 骨架
- [x] Phase 2: 输出渲染
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
