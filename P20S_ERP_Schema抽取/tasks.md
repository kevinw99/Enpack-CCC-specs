# Tasks: P20S ERP Schema 抽取

## Phase 0: 调研与准备（1-2 天）

- [x] 确认金蝶云星空 `T_META_*` 表在本环境的实际名称和可访问性
  → 金蝶 REST API 不直接支持 SQL；本实现改走 `QueryBusinessInfo` 官方接口
- [x] 尝试通过 P20E 的 `kingdee_query_bills` + `FormId=META_*` 读取元数据表
  → 改用 `QueryBusinessInfo` + `BOS_MetadataBusinessObject`
- [x] 评估是否可申请数据库只读账号（加速 Channel A）
  → 本期不申请，API 路径已满足需求
- [x] 列出 P20E 已涉及的核心表单清单（20+ 张，作为 MVP 范围）
  → `FORM_CATALOG` 10 张 + 扩展清单 22 张 = **32 张**

## Phase 1: Channel A 骨架（官方元数据，3-5 天）

- [x] `channels/official.py` 实现
  - [x] 读取表单元数据（采用 `QueryBusinessInfo` 替代直查 T_META_*）
  - [x] 处理多语言字段（Key=2052 提取中文名）
  - [x] 处理数据类型映射（官方返回已含 key/name/lookup/required 精简格式）
- [x] 输出中间结构（schema dict: form_id / form_name / field_count / fields / source）
- [x] 测试：MVP 10 张 + 扩展 22 张 = 32 张 100% 成功，共 3647 字段

## Phase 2: 输出渲染（2-3 天）

- [x] `renderer.py` 实现
  - [x] 单表 Markdown 生成（元信息 + 字段表 + 关联基础资料 + 枚举段）
  - [x] `index.json` 生成（version / stats / tables）
- [x] 目录结构 `schema/{form_id}.md` + `schema/index.json`
- [x] 对 MVP 20+ 张表跑一次全量输出（实际 32 张）

## Phase 3: Channel C LLM 注解（3-4 天）

- [x] `channels/llm_annotator.py` 实现
  - [x] 命名规则库 `rules/naming_rules.yaml` 编写（表/字段前缀 + 通用枚举）
  - [x] LLM prompt 模板 + DeepSeek 调用（`response_format=json_object`）
  - [x] 批次大小控制（默认 40 字段/批）
  - [x] 置信度评分（high / medium / low）
- [x] 对元数据缺失/中文描述为空的字段补全
  → 验证：本环境 QueryBusinessInfo 中文名覆盖率已达 **100%**（0 字段需补全）
- [x] 标注 `source: llm` + `confidence` 与官方数据区分

## Phase 4: 枚举值提取（2 天）

- [x] 状态字段识别规则（`FStatus / FDocumentStatus / FForbidStatus / FApproveStatus`）
- [x] 从真实数据扫描去重值（复用 `_post("query", ...)`，默认采样 200 行）
- [x] 枚举值业务含义标注（`DEFAULT_ENUM_MAP` 固化金蝶通用语义）
- [x] 典型案例：PUR_PurchaseOrder FDocumentStatus 采到 A/B/C/D 全值

## Phase 5: 关联关系图（2-3 天）

- [x] 外键字段识别（从 `lookup` 属性聚合）
- [x] 主数据表识别（`BD_ / ORG_ / SEC_ / META_` 前缀）
- [x] JOIN 路径生成（`schema/relations.json` 959 条边）
- [x] Mermaid 关系图输出（`schema/relations.md`，内部边 532 条）

## Phase 6: Schema Merger + CLI（2 天）

- [x] `merger.py` 三通道合并，优先级 A > B > C
- [x] `cli.py` 命令行入口
  - [x] `--forms` 指定表单范围
  - [x] `--mvp` / `--extended` 预设清单
  - [x] `--enums / --llm-annotate / --bos-dir / --merge` 通道开关
  - [~] `--incremental` 增量模式（当前每次覆盖，已是近似增量：`--forms X,Y` 只改指定文件）
- [x] 版本号 + 时间戳（`index.json.version / generated_at`）

## Phase 7: Channel B BOS 导出（可选，2-3 天）

- [x] BOS 导出文件格式调研（兼容 `<Form>` / `<BusinessObject>` / `<BOSBusinessObject>`）
- [x] `channels/bos_parser.py` 实现（parse_bos_file / parse_bos_dir）
- [x] 与 Channel A 合并（`merger.merge_batch(a_list, b_map)`）
- [ ] **激活**：待用户提供导出文件后 `--bos-dir ./bos_exports/` 即可启用

## Phase 8: 与 P20E 集成（2 天）

- [x] 新 MCP 工具 `kingdee_get_schema(form_id)`
- [x] 返回精简 schema（BD_Material 实测 23KB vs 原 65KB，≈65% 体积下降）
- [x] P20E 的 `describe_form` 保留为兜底（缓存未命中时自动回退 `QueryBusinessInfo`）
- [x] 新增工具 `kingdee_get_relations()` + `kingdee_list_cached_schemas()`
- [x] 文档：`docs/P20S_schema抽取器使用说明.md`

## Phase 9: 评估与迭代（持续）

- [x] 用 Q013 等典型案例回归测试（对接 P23）
  → `schema_extractor/regression.py` + `regression_cases.json` (5 用例)
- [x] 字段选择准确率统计
  → validity_rate: baseline 58.3% → with_schema **100%**（+41.7%）
- [~] 人工审核 LLM 推断标注的字段（当前无 LLM 推断产出，不需审核）
- [ ] 根据反馈更新命名规则库（持续项）

## Phase 10: 文档与交付

- [x] `docs/P20S_schema抽取器使用说明.md`（命令行 + MCP 工具 + 架构）
- [x] `docs/P20S_回归评估结果.md`（评估发现 + 数据）
- [x] 把 MVP 20+ 张表的 schema 入库（实际 32 张，3647 字段）
- [ ] 业务人员（吕经理）审核枚举值标注（待运营）

## 图例

- [x] 已完成
- [~] 部分完成 / 有说明
- [ ] 待运营或等外部依赖
