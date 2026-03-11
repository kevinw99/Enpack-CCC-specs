# Tasks: MCP问答质量评估 (MCP Q&A Quality Evaluation)

## Phase 1: Framework Setup
- [ ] Task 1.1 - Finalize evaluation dimensions and scoring rubric
- [ ] Task 1.2 - Select test question subset from P18 (30-50 questions)
- [ ] Task 1.3 - Design blind evaluation protocol (randomization, label assignment)
- [ ] Task 1.4 - Create evaluation spreadsheet/template for human scorers

## Phase 2: Test Harness
- [ ] Task 2.1 - Build test harness script (run questions through vanilla + MCP configs)
- [ ] Task 2.2 - Implement Config A: vanilla Claude API call
- [ ] Task 2.3 - Implement Config B: Claude with MCP tools (P20 server)
- [ ] Task 2.4 - Implement Config C (optional): vanilla + company info system prompt
- [ ] Task 2.5 - Implement automated metrics (grounding score, specificity score, length)
- [ ] Task 2.6 - Generate answer pairs for all test questions

## Phase 3: Evaluation
- [ ] Task 3.1 - Run automated metrics on all answer pairs
- [ ] Task 3.2 - Conduct human evaluation (blind scoring on 4 dimensions)
- [ ] Task 3.3 - Compile scores into evaluation-results.md
- [ ] Task 3.4 - Calculate aggregate statistics (averages, win rates, confidence intervals)

## Phase 4: Analysis & Reporting
- [ ] Task 4.1 - Build scorecard comparing MCP vs vanilla across all dimensions
- [ ] Task 4.2 - Analyze failure modes (where MCP didn't help or hurt)
- [ ] Task 4.3 - Identify question categories with strongest MCP advantage
- [ ] Task 4.4 - Write recommendations for P20 improvement
- [ ] Task 4.5 - Write recommendations for KB content additions (feedback to P19)
- [ ] Task 4.6 - Present findings to stakeholders

## Phase 5: Iteration
- [ ] Task 5.1 - Apply P20 improvements based on evaluation findings
- [ ] Task 5.2 - Re-run evaluation on problem questions to verify improvement
- [ ] Task 5.3 - Update scorecard with post-improvement results

## Notes
- Phase 1 can start now (framework design doesn't need P20)
- Phase 2-3 requires P20 Phase 1 to be functional
- Phase 3 requires human evaluators with domain knowledge
- Consider running evaluation again after each major P20 update
- Keep evaluation data versioned for longitudinal comparison
