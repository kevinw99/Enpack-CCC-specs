# 数据源需求文档 (Data Source Requirements)

**Created**: 2026-03-08
**Purpose**: Technical requirements for each external data source needed by the P20 MCP server
**Feeds into**: P20 MCP知识库服务 (Phase 2: Structured Data)

---

## Data Source Priority Ranking

| Priority | Data Source | Questions Dependent | P20 Tool Mapping |
|----------|-----------|-------------------|-----------------|
| 1 | ERP — 库存模块 | 5 questions | `query_inventory` |
| 2 | ERP — 销售/订单模块 | 4 questions | `query_orders`, `query_sales` |
| 3 | ERP — 成本/财务模块 | 5 questions | `query_costs`, `query_financials` |
| 4 | CRM — 客户/供应商 | 6 questions | `query_customer`, `query_supplier` |
| 5 | ERP — 生产模块 | 4 questions | `query_production` |
| 6 | External — 期货/市场价格 | 3 questions | `query_market_prices` |
| 7 | ERP — 采购模块 | 4 questions | `query_procurement` |
| 8 | ERP — 合同管理 | 1 question | `query_contracts` |

---

## DS-1: ERP System

### System Information
- **System name**: [To be confirmed — likely SAP, Kingdee, or UFIDA]
- **Deployment**: [On-premise / Cloud]
- **Modules needed**: Inventory, Sales, Finance/Cost, Production, Procurement, Contracts
- **Access method**: [API / Database query / Report export]

### Required Data Points

#### Inventory Module
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Current stock by material/product | Q-002, Q-033 | Real-time query |
| Safety stock levels | Q-033 | Configuration lookup |
| Stock aging / days of supply | Q-033, Q-037 | Calculated field |
| WIP (work in progress) | Q-035 | Real-time query |
| Inventory turnover by product | Q-037 | Calculated over period |

#### Sales/Order Module
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Order history by customer | Q-011 | Historical query |
| Order pipeline / backlog | Q-018, Q-035 | Real-time query |
| Sales by rep / product / period | Q-016 | Aggregate query |
| Accounts receivable by customer | Q-013 | Real-time query |
| Delivery schedule | Q-018, Q-035 | Real-time query |

#### Cost/Finance Module
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Product cost breakdown (material, labor, energy, depreciation) | Q-039 | Period query |
| Product margins | Q-004, Q-040 | Calculated |
| Budget vs actual by department | Q-010, Q-043 | Period query |
| Cash flow summary | Q-041 | Period query |
| AR/AP days outstanding | Q-041 | Calculated |

#### Production Module
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Production order status | Q-018 | Real-time query |
| Yield rate by line / period | Q-019, Q-025 | Aggregate query |
| Equipment downtime log | Q-020 | Historical query |
| Capacity utilization by line | Q-021 | Calculated |
| Material consumption vs standard | Q-022 | Variance query |
| Production schedule | Q-024, Q-035 | Real-time query |

#### Procurement Module
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Purchase history by item/person/dept | Q-001 | Historical query |
| Purchase price history by material | Q-006 | Time series query |
| Supplier on-time delivery rate | Q-009 | Aggregate query |
| Contract expiry dates | Q-007 | Lookup query |

### Access Requirements
- **Read-only access**: All MCP queries are read-only. No write operations.
- **Authentication**: Service account with minimum necessary permissions
- **Rate limiting**: Expect ~100 queries/day during normal use, bursts during evaluation
- **Data freshness**: Ideally real-time; daily sync acceptable for initial phase
- **Security**: Data must not leave the corporate network; MCP runs locally

---

## DS-2: CRM System

### System Information
- **System name**: [To be confirmed]
- **Deployment**: [On-premise / Cloud / WeChat-based]

### Required Data Points
| Data Point | Used By | Access Pattern |
|-----------|---------|---------------|
| Customer profile (name, industry, size, credit terms) | Q-004, Q-014 | Lookup |
| Supplier profile (rating, history, capabilities) | Q-003, Q-005 | Lookup |
| Cooperation history (orders, performance scores) | Q-003 | Historical query |
| Customer complaints log | Q-015 | Historical query |
| Sales targets by rep | Q-016 | Period query |

### Access Requirements
- Same as ERP: read-only, service account, local network

---

## DS-3: External Market Data

### Data Sources
| Source | Data Point | Used By | Update Frequency |
|--------|-----------|---------|-----------------|
| Shanghai Futures Exchange | Copper futures prices | Q-002, Q-006 | Daily |
| LME | Aluminum prices | Q-006 | Daily |
| Industry price index | PET film, target material prices | Q-006 | Weekly/Monthly |
| Company credit databases (天眼查/企查查) | Supplier/customer credit info | Q-003, Q-014 | On-demand |

### Access Requirements
- **API access**: Free tier may suffice for daily price lookups
- **Cost**: Budget for commercial API if needed (天眼查 API ~¥5000/year)
- **Caching**: Cache daily prices locally to reduce API calls

---

## DS-4: Future Data Sources (Deferred)

| Source | Data Point | Questions | Blocker |
|--------|-----------|-----------|---------|
| Email system | Supplier correspondence history | Q-003 | Privacy, access policy |
| Meeting records | Meeting notes, decisions | Q-003 | Format, digitization |
| Lab/experiment DB | Test results, experiment parameters | Q-023, Q-029 | System existence unclear |
| HR system | Headcount, recruitment pipeline | Q-047 | Privacy, access policy |
| Customs/logistics | Shipment tracking, clearance status | Q-038 | Third-party system |
| Patent database | Patent filings and claims | Q-030 | External API cost |

---

## Action Items

1. **Confirm ERP system type and version** — needed to determine API approach
2. **Confirm CRM system type** — or whether customer data is in ERP
3. **Request read-only API/database access** to ERP for P20 MCP server
4. **Identify IT contact** who can provide API documentation and test credentials
5. **Evaluate external market data APIs** — test free tiers, estimate costs for paid tiers
