# Requirements: P30 MCP 问答记录与质量评估系统

## Overview

在 Pipeline 层增加遥测记录层，全量捕获每次问答的用户问题、最终答案、工具调用链、性能指标（耗时/Token/费用/模型），并基于记录数据建立自动化质量评估流水线。

## Business Context

### 动机

现有评估（P21/P23/P26/P28）均为**离线一次性评估**——手动准备题目集 → 跑分 → 出报告。缺少对**线上真实用户问答**的持续监控：

1. 不知道每天用户问了多少问题、哪些问题多
2. 不知道线上回答质量如何，只能靠定期离线评估
3. P26 的分层归因依赖手工跑分，无法自动化
4. 双部署（阿里云 + Cloudflare）数据分散，无统一视图

P30 解决以上问题——为线上 MCP 问答建立持续监控基础设施。

## Objectives

1. 在 Pipeline 层无侵入地记录每次问答的完整链路数据
2. 本地 SQLite 即时写入 + 异步同步到 Supabase，支持双部署数据聚合
3. 基于记录数据建立自动化评估流水线（自动指标 + LLM-as-Judge + 抽样人工复核）
4. 产出可复用的评估数据，支撑 P26 的迭代和日常质量监控

## Scope

### In Scope

- Pipeline 层记录器（MCPRecorder），覆盖会话级 + 工具调用级数据
- SQLite 本地存储 + Supabase 同步
- 自动指标计算（工具成功率、轮数、延迟、成本）
- LLM-as-Judge 五维度自动评分
- 抽样人工复核流程
- 配置文件开关（启用/禁用、采样率、存储目标）

### Out of Scope

- 在 MCP Server 内部（工具级）加记录层（记录层只在 Pipeline）
- 评估仪表盘/Dashboard UI（先做数据+脚本，后续再加前端）
- 实时告警（后续迭代）
- Claude Code 本地直接调 MCP 的记录（仅在 Pipeline/部署版生效）

## Functional Requirements

### F1: 记录层（MCPRecorder）

- F1.1 会话开始时生成 session_id，记录 timestamp、source、user_question
- F1.2 每轮 function calling 的每个 tool_call 记录：tool_name、tool_args、result_size、latency_ms、success
- F1.3 会话结束时记录：final_answer、model、total_latency_ms、prompt_tokens、completion_tokens、total_tokens、cost_usd、round_count
- F1.4 记录写入 SQLite 必须是同步的（不丢数据），但不应显著增加 LLM 调用延迟
- F1.5 异常时记录 status=error 及错误信息，不丢失已捕获的数据
- F1.6 当 function calling 触达 MAX_TOOL_ROUNDS 上限时：
    - 兜底再调一次 LLM，`tool_choice="none"` 强制收敛
    - 兜底前追加 system 消息，要求基于已收集信息作答、信息不足时明确说明缺失项、禁止编造
    - 会话状态记为 `status="truncated"`，PipelineResult 同步暴露 `truncated=True`
    - 触发时向 stderr 输出告警（含 session_id），用于监控触发频率

### F2: 存储层

- F2.1 本地 SQLite 存储（`data/recorder.db`），schema 包含 sessions、tool_calls、evaluations 三张表
- F2.2 Supabase 异步同步（批量上传，后台任务，失败自动重试）
- F2.3 source 字段区分 `aliyun` / `cloudflare`
- F2.4 支持采样率配置（1.0=全量，0.1=10%采样）

### F3: 评估层

- F3.1 自动指标：tool_success_rate、avg_rounds、avg_latency_ms、avg_cost_usd
- F3.2 LLM-as-Judge 五维度评分（1-5）：事实准确性、具体性、业务落地性、来源可追溯、拒绝合理性
- F3.3 评分写入 evaluations 表，可迭代覆盖（同一 session_id + evaluator 组合）
- F3.4 支持批量评估脚本（评估指定时间范围的新记录）
- F3.5 人工复核接口：按条件抽选记录供人工评分，对比人机一致性

### F4: 配置

- F4.1 `MCP_RECORDER_ENABLED` — 总开关
- F4.2 `MCP_RECORDER_STORE` — sqlite / supabase / both
- F4.3 `MCP_RECORDER_SAMPLE_RATE` — 采样率
- F4.4 Supabase 连接配置（URL + KEY 从环境变量读取）

## Evaluation Dimensions

| 维度 | 评估方式 | 说明 |
|------|----------|------|
| 工具调用成功率 | 自动计算 | 成功 tool_call / 总数 |
| 查询效率 | 自动计算 | function calling 轮数 + 工具调用数 |
| 响应时间 | 自动计算 | 端到端延迟 ms |
| 成本效率 | 自动计算 | USD/问题，可按模型分组 |
| 兜底触发率 | 自动计算 | `status='truncated'` 占比，反映 MAX_TOOL_ROUNDS 是否够用 |
| 事实准确性 (1-5) | LLM-as-Judge | 数据、名称、事实是否正确 |
| 具体性 (1-5) | LLM-as-Judge | 是否包含具体数据 vs 笼统 |
| 业务落地性 (1-5) | LLM-as-Judge | 是否基于公司规则做判断 |
| 来源可追溯 (1-5) | LLM-as-Judge | 是否引用数据源/文档 |
| 拒绝合理性 (1-5) | LLM-as-Judge | 无法回答时是否正确告知 |

## Success Criteria

- [ ] Pipeline 层 MCPRecorder 集成完成，不对原有流程引入可感知延迟
- [ ] SQLite 本地存储 schema 就绪，可通过 SQL 查询按时间/来源/模型分组统计
- [ ] Supabase 同步链路跑通，阿里云 + Cloudflare 数据聚合可用
- [ ] 自动指标脚本可运行，产出按日/周/月的汇总统计
- [ ] LLM-as-Judge 评估脚本可运行，每条新记录自动评分
- [ ] 与 P26 分层评估集对接：P30 的记录可直接作为 P26 scorer 的输入

## Constraints & Assumptions

- Pipeline 层 (pipeline.py / MCPManager) 是唯一的集成点，两个 MCP Server 不修改
- SQLite 使用标准库 sqlite3，不引入新依赖
- Supabase 复用 AI-ALL 仓库已有的 Supabase 实例
- LLM-as-Judge 使用 DeepSeek（成本优先），模型可切换
- 记录频率：每条用户问答一条记录，预估每天几十到几百条

## Dependencies

- **AI-ALL / Supabase**: 复用已有的 Supabase Postgres 实例
- **P29 业务AI客户端**: Pipeline 所在的模块
- **P26 ERP MCP分层评估集**: 评估层复用其 LLM-as-Judge 评分模式
- **P18 样本问题收集**: 评估时的参考问题集

## Relationship to Other Specs

- **P21/P23**: 提供评估维度和方法论参考
- **P26**: P30 的记录数据可作为 P26 scorer 的持续输入，加分层层归因
- **P28**: P30 记录的模型/Token/成本数据可直接支撑模型对比
- **P29**: P30 的记录层集成在 P29 的 Pipeline 中
