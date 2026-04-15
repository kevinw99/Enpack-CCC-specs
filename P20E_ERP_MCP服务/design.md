# Design: P20E ERP MCP 服务

> **Retrofit spec**: 此设计文档反映 `源代码/mcp-kingdee-server/` 的实际架构。

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│  Claude Desktop / Claude Code / 其他 MCP 客户端  │
└─────────────────────┬───────────────────────┘
                      │ MCP (stdio)
                      ▼
┌─────────────────────────────────────────────┐
│            mcp-kingdee-server                │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │  Kingdee Module  │  │  Futures Module  │  │
│  │  (金蝶 ERP)      │  │  (AkShare 期货)  │  │
│  └────────┬─────────┘  └────────┬─────────┘  │
│           │                      │            │
│    kingdee_client          akshare client     │
└───────────┼──────────────────────┼────────────┘
            │                      │
            ▼                      ▼
   金蝶云星空 REST API        AkShare 公开接口
```

## Module Layout

```
src/
├── server.py              # MCP 入口（整合两个模块）
├── kingdee_client.py      # 金蝶 HTTP 客户端 + 签名/认证
├── models.py              # 金蝶数据模型 (Pydantic)
├── tools/                 # 金蝶工具模块
│   ├── __init__.py
│   ├── common.py          # 通用查询 + 表单元数据
│   ├── master_data.py     # 物料档案
│   ├── inventory.py       # 即时库存
│   ├── purchase.py        # 采购申请 + 审批分析
│   └── fixed_assets.py    # 固定资产
└── futures/               # 期货模块（完全独立）
    ├── __init__.py
    ├── models.py
    ├── client.py
    └── tools.py
```

**模块解耦原则**:
- 金蝶模块与期货模块互不依赖
- 期货模块可单独剥离使用
- 所有工具通过 `server.py` 统一注册到 MCP 协议

## Tool Inventory

### ERP 工具（8 个）

| 工具名称 | 功能 | 关键字段/参数 |
|---------|------|-------------|
| `kingdee_query_bills` | 查询任意单据 | FormId, FilterString, FieldKeys |
| `kingdee_query_materials` | 物料档案 | FNumber, FName, FSpecification |
| `kingdee_query_inventory` | 即时库存 | FMaterialId, FStockId, FQty |
| `kingdee_query_purchase_requisition` | 采购申请 | FBillNo, FReqOrgId, FCreateDate |
| `kingdee_purchase_approval_analysis` | 采购审批合理性 | 内部规则引擎 |
| `kingdee_query_fixed_assets` | 固定资产 | FAssetNumber, FAssetName |
| `kingdee_list_forms` | 表单搜索 | keyword |
| `kingdee_describe_form` | 字段元数据 | FormId (⚠️ 返回 65KB) |

### 期货工具

| 工具名称 | 功能 |
|---------|------|
| 期货合约行情 | 主力合约价格 |
| 价格走势 | 历史 K 线/趋势 |
| 成本对比 | ERP 采购价 vs 市场价 |

## Authentication

金蝶云星空使用 AppSecret + Username 签名方案：

```
acct_id      ← 账套 ID
app_id       ← 开放平台 App ID
app_secret   ← App 密钥
username     ← 运行用户
server_url   ← k3cloud 服务地址
```

所有敏感信息通过 `.env` 文件注入，不入库。

## Client Configuration

用户通过 `setup_claude_config.py` 一键生成 Claude Desktop 配置：

```json
{
  "mcpServers": {
    "kingdee": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/mcp-kingdee-server",
      "env": { ... }
    }
  }
}
```

## Knowledge Layer (V0.1)

样本问题回答采用三文件协作：

```
样本问题库.md           ← 52 题题面（业务人员提供）
问题库回答指南.md        ← 人工维护的字段/状态值/业务规则
answer/q{编码}_answer.md ← AI 生成的具体答案（结论先行 + 分析 + 数据流）
```

**回答工作流**（见 CLAUDE.md）：

1. 读 `问题库回答指南.md` 了解数据流
2. 用 `kingdee_describe_form` 确认字段
3. 用 `kingdee_query_*` 取真实数据
4. 不清楚时向用户提问，答案要求可追溯
5. 每个数据点标注来源（ERP / 指南 / 推断⚠️待验证）
6. 答案按"结论先行 → 分析过程 → 数据流查询"三段组织

## Known Technical Debt

- T1: `describe_form` 65KB 响应 → 需要按需返回字段子集（V0.2 方向）
- T2: 业务语义（字段含义、状态值）只存在于指南文件，无结构化索引
- T3: 表单间关联关系（JOIN 路径）未显式建模
- T4: 没有自动化的答案质量回归测试（由 P23 评估规格处理）
