# Requirements: MCP问答质量评估 (MCP Q&A Quality Evaluation)

## Overview

Evaluate the quality of answers produced by the MCP knowledge base server (P20) compared to a vanilla LLM (same model, no MCP tools). This provides objective evidence of whether the MCP-augmented system actually delivers better, more accurate, more actionable answers for Enpack business questions.

## Objectives

1. Design a repeatable evaluation framework for comparing MCP-augmented vs vanilla LLM answers
2. Build a test harness that runs the same questions through both configurations
3. Measure answer quality on multiple dimensions (accuracy, specificity, relevance, actionability)
4. Produce a quantitative scorecard showing MCP value-add
5. Identify question types where MCP adds the most (and least) value

## Scope

### In Scope
- Evaluation of P20 MCP server answers vs same model without MCP tools
- Using P18 sample questions as the test set
- Multiple evaluation dimensions (see Success Criteria)
- Both automated metrics and human evaluation
- Analysis of failure modes (where MCP hurts or doesn't help)

### Out of Scope
- Evaluating different LLM models against each other
- Evaluating MCP against other RAG approaches (that's a separate study)
- Evaluating real-time data queries (Phase 3 of P20, not yet built)
- User satisfaction surveys (useful but separate from answer quality)

## Evaluation Dimensions

### Dimension 1: Factual Accuracy (准确性)
- Does the answer contain correct facts about Enpack/CCC?
- Does it avoid hallucinating company-specific information?
- Score: 1-5 scale

### Dimension 2: Specificity (具体性)
- Does the answer include specific data, numbers, names, or details from the KB?
- Or is it generic/vague?
- Score: 1-5 scale

### Dimension 3: Relevance (相关性)
- Does the answer directly address the question asked?
- Does it stay on topic without irrelevant tangents?
- Score: 1-5 scale

### Dimension 4: Actionability (可操作性)
- Can the user take a concrete action based on the answer?
- Does it provide enough context for decision-making?
- Score: 1-5 scale

### Dimension 5: Source Attribution (来源标注)
- Does the answer cite specific documents or data sources?
- Can the user verify the information?
- Score: 1-5 scale (MCP-only dimension — vanilla LLM gets N/A)

### Dimension 6: Hallucination Rate (幻觉率)
- Does the answer fabricate information that doesn't exist in the KB?
- Binary per-claim: hallucinated or grounded
- Metric: % of claims that are hallucinated

## Success Criteria

- [ ] Evaluation framework documented with clear scoring rubrics
- [ ] Test harness built that can run questions through both MCP and vanilla configurations
- [ ] At least 30 questions evaluated (from P18 question bank)
- [ ] Each question scored on all applicable dimensions by at least 1 evaluator
- [ ] Quantitative comparison report produced (average scores per dimension, win/loss/tie counts)
- [ ] Failure mode analysis completed (categories of questions where MCP underperforms)
- [ ] Recommendations for P20 improvement based on evaluation findings

## Constraints & Assumptions

- Same base model (Claude) used for both MCP and vanilla comparisons
- Vanilla baseline = same model with only the question (no system prompt with company info)
- MCP evaluation requires P20 Phase 1 to be functional
- Human evaluation is time-intensive; start with a representative subset
- Evaluation should be blind where possible (evaluator doesn't know which answer is MCP vs vanilla)

## Dependencies

- P18 (样本问题收集) — provides the test question set
- P20 (MCP知识库服务) — must be functional (at least Phase 1) to evaluate
- Access to Claude API for running vanilla baseline comparisons
- Evaluator(s) with domain knowledge to score answers

## Questions & Clarifications

- Who will be the human evaluators? Domain experts (翁伟嘉, other staff) or project team?
- Should we also measure response latency as a quality dimension?
- What is the minimum acceptable improvement to justify MCP investment?
- Should we test with different question phrasings (robustness testing)?
