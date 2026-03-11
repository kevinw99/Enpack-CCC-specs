# Spec Template

Use this as a guide when creating new specs.

## Directory Structure

```
规格/P##_your-topic-name/       # P = public, R = restricted
├── requirements.md
├── design.md
├── tasks.md
└── status.md (add when work begins)
```

## requirements.md Template

```markdown
# Requirements: [Topic Title]

## Overview
[What is this about? What problem does it solve?]

## Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Scope
[What's included? What's excluded?]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Constraints & Assumptions
- [Constraint/Assumption 1]
- [Constraint/Assumption 2]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Questions & Clarifications
- [Question 1]
- [Question 2]
```

## design.md Template

```markdown
# Design: [Topic Title]

## Approach
[How will this be done? What's the strategy?]

## Architecture / Structure
[Key components, organization, or structure]

## Key Decisions
- **Decision 1**: [Rationale]
- **Decision 2**: [Rationale]

## Technical Details
[Implementation approach, tools, technologies]

## Alternative Approaches
- **Alternative 1**: [Pros/cons]
- **Alternative 2**: [Pros/cons]

## Risk Mitigation
- Risk 1: [Mitigation strategy]
- Risk 2: [Mitigation strategy]
```

## tasks.md Template

```markdown
# Tasks: [Topic Title]

## Phase 1: [Phase Name]
- [ ] Task 1.1 - [description]
- [ ] Task 1.2 - [description]
- [ ] Task 1.3 - [description]

## Phase 2: [Phase Name]
- [ ] Task 2.1 - [description]
- [ ] Task 2.2 - [description]

## Phase 3: [Verification & Completion]
- [ ] Test task 3.1
- [ ] Documentation task 3.2
- [ ] Final verification 3.3

## Notes
- [Task notes, dependencies, or considerations]
```

## status.md Template

```markdown
# Status: [Topic Title]

## Current Status
**Overall**: In Progress
**Started**: [Date]
**Last Updated**: [Date]

## Completed Work
- [Date]: Task completed
- [Date]: Task completed

## Current Work
- Working on: [Task name]
- Estimated completion: [Date]

## Remaining Work
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Session Notes
### Session [Date]
- Accomplished: [What was done]
- Findings: [Key findings]
- Next steps: [What to do next]
- Blockers: [Any blockers]

### Session [Date]
- [Session notes]

## Files Changed
- [File 1]: [Changes]
- [File 2]: [Changes]

## Verification
How to verify this work is correct:
- [Verification step 1]
- [Verification step 2]
```

---

## How to Create a New Spec

1. Create a new directory: `规格/P##_descriptive-name/` (or `R##` for restricted)
2. Create three files: `requirements.md`, `design.md`, `tasks.md`
3. Fill them in using the templates above
4. When you start work, add `status.md` and track progress
5. Update `status.md` regularly with session notes

Numbers use a global counter shared across public (P) and restricted (R) repos. Check both repos for the next available number.
