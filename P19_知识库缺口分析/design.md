# Design: 知识库缺口分析 (Knowledge Base Gap Analysis & Fill Plan)

## Approach

Three-pass analysis: (1) map questions to KB, (2) classify gaps, (3) prioritize and plan.

## Pass 1: Coverage Mapping

For each P18 question, assess current knowledge base coverage:

```
| Coverage Level | Definition | Example |
|----------------|------------|---------|
| FULL | KB has all info needed to answer | "What products does the company make?" → 产品组合.md |
| PARTIAL | KB has some info, but missing key data | "Is this purchase reasonable?" → Has product info but no purchase history |
| NONE | KB has no relevant info | "What's the futures trend for copper oxide?" → No futures data |
```

### Current Knowledge Base Inventory

| KB Section | Content Type | Estimated Question Coverage |
|------------|-------------|---------------------------|
| 01_公司档案 | Company profile, org structure, financials | Company background questions |
| 02_业务运营 | Products, customers, supply chain, market position | Business context questions |
| 04_运营分析 | Pain points, KPIs, performance metrics | Operational analysis questions |
| 05_行业背景 | Industry standards, market trends | Industry context questions |
| 研究/ | Pricing, competitor profiles, tech roadmap | Strategic analysis questions |

### What's Missing (Initial Assessment)

Based on the seed questions from P18, the following data types are NOT in the current KB:

| Data Type | Required For | Current Status |
|-----------|-------------|---------------|
| ERP transaction data | Purchase history, inventory, costs | Not connected |
| CRM data | Customer profiles, cooperation history | Not connected |
| Email/meeting records | Supplier relationship history | Not connected |
| Futures/market prices | Commodity price analysis | Not connected |
| External company info | Supplier/customer due diligence | Not connected |
| Historical approval records | Procurement pattern analysis | Not connected |

## Pass 2: Gap Classification

Three types of gaps:

### Type A: Content Gaps (can fill by writing documents)
- Missing knowledge base articles on topics we already know about
- Example: Detailed supplier evaluation criteria, cost structure breakdowns
- **Fill method**: Write new KB documents or expand existing ones
- **Effort**: Low to medium

### Type B: Data Gaps (need system integration)
- Questions requiring live/transactional data from business systems
- Example: Current inventory levels, purchase history, customer order records
- **Fill method**: Build MCP tools that query ERP/CRM/other systems
- **Effort**: High (requires API access, data mapping)

### Type C: Capability Gaps (need analysis logic)
- Questions requiring computation, trend analysis, or multi-source synthesis
- Example: "Is 10 tons too much?" requires inventory + orders + futures + trend analysis
- **Fill method**: Build analysis tools/prompts in the MCP server
- **Effort**: High (requires business logic implementation)

## Pass 3: Prioritization Matrix

Score each gap on two axes:

| | Low Difficulty | Medium Difficulty | High Difficulty |
|---|---|---|---|
| **High Impact** | DO FIRST | PLAN NEXT | STRATEGIC |
| **Medium Impact** | EASY WIN | SCHEDULED | DEFERRED |
| **Low Impact** | OPTIONAL | DEFERRED | SKIP |

**Impact criteria**: Frequency of related questions, business value of answers, number of departments affected
**Difficulty criteria**: Data availability, technical complexity, organizational barriers

## Output Deliverables

1. **gap-analysis-matrix.md** — Full mapping of questions to KB coverage with gap types
2. **fill-plan.md** — Prioritized action list with owners, effort, dependencies
3. **data-source-requirements.md** — Technical requirements for each external data source needed by the MCP

## Key Decisions

- **Pragmatic scope**: Focus on what the MCP can realistically access, not every possible question
- **Three gap types**: Content/Data/Capability distinction drives different fill strategies
- **Impact-driven priority**: Business value determines what gets filled first, not technical ease

## Risk Mitigation

- Risk: P18 questions not ready → Mitigation: Start with seed questions, iterate as more arrive
- Risk: Data system access unclear → Mitigation: Document requirements, flag blockers early
- Risk: Analysis paralysis → Mitigation: Timebox to 2 weeks, deliver actionable plan not perfect analysis
