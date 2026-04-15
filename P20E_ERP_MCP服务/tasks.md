# Tasks: P20E ERP MCP 服务

> **Retrofit spec**: 此 tasks 反映已完成工作和遗留任务。

## Phase 1: MCP Server 骨架 ✅ 已完成

- [x] 金蝶 API 客户端封装（签名、认证、HTTP）
- [x] Pydantic 数据模型定义
- [x] MCP server.py 入口 + 工具注册机制
- [x] stdio 协议接入
- [x] Claude Desktop 配置模板 + setup 脚本

## Phase 2: ERP 工具集 ✅ 已完成

- [x] `kingdee_query_bills` 通用单据查询
- [x] `kingdee_query_materials` 物料档案
- [x] `kingdee_query_inventory` 即时库存
- [x] `kingdee_query_purchase_requisition` 采购申请
- [x] `kingdee_purchase_approval_analysis` 审批分析
- [x] `kingdee_query_fixed_assets` 固定资产
- [x] `kingdee_list_forms` 表单搜索
- [x] `kingdee_describe_form` 字段元数据

## Phase 3: 期货模块 ✅ 已完成

- [x] AkShare 客户端封装
- [x] 期货行情查询工具
- [x] 价格走势分析工具
- [x] 采购成本对比工具
- [x] 模块独立性验证

## Phase 4: 文档体系 ✅ 已完成

- [x] `README.md` 项目说明
- [x] `docs/使用手册.md`
- [x] `docs/Claude_Code_MCP配置指南.md`
- [x] `docs/MCP工作原理详解.md`
- [x] `docs/ERP MCP建设现状.md`
- [x] `docs/期货数据MCP工具使用说明.md`
- [x] `docs/期货数据获取方案调研.md`
- [x] `docs/快速开始指南.md`
- [x] `CLAUDE.md` 回答规范

## Phase 5: 样本问题回答 🟡 进行中（10/52 = 19%）

- [x] 建立样本问题库（52 题）
- [x] 建立问题库回答指南
- [x] 建立 answer/ 答案目录
- [x] 完成 q001, q002, q004, q005, q006, q009, q011, q012, q013, q019
- [ ] 剩余可回答题目约 14 题（目标 24/52 ≈ 46%）
- [ ] 标注伪问题 / 数据缺口题（约 18 题）
- [ ] 标注线下数据题（约 5 题）

## Phase 6: 已知问题跟踪 🟡 待处理

- [ ] T1: `describe_form` 65KB 响应优化（按需返回字段子集）
- [ ] T2: 业务语义结构化（解决方案见 P20T_ERP_TextToSql）
- [ ] T3: 表单关联关系建模
- [ ] T4: Q013 式错误的自动化检测（由 P23 评估规格处理）

## Phase 7: 后续演进（不在本规格范围）

- 推进 P20T_ERP_TextToSql 设计落地
- 推进 P23_ERP_MCP问答质量评估 的评估框架
