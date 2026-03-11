# Design: 样本问题收集 (Sample Question Collection)

## Approach

Use a structured elicitation process to collect business questions, starting from the seed examples in the 2/22 screenshot and expanding through department interviews and scenario workshops.

## Question Schema

Each collected question is stored with the following metadata:

```
| Field | Type | Description |
|-------|------|-------------|
| id | Q-###  | Unique identifier |
| question_zh | string | The question in Chinese |
| question_en | string | English translation |
| department | enum | 采购/销售/生产/研发/供应链/财务/管理 |
| scenario | string | Business scenario triggering the question |
| data_sources | list | Required data: ERP, CRM, 邮件, 会议记录, 库存, 期货, 外部信息, 知识库 |
| complexity | enum | simple / medium / complex |
| answer_type | enum | lookup / analysis / recommendation |
| kb_coverage | enum | full / partial / none |
| priority | enum | high / medium / low |
| source | string | Where the question came from |
```

## Seed Questions (from 2/22 Screenshot)

### Q-001: 采购审批合理性
**场景**: 有一份采购申请买入卡尺1支
**问题**: 我可以调阅这个人买过几支卡尺，这个部门有多少支卡尺，购买的是否合理。
- **Department**: 采购
- **Data Sources**: ERP(采购记录), ERP(资产台账), ERP(部门资产)
- **Complexity**: medium
- **Answer Type**: analysis

### Q-002: 原材料采购量分析
**场景**: 采购要买入10吨氧化铜
**问题**: 我可以调取到氧化铜的现有库存对应的订单需求情况，根据期货走势分析买入10吨是多了还是少了，是否合理。
- **Department**: 采购
- **Data Sources**: ERP(库存), ERP(订单), 期货数据(外部), 历史采购记录
- **Complexity**: complex
- **Answer Type**: recommendation

### Q-003: 供应商谈判准备
**场景**: 我要和供应商谈判
**问题**: 我可以调取之前和这位供应商的会议记录、往来邮件和信息、合作次数和每次合作的表现，该供应商的外网信息评价、在产业链内的优势劣势，来为我提供谈判的信息。
- **Department**: 采购/供应链
- **Data Sources**: 会议记录, 邮件系统, CRM(合作记录), 外部信息(企业信用/评价), 行业分析
- **Complexity**: complex
- **Answer Type**: analysis

### Q-004: 销售定价决策
**场景**: 销售申请用5元的价格卖出10万平米的MA
**问题**: 我可以快速的分析这个价格对于我们目前的成本是否值得去做，还有这个客户是否值得去合作等等......
- **Department**: 销售
- **Data Sources**: ERP(成本数据), ERP(定价历史), CRM(客户档案), 利润率分析模型
- **Complexity**: complex
- **Answer Type**: recommendation

## Collection Methods

### Method 1: Chat Mining (Immediate)
- Extract questions from existing chat logs, WeChat groups, meeting transcripts
- Source: 翁伟嘉 conversation (already started), other department chats

### Method 2: Department Interviews (Week 1-2)
- Structured interviews with department heads/key users
- Guide: "What questions do you wish you could instantly get answers to?"
- Focus on daily operational decisions and recurring analysis needs

### Method 3: Scenario Workshop (Week 2-3)
- Walk through common business processes end-to-end
- At each decision point, ask: "What information would help here?"
- Processes: procurement approval flow, sales quotation, production planning, supplier evaluation

### Method 4: Pain Point Mapping (Ongoing)
- Cross-reference with 知识库/04_运营分析/当前运营痛点分析.md
- For each pain point, derive the questions people would ask

## Output Structure

Questions stored in: `规格/P18_样本问题收集/question-bank.md`

Organized by department, with summary statistics at the top.

## Key Decisions

- **Bilingual**: Questions collected in Chinese (natural) with English translations (for spec consistency)
- **Structured metadata**: Every question gets full metadata to enable systematic gap analysis in P19
- **Living document**: Question bank grows over time, not a one-shot exercise

## Risk Mitigation

- Risk: Questions too abstract → Mitigation: Always require a concrete scenario
- Risk: Only collecting from one department → Mitigation: Systematic coverage checklist across all departments
- Risk: Collecting questions we can never answer → Mitigation: Tag feasibility level, accept "aspirational" questions as input for roadmap
