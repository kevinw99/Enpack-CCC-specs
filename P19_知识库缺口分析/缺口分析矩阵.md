# 知识库缺口分析矩阵 (Gap Analysis Matrix)

**Created**: 2026-03-08
**Based on**: P18 Question Bank (52 questions)
**KB Snapshot**: 25 KB docs + 22 research docs

---

## Pass 1: Coverage Mapping

### Legend
- **Coverage**: FULL = KB can fully answer | PARTIAL = KB has some info | NONE = KB has no relevant info
- **Gap Type**: A = Content gap (write docs) | B = Data gap (system integration) | C = Capability gap (analysis logic)
- **Impact**: H = High | M = Medium | L = Low
- **Difficulty**: L = Low | M = Medium | H = High

---

### 采购部 (Procurement) — 10 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-001 | 采购审批合理性 | NONE | B | ERP采购记录, 资产台账, 部门资产 | H | H |
| Q-002 | 原材料采购量分析 | NONE | B+C | ERP库存, 订单, 期货数据, 历史采购 | H | H |
| Q-003 | 供应商谈判准备 | PARTIAL | A+B | 会议记录, 邮件, CRM合作记录; KB有部分行业分析 | H | H |
| Q-005 | 供应商价格对比 | PARTIAL | B | ERP采购价格, CRM供应商档案; KB有部分供应链信息 | H | M |
| Q-006 | 采购成本趋势 | NONE | B+C | ERP采购历史, 期货数据, 价格指数 | H | H |
| Q-007 | 采购合同到期提醒 | NONE | B | ERP合同管理 | M | M |
| Q-008 | 采购替代材料分析 | PARTIAL | A+C | KB有技术标准; 缺材料替代分析, 外部材料数据库 | M | M |
| Q-009 | 供应商交期达成率 | NONE | B | ERP收货记录, 采购订单 | M | M |
| Q-010 | 采购预算执行情况 | NONE | B | ERP采购订单, 财务预算 | M | M |

**Procurement summary**: 0 FULL, 3 PARTIAL, 7 NONE. Heavily dependent on ERP data.

---

### 销售部 (Sales) — 9 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-004 | 销售定价决策 | NONE | B+C | ERP成本, 定价历史, CRM客户档案, 利润模型 | H | H |
| Q-011 | 客户订单趋势 | PARTIAL | B | ERP订单记录; KB有U&S ENERGY基本信息 | H | M |
| Q-012 | 产品报价参考 | PARTIAL | B+A | ERP报价记录; KB有竞争对手部分信息, 缺行业报价 | H | M |
| Q-013 | 客户应收账款 | NONE | B | ERP应收账款, CRM客户信用 | H | M |
| Q-014 | 新客户开发分析 | PARTIAL | A | KB有行业背景和公司档案研究; 缺客户渗透率分析 | H | M |
| Q-015 | 客户投诉分析 | NONE | B | CRM投诉记录, ERP质检记录 | M | M |
| Q-016 | 销售目标达成 | NONE | B | ERP销售数据, CRM目标 | M | L |
| Q-017 | 产品交叉销售 | PARTIAL | B+C | CRM客户档案; KB有公司双主业信息 | M | M |

**Sales summary**: 0 FULL, 4 PARTIAL, 5 NONE. Needs ERP+CRM integration.

---

### 生产部 (Production) — 8 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-018 | 生产进度查询 | NONE | B | ERP生产工单, 排产计划 | H | M |
| Q-019 | 良率分析 | PARTIAL | B | ERP质检数据; KB有缺陷分类指南 | H | M |
| Q-020 | 设备故障与停机 | NONE | B | ERP设备维修记录, 生产日志 | H | M |
| Q-021 | 产能利用率 | PARTIAL | B | ERP生产数据; KB有产能规划基本信息 | H | M |
| Q-022 | 原材料消耗异常 | NONE | B+C | ERP物料消耗, 生产参数, 历史异常 | M | H |
| Q-023 | 工艺参数优化 | PARTIAL | B+C | ERP生产参数+质检; KB有部分研究数据 | M | H |
| Q-024 | 排产冲突 | NONE | B+C | ERP订单, 排产计划, 成本数据 | H | H |
| Q-025 | 班组绩效对比 | NONE | B | ERP生产记录, 质检数据 | L | M |

**Production summary**: 0 FULL, 3 PARTIAL, 5 NONE. Almost entirely ERP-dependent.

---

### 研发部 (R&D) — 7 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-026 | 技术标准查询 | FULL | — | KB has 技术标准综合, 测试程序指南, 缺陷分类 | H | — |
| Q-027 | 竞争对手技术对比 | PARTIAL | A | KB有公司档案研究; 缺产品性能参数对比表 | H | M |
| Q-028 | 固态电池材料需求 | PARTIAL | A | KB有技术路线图; 缺具体适配分析 | H | M |
| Q-029 | 实验数据查询 | NONE | B | 实验数据库 (不在KB中) | M | H |
| Q-030 | 专利和知识产权 | NONE | B | 内部专利库, 外部专利数据库 | M | H |
| Q-031 | 新产品开发进度 | NONE | B | 项目管理系统, 会议记录 | H | M |
| Q-032 | 行业技术趋势 | PARTIAL | A | KB有行业背景; 需要定期更新最新技术动态 | M | L |

**R&D summary**: 1 FULL, 3 PARTIAL, 3 NONE. Best KB coverage of all departments, but still needs lab data integration.

---

### 供应链/物流 (Supply Chain) — 6 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-033 | 库存预警 | NONE | B | ERP库存, 生产计划, 安全库存设定 | H | M |
| Q-034 | 物流成本分析 | NONE | B | ERP物流费用, 外部物流报价 | M | M |
| Q-035 | 交期风险评估 | NONE | B+C | ERP库存+在制品+排产+订单 | H | H |
| Q-036 | 供应链中断应对 | PARTIAL | B+A | ERP库存, CRM供应商; KB有供应链管理基本信息 | H | H |
| Q-037 | 成品库存周转 | NONE | B | ERP库存, 销售记录 | M | M |
| Q-038 | 进口材料通关 | NONE | B | 物流系统, 报关系统 | M | M |

**Supply Chain summary**: 0 FULL, 1 PARTIAL, 5 NONE. Heavily ERP-dependent.

---

### 财务部 (Finance) — 6 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-039 | 产品成本构成 | NONE | B | ERP成本核算, 生产数据 | H | M |
| Q-040 | 盈亏平衡分析 | PARTIAL | B+C | ERP成本+产能; KB有定价研究部分数据 | H | H |
| Q-041 | 现金流查询 | NONE | B | ERP财务数据, 应收应付 | H | M |
| Q-042 | 投资回报分析 | PARTIAL | B+C | ERP财务+订单; KB有公司概览中的投资金额 | H | H |
| Q-043 | 费用报销审核 | NONE | B | ERP费用系统, 预算 | L | L |
| Q-044 | 税务优惠利用 | PARTIAL | A+B | 财务数据; KB有企业资质信息 | M | M |

**Finance summary**: 0 FULL, 3 PARTIAL, 3 NONE. Needs ERP financial module integration.

---

### 管理层 (Management) — 6 questions

| ID | Question (short) | Coverage | Gap Type | Missing Data | Impact | Difficulty |
|----|-----------------|----------|----------|-------------|--------|-----------|
| Q-045 | 经营仪表盘 | NONE | B+C | ERP全模块汇总 | H | H |
| Q-046 | 战略方向评估 | PARTIAL | A | KB有行业背景和竞争对手档案; 缺最新动态 | H | M |
| Q-047 | 人力资源需求 | PARTIAL | B+A | HR系统; KB有组织结构 | M | M |
| Q-048 | 双主业协同分析 | PARTIAL | A+C | KB有公司概览和业务运营; 缺具体协同分析 | M | M |
| Q-049 | 风险预警 | PARTIAL | A+C | KB有战略重点和行业背景; 缺量化风险数据 | H | H |
| Q-050 | 政策与合规 | FULL | — | KB有GB38031-2025完整内容 | H | — |
| Q-051 | 国际市场拓展 | PARTIAL | A | KB有竞争对手档案; 缺海外市场认证要求 | H | M |
| Q-052 | 产能扩张决策 | PARTIAL | B+C | ERP订单+财务; KB有产能规划基本数据 | H | H |

**Management summary**: 1 FULL, 6 PARTIAL, 1 NONE. Best partial coverage (strategic content in KB), but needs data for quantitative analysis.

---

## Pass 2: Gap Classification Summary

### By Gap Type

| Gap Type | Description | Count | % of Gaps |
|----------|-------------|-------|-----------|
| **B** (Data only) | Need ERP/CRM/system integration | 23 | 46% |
| **B+C** (Data + Capability) | Need data + analysis logic | 12 | 24% |
| **A** (Content only) | Can fill by writing KB docs | 5 | 10% |
| **A+B** (Content + Data) | Need both new docs and data | 5 | 10% |
| **A+C** (Content + Capability) | Need docs + analysis | 3 | 6% |
| No gap (FULL) | KB can already answer | 2 | 4% |

### By Required Data Source

| Data Source | Questions Requiring It | Availability |
|------------|----------------------|-------------|
| **ERP** (all modules) | 42 / 52 (81%) | Not connected |
| **CRM** | 15 / 52 (29%) | Not connected |
| **External market data** (futures, industry) | 8 / 52 (15%) | Not connected |
| **Knowledge base** (existing docs) | 24 / 52 (46%) | Available via P20 MCP |
| **Research outputs** | 8 / 52 (15%) | Available via P20 MCP |
| **Email/meeting records** | 3 / 52 (6%) | Not connected |
| **Lab/experiment data** | 2 / 52 (4%) | Not connected |
| **HR system** | 1 / 52 (2%) | Not connected |

### Key Finding

**ERP is the #1 blocker.** 81% of questions require ERP data. The knowledge base alone can only fully answer 2 out of 52 questions. However, 24 questions can benefit from KB content as supplementary context even when ERP data is the primary source.

---

## Pass 3: Prioritization Matrix

### Priority 1: DO FIRST (High Impact, Low-Medium Difficulty)

These are Type A (content) gaps — can be filled immediately by writing new KB documents.

| Action | Questions Served | Effort |
|--------|-----------------|--------|
| A1: Write competitive product specs comparison table | Q-027, Q-012, Q-046 | 2-3 days |
| A2: Write solid-state battery adaptation analysis | Q-028 | 1-2 days |
| A3: Write international market certification requirements | Q-051 | 1-2 days |
| A4: Update industry tech trends quarterly | Q-032, Q-046 | 1 day/quarter |
| A5: Write dual-business synergy analysis | Q-048 | 1-2 days |

### Priority 2: PLAN NEXT (High Impact, Medium Difficulty)

Type B gaps requiring ERP read-only access.

| Action | Questions Served | Effort |
|--------|-----------------|--------|
| B1: ERP inventory query tool | Q-002, Q-033, Q-035, Q-037 | 1-2 weeks |
| B2: ERP order/sales query tool | Q-011, Q-013, Q-016, Q-018 | 1-2 weeks |
| B3: ERP cost data query tool | Q-004, Q-039, Q-040, Q-041 | 1-2 weeks |
| B4: CRM customer/supplier query tool | Q-003, Q-005, Q-011, Q-014 | 1-2 weeks |
| B5: ERP production data query tool | Q-019, Q-020, Q-021, Q-025 | 1-2 weeks |

### Priority 3: STRATEGIC (High Impact, High Difficulty)

Type B+C gaps requiring both data access and analysis logic.

| Action | Questions Served | Effort |
|--------|-----------------|--------|
| C1: Procurement reasonableness analyzer | Q-001, Q-002, Q-010 | 2-3 weeks |
| C2: Pricing/margin calculator | Q-004, Q-040, Q-042 | 2-3 weeks |
| C3: Delivery risk predictor | Q-035, Q-024 | 2-3 weeks |
| C4: Executive dashboard aggregator | Q-045 | 3-4 weeks |
| C5: Market price trend analyzer (futures) | Q-002, Q-006 | 2-3 weeks |

### Priority 4: DEFERRED (Medium/Low Impact)

| Action | Questions Served | Effort |
|--------|-----------------|--------|
| D1: Email/meeting record search | Q-003 (partial) | 2-3 weeks |
| D2: Patent database integration | Q-030 | 2-3 weeks |
| D3: Lab data integration | Q-029, Q-023 | 3-4 weeks |
| D4: HR system integration | Q-047 | 1-2 weeks |
| D5: Customs/logistics tracking | Q-038 | 2-3 weeks |
