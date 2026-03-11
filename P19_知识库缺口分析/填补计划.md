# 缺口填补计划 (Gap Fill Plan)

**Created**: 2026-03-08
**Based on**: gap-analysis-matrix.md
**Total Actions**: 20

---

## Immediate Actions (Week 1-2) — Content Gaps (Type A)

These can be done now without any system integration.

| # | Action | Owner Type | Questions | Effort | Dependencies |
|---|--------|-----------|-----------|--------|-------------|
| A1 | Write competitive product specs comparison table (性能参数对比表) — compare our composite copper/aluminum foil specs vs Jinmei, Shuangxing, Nuode, Baoming | Content Writer | Q-027, Q-012, Q-046 | 2-3 days | P08 competitor research |
| A2 | Write solid-state battery current collector adaptation analysis — requirements, gaps in our tech, needed R&D | Content Writer | Q-028 | 1-2 days | P09 tech roadmap research |
| A3 | Write international market entry requirements — certifications by region (Korea, Japan, EU, US), timeline, cost | Content Writer | Q-051 | 1-2 days | External research |
| A4 | Write dual-business synergy analysis — technology, customer, supply chain crossover between metal packaging and CCC | Content Writer | Q-048 | 1-2 days | KB 01/02 sections |
| A5 | Expand industry tech trends with latest developments (2025-2026 updates) | Content Writer | Q-032, Q-046 | 1 day | External research |

**Estimated total**: 7-10 days of content writing

---

## Short-term Actions (Week 3-6) — Data Integration (Type B)

These require P20 MCP server tools connecting to business systems.

| # | Action | Owner Type | Questions Served | Effort | Dependencies |
|---|--------|-----------|-----------------|--------|-------------|
| B1 | **ERP Inventory Tool** — query current stock levels, safety stock, days of supply | Data Engineer | Q-002, Q-033, Q-035, Q-036, Q-037 | 1-2 weeks | ERP API access |
| B2 | **ERP Order/Sales Tool** — query orders, sales data, delivery schedules | Data Engineer | Q-011, Q-013, Q-016, Q-018 | 1-2 weeks | ERP API access |
| B3 | **ERP Cost Tool** — query product costs, margins, budget execution | Data Engineer | Q-004, Q-010, Q-039, Q-041, Q-043 | 1-2 weeks | ERP API access |
| B4 | **CRM Customer/Supplier Tool** — query customer profiles, supplier scores, cooperation history | Data Engineer | Q-003, Q-005, Q-009, Q-011, Q-014, Q-015 | 1-2 weeks | CRM API access |
| B5 | **ERP Production Tool** — query production logs, yield data, equipment status | Data Engineer | Q-019, Q-020, Q-021, Q-025 | 1-2 weeks | ERP API access |

**Estimated total**: 5-10 weeks (can parallelize B1-B5)

**Critical prerequisite**: ERP and CRM API access must be authorized and documented. See `data-source-requirements.md`.

---

## Medium-term Actions (Week 7-12) — Capability Gaps (Type C)

These require analysis logic built on top of data tools.

| # | Action | Owner Type | Questions Served | Effort | Dependencies |
|---|--------|-----------|-----------------|--------|-------------|
| C1 | **Procurement Reasonableness Analyzer** — cross-reference purchase request vs historical purchases, department assets, and standards | AI Developer | Q-001, Q-002, Q-010 | 2-3 weeks | B1, B3 |
| C2 | **Pricing/Margin Calculator** — compute margins at different price points, compare vs historical, recommend accept/reject | AI Developer | Q-004, Q-040, Q-042 | 2-3 weeks | B2, B3 |
| C3 | **Delivery Risk Predictor** — assess order fulfillment risk based on inventory, WIP, and production capacity | AI Developer | Q-024, Q-035 | 2-3 weeks | B1, B2, B5 |
| C4 | **Executive Dashboard** — aggregate key metrics from all ERP modules into weekly brief | AI Developer | Q-045 | 3-4 weeks | B1-B5 |
| C5 | **Market Price Analyzer** — integrate futures/commodity price feeds, compare vs our purchase prices | AI Developer | Q-002, Q-006 | 2-3 weeks | B3, External API |

**Estimated total**: 12-16 weeks (sequential dependency on B-tier tools)

---

## Long-term / Deferred Actions

| # | Action | Owner Type | Questions Served | Effort | Dependencies | Priority |
|---|--------|-----------|-----------------|--------|-------------|---------|
| D1 | Email/meeting record search integration | Data Engineer | Q-003 | 2-3 weeks | Email system access | Low — privacy concerns |
| D2 | Patent database integration | Data Engineer | Q-030 | 2-3 weeks | Patent DB API | Medium |
| D3 | Lab experiment data integration | Data Engineer | Q-023, Q-029 | 3-4 weeks | Lab system access | Medium |
| D4 | HR system integration | Data Engineer | Q-047 | 1-2 weeks | HR system API | Low |
| D5 | Customs/logistics tracking integration | Data Engineer | Q-038 | 2-3 weeks | Logistics system API | Low |

---

## Action Summary by Owner Type

| Owner Type | Actions | Estimated Effort |
|-----------|---------|-----------------|
| Content Writer | A1-A5 | 7-10 days |
| Data Engineer | B1-B5, D1-D5 | 15-25 weeks |
| AI Developer | C1-C5 | 12-16 weeks |

---

## Implementation Roadmap

```
Week 1-2:   [A1-A5] Content writing (immediate, no blockers)
Week 3-4:   [B1-B5] Start ERP/CRM tool development (needs API access)
Week 5-6:   [B1-B5] Complete and test data tools
Week 7-8:   [C1-C2] Procurement analyzer + pricing calculator
Week 9-10:  [C3-C4] Delivery risk + executive dashboard
Week 11-12: [C5] Market price analyzer + iteration
Week 13+:   [D1-D5] Deferred integrations as resources allow
```

## Feedback Loop

After each tier of actions is complete:
1. Rerun P18 question bank through updated MCP → measure coverage improvement
2. Update this fill plan with new gaps discovered
3. Feed findings to P21 (MCP Q&A quality evaluation) for formal benchmarking
