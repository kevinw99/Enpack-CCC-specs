# Tasks: P20S ERP Schema 抽取

## Phase 0: 调研与准备（1-2 天）

- [ ] 确认金蝶云星空 `T_META_*` 表在本环境的实际名称和可访问性
- [ ] 尝试通过 P20E 的 `kingdee_query_bills` + `FormId=META_*` 读取元数据表
- [ ] 评估是否可申请数据库只读账号（加速 Channel A）
- [ ] 列出 P20E 已涉及的核心表单清单（20+ 张，作为 MVP 范围）

## Phase 1: Channel A 骨架（官方元数据，3-5 天）

- [ ] `channels/official.py` 实现
  - [ ] 读取 `T_META_OBJECTTYPE` / `T_META_TABLE` / `T_META_FIELD`
  - [ ] 处理多语言字段（`FNAME_L2` / `FFIELDNAME_L2` 中文）
  - [ ] 处理数据类型映射（金蝶类型 → 标准类型）
- [ ] 输出中间结构 `RawSchema` (内部数据模型)
- [ ] 单元测试：能成功抽取 1 张测试表

## Phase 2: 输出渲染（2-3 天）

- [ ] `renderer.py` 实现
  - [ ] 单表 Markdown 生成
  - [ ] `index.json` 生成
- [ ] 目录结构 `schema/{form_id}.md` + `schema/index.json`
- [ ] 对 MVP 20 张表跑一次全量输出

## Phase 3: Channel C LLM 注解（3-4 天）

- [ ] `channels/llm_annotator.py` 实现
  - [ ] 命名规则库 `rules/naming_rules.yaml` 编写
  - [ ] LLM prompt 模板 + DeepSeek/Claude 调用
  - [ ] 样本数据采样（去重 + 限量）
  - [ ] 置信度评分
- [ ] 对元数据缺失/中文描述为空的字段补全
- [ ] 标注 `source: llm` 与官方数据区分

## Phase 4: 枚举值提取（2 天）

- [ ] 状态字段识别规则（`FStatus`, `F*Status` 后缀）
- [ ] 从真实数据扫描去重值（复用 P20E 的 `kingdee_query_bills`）
- [ ] 枚举值业务含义标注（LLM + 人工补充）
- [ ] 典型案例：Q013 涉及的 FStatus 状态值完整覆盖

## Phase 5: 关联关系图（2-3 天）

- [ ] 外键字段识别（`F*Id` 命名）
- [ ] 主数据表识别（`T_BD_*`）
- [ ] JOIN 路径生成
- [ ] Mermaid 关系图输出（可选）

## Phase 6: Schema Merger + CLI（2 天）

- [ ] `merger.py` 三通道合并，优先级逻辑
- [ ] `cli.py` 命令行入口
  - [ ] `--forms` 指定表单范围
  - [ ] `--incremental` 增量模式
  - [ ] `--channels` 选择通道
- [ ] 版本号 + 时间戳

## Phase 7: Channel B BOS 导出（可选，2-3 天）

- [ ] BOS 导出文件格式调研
- [ ] `channels/bos_parser.py` 实现
- [ ] 与 Channel A 合并

## Phase 8: 与 P20E 集成（2 天）

- [ ] 新 MCP 工具 `kingdee_get_schema(form_id)`
- [ ] 返回精简 schema（3-5KB vs 原 65KB）
- [ ] P20E 的 `describe_form` 保留为兜底
- [ ] 文档：`docs/使用 schema 工具.md`

## Phase 9: 评估与迭代（持续）

- [ ] 用 Q013 等典型案例回归测试（对接 P23）
- [ ] 字段选择准确率统计
- [ ] 人工审核 LLM 推断标注的字段
- [ ] 根据反馈更新命名规则库

## Phase 10: 文档与交付

- [ ] `docs/schema-extractor-design.md`
- [ ] `docs/schema-extractor-usage.md`
- [ ] 把 MVP 20+ 张表的 schema 入库
- [ ] 业务人员（吕经理）审核枚举值标注
