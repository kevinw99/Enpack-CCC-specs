# Design: P29 业务AI客户端

## 架构

```
用户 → [Streamlit Web UI]
              ↓
       [Chat Controller]
              ↓
       [Router LLM (Flash)]  →  工具调用计划 (JSON)
              ↓
       [Tool Executor]
         ├─ KB MCP Tools (搜索/档案/产品/竞品/行业)
         └─ ERP MCP Tools (物料/库存/单据/资产/期货)
              ↓
       [Answerer LLM (Flash/Pro)]  →  最终回答
              ↓
       [UI 渲染: 回答 + 工具调用详情]
```

## 复用策略

直接复用现有代码：
- `源代码/rd_ai_tools/common/llm_client.py` — LLM 调用封装
- `规格/P28_模型MCP对比评估/compare.py` — 工具执行器、路由 prompt（经过验证）
- `源代码/mcp-kb-server/src/tools/` — KB 工具函数
- `源代码/mcp-kingdee-server/src/` — ERP 工具函数

新增：
- `源代码/ai-chat-client/app.py` — Streamlit 主应用
- `源代码/ai-chat-client/pipeline.py` — 聊天管道（路由 → 执行 → 回答）
- `源代码/ai-chat-client/config.py` — 客户端配置

## 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 前端 | Streamlit | 快速原型，Python 全栈，无需前端工程 |
| LLM Router | DeepSeek V4 Flash | P28 验证最佳性价比（19.7s/题, $0.0008/题） |
| LLM Answerer | DeepSeek V4 Flash (默认) | 可切换 Pro |
| KB 数据 | 直接调用工具函数 | 避免 MCP 协议开销 |
| ERP 数据 | 直接调用工具函数 | 同上 |

## UI 设计

### 主界面
```
┌─────────────────────────────────────────────┐
│  Enpack AI 助手                    ⚙️ 设置  │
├─────────────────────────────────────────────┤
│                                             │
│  👤 铜箔库存有多少？                         │
│                                             │
│  🤖 根据 ERP 数据，目前有 20 种铜箔物料...    │
│  ┌──────────────────────────────────┐       │
│  │ 📋 工具调用 (3 步)         [展开] │       │
│  │ 1. erp_materials("铜箔") ✅      │       │
│  │ 2. erp_inventory("CECE...") ✅   │       │
│  │ 3. erp_bills(STK_Inventory) ✅   │       │
│  │ ⏱ 12.3s  💰 $0.0003             │       │
│  └──────────────────────────────────┘       │
│                                             │
├─────────────────────────────────────────────┤
│  💬 输入问题...                    [发送]    │
└─────────────────────────────────────────────┘
```

### 侧边栏设置
- 模型选择: Flash / Pro / Hybrid
- 显示工具详情: 开/关
- 显示成本统计: 开/关

## 部署

采用 Cloudflare + 阿里云双部署架构，详见 [`AI-ALL/docs/leapbound-infra-plan.md`](../../../AI-ALL/docs/leapbound-infra-plan.md)。

### 环境一览

| 环境 | 入口 | 用途 |
|------|------|------|
| 阿里云 ECS (上海) | `http://47.116.176.127` | 国内用户，KB + ERP 全功能 |
| Cloudflare Containers | `https://enpack-ai-chat.kevinweng99.workers.dev` | 海外演示，KB only |

### 阿里云管理

- **ECS 控制台**: https://ecs.console.aliyun.com/
- 实例: ecs.e-c1m1.large, 2vCPU 2GiB, Ubuntu 22.04, 华东2 (上海)
- 部署目录: `/opt/enpack-ai-chat/`
- 容器: `enpack-ai-chat` (port 80→8501)

### 常用运维命令

```bash
# SSH 登录
ssh root@47.116.176.127

# 查看容器状态
docker ps

# 重启服务
cd /opt/enpack-ai-chat && docker compose restart

# 查看日志
docker logs enpack-ai-chat --tail 100 -f

# 重新部署（本地执行）
cd Enpack_CCC/deploy/domestic
./deploy-to-server.sh 47.116.176.127
```

### 部署流程与配置

构建脚本、Docker Compose、环境变量等详见：
- 本仓库: `deploy/domestic/` (阿里云) 和 `deploy/cloud/` (Cloudflare)
- 完整架构文档: `AI-ALL/docs/leapbound-infra-plan.md` §1–8
