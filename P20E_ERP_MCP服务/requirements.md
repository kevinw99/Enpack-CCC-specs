# Requirements: P20E ERP MCP 服务

> **Retrofit spec**: 此规格是对已完成开发的回顾性文档化，对应源码位于 `源代码/mcp-kingdee-server/`。

## Overview

为 Claude (及其他 MCP 客户端) 提供金蝶云星空 ERP 数据查询能力的 MCP Server，
并集成期货行情数据获取模块，支持采购决策、库存分析、成本对标等业务问答场景。

## Business Context

- 英联股份内部使用金蝶云星空作为 ERP 系统，数据涵盖采购、库存、固定资产、物料档案等
- 研发/采购决策需要基于 ERP 实时数据，但直接查询需要熟悉金蝶 API、表单编码、字段语义
- 通过 MCP 协议将 ERP 查询能力暴露给 LLM，业务人员可用自然语言提问得到数据支持
- 期货价格（铜、铝等）是原材料采购成本对标的重要参考，独立封装为 futures 模块

## Functional Requirements

### F1: 金蝶 ERP 数据查询
- F1.1 通用单据查询（任意表单）
- F1.2 物料档案查询
- F1.3 即时库存查询
- F1.4 采购申请单查询 + 审批合理性分析
- F1.5 固定资产查询
- F1.6 表单元数据查询（字段发现）
- F1.7 表单搜索（按名称/编码）

### F2: 期货行情数据
- F2.1 期货合约行情查询
- F2.2 价格走势分析
- F2.3 采购成本对比（ERP 采购价 vs 市场价）

### F3: 样本问题回答知识沉淀
- F3.1 样本问题库（52 题，覆盖 7 个部门）
- F3.2 人工维护的 `问题库回答指南.md`（字段映射、状态值枚举、业务规则）
- F3.3 逐题答案文档（`answer/q{编码}_answer.md`）
- F3.4 回答文档编写规范（结论先行 → 分析过程 → 数据流查询过程）

## Non-Functional Requirements

- **认证**: 金蝶 API App 签名 (acct_id / app_id / app_secret / username)
- **部署**: stdio MCP 协议，通过 `claude_desktop_config.json` 接入 Claude Desktop
- **运行环境**: Python ≥ 3.11
- **依赖**: mcp, httpx, pydantic, python-dotenv, akshare

## Success Criteria (已达成)

- ✅ 8 个 ERP 工具可用，支持任意表单查询
- ✅ 期货模块独立可用
- ✅ Claude Desktop 配置模板和 setup 脚本完成
- ✅ 10/52 题有答案文档（约 19%）
- ✅ 文档体系完整（README、使用手册、Claude Code MCP 配置指南等）

## Known Limitations

- L1: `kingdee_describe_form` 返回 65KB 全量字段，单次调用上下文消耗大（已做初步优化）
- L2: AI 在字段选择和状态值理解上不稳定（典型案例 Q013 反复修正 3 次）
- L3: 业务知识（字段含义、状态枚举）强依赖人工维护指南
- L4: 答案修正无自动反馈回路
- L5: 约 18 题无对应 ERP 数据（伪问题/数据缺口/线下数据）

## Relationship to Other Specs

- **P20E（本规格）**: 已完成的 MCP 服务器 + 样本问题回答 V0.1 方案
- **P20T_TextToSql**: V0.2 演进方向，用 LLM Wiki 或 Text2SQL 解决 L1-L4 瓶颈
- **P23_ERP_MCP问答质量评估**（main 分支）: 对本服务的问答质量评估
