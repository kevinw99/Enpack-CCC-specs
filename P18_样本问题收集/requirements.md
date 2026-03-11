# Requirements: 样本问题收集 (Sample Question Collection)

## Overview

Systematically collect and categorize real business questions that employees across departments would ask an AI assistant. These sample questions define the actual needs and use cases for the MCP knowledge base server (P20), and serve as input for knowledge gap analysis (P19).

The screenshot conversation (2/22) from 翁伟嘉 provides the first batch of examples — procurement approval, inventory analysis, supplier negotiation prep, and sales pricing decisions.

## Objectives

1. Collect 50-100 representative business questions across all major departments
2. Categorize questions by department, data source required, and complexity level
3. Identify the data systems and knowledge types each question requires
4. Create a structured question bank that drives P19 (gap analysis) and P20 (MCP development)

## Scope

### In Scope
- Questions from all major departments: procurement, sales, production, R&D, supply chain, finance, management
- Both routine operational questions and strategic analysis questions
- Mapping each question to required data sources (ERP, CRM, email, meeting records, inventory, futures data, external info, knowledge base docs)
- Chinese-language questions (reflecting actual user language)

### Out of Scope
- Building the system to answer the questions (that's P20)
- Actually connecting to data systems (that's a later implementation concern)
- Questions about personal/HR matters (focus on business operations)

## Success Criteria

- [ ] Minimum 50 sample questions collected
- [ ] Questions cover at least 5 different departments/functions
- [ ] Each question is tagged with: department, data sources needed, complexity (simple/medium/complex), answer type (lookup/analysis/recommendation)
- [ ] Question bank reviewed and validated by stakeholders
- [ ] Questions are stored in a structured format (markdown table or JSON) for downstream use

## Constraints & Assumptions

- Primary language for questions is Chinese (matching actual user context)
- Questions should reflect realistic scenarios that employees face daily
- Some questions may require data that doesn't exist yet in any system — that's OK, it feeds P19
- Initial collection can be from chat transcripts, interviews, and brainstorming

## Dependencies

- Access to department heads or representatives for question elicitation
- Screenshot conversation provides seed examples
- Knowledge base index (知识库导航索引.md) for understanding current coverage

## Questions & Clarifications

- Should we prioritize CCC (复合集流体) questions or also include metal packaging (金属包装) questions?
- Are there existing chat logs or meeting notes we can mine for more question examples?
- What is the timeline for the first collection round?
