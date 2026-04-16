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

## Phase 8: P20S/P20T 整合（2026-04-15 实施）

目标：让 LLM 通过 MCP 工具调用路径自然发现并使用 P20S 的 schema 工具和 P20T 的 wiki 知识，从而让 P26 真实 MCP-level T1/T2 评估可执行。

- [x] 8.1 提升 `kingdee_get_schema` docstring 优先级：明确列出何时用、何时不用、与相邻工具的分工
- [x] 8.2 提升 `kingdee_get_relations` 和 `kingdee_list_cached_schemas` docstring：标注"V0.2 路由首选"
- [x] 8.3 降级 `kingdee_describe_form` docstring：加 ⚠️ 标记为"遗留兜底，不建议常用"；移除"不知道字段先调此工具"这类磁吸话术
- [x] 8.4 新增 `kingdee_get_wiki` 工具（`src/tools/wiki.py` + 注册到 `src/server.py`）：暴露 P20T wiki/ 的业务语义层；支持 topic="" 列目录 + topic="财务/应收应付" 读正文；路径穿越防护
- [x] 8.5 更新 `CLAUDE.md` V0.2 路由：wiki 访问改走 `kingdee_get_wiki`，明确禁止文件系统 Read
- [x] 8.6 刷新 q001 / q013 示范答案：在"查询过程"段落显式展示 6 步路由（schema → wiki → relations → query），q013 附加"为什么 wiki 必须先于 schema"的说明
- [ ] 8.7 **跑 P26 real MCP-level T1**（46 题，走真实 harness），与 LLM-level T1 的 0.829 ceiling 做 gap 分析
- [ ] 8.8 若 gap > 0.10，迭代 docstring / CLAUDE.md
- [ ] 8.9 **跑 P26 T2**（wiki 集成后），重点看 L7 refusal 能否 0.833 → ≥0.95
- [ ] 8.10 重跑 P23 28 题作为头条指标校验，预期 82% → ≥85% 且 Q013 由 Vanilla-win 翻为 MCP-win

### 8.x 注意事项

- 所有改动不改变旧工具的参数/返回，仅调整 docstring 和新增工具，对现有 Claude Desktop 配置零兼容影响
- `kingdee_get_wiki` 实际是文件系统读取，未来若有高频 wiki 内容可考虑预渲染到 `wiki/index.json` 加速
- P20E 不负责 wiki 内容本身（那是 P20T 的 Phase 4 持续工作），只负责"让 LLM 能到达"
