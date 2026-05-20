# Tasks: P30 MCP 问答记录与质量评估系统

## Phase 1: 记录层 (recorder)

- [ ] P1.1 创建 `源代码/mcp-recorder/` 模块目录和 pyproject.toml
- [ ] P1.2 实现 `models.py` — Pydantic 数据模型 (SessionRecord, ToolCallRecord, EvalRecord)
- [ ] P1.3 实现 `config.py` — 配置管理（开关、采样率、存储目标）
- [ ] P1.4 实现 `store_sqlite.py` — SQLite 本地存储（schema 初始化 + CRUD）
- [ ] P1.5 实现 `recorder.py` — MCPRecorder 核心类（start_session / record_tool_call / end_session）
- [ ] P1.6 写 SQLite store 单元测试

## Phase 2: Pipeline 集成

- [ ] P2.1 在 pipeline.py (P29) 中集成 MCPRecorder
- [ ] P2.2 添加 Docker 部署的环境变量配置
- [ ] P2.3 阿里云部署验证（确认记录正常写入）
- [ ] P2.4 Cloudflare 部署验证
- [x] P2.5 MAX_TOOL_ROUNDS 兜底分支防幻觉加固：追加约束 system 提示、`status="truncated"` 入库、`PipelineResult.truncated` 透出、stderr 告警

## Phase 3: Supabase 同步

- [ ] P3.1 实现 `store_supabase.py` — Supabase 客户端（批量上传 + 重试）
- [ ] P3.2 Supabase 端创建表结构（复用 AI-ALL Supabase 实例）
- [ ] P3.3 实现 `flush_to_supabase()` — 异步同步逻辑
- [ ] P3.4 双部署数据聚合验证

## Phase 4: 评估流水线

- [ ] P4.1 实现自动指标计算脚本（SQL 聚合查询）
- [ ] P4.2 实现 LLM-as-Judge 评分脚本（复用 P26 scoring prompt）
- [ ] P4.3 实现 `sample_for_review.py` — 抽样人工复核脚本
- [ ] P4.4 实现 `import_reviews.py` — 人工评分导入脚本
- [ ] P4.5 与 P26 scorer 对接验证（P30 记录作为 P26 scorer 输入）

## Phase 5: 文档

- [ ] P5.1 写 README.md（模块说明 + 使用方式 + 配置说明）
- [ ] P5.2 更新 deploy/ 部署文档（新增环境变量说明）
