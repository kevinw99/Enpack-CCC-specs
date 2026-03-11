# Specs Directory

This directory contains all project specifications and requirements.

## Naming Convention

- Format: `P##_descriptive-name` (public), `R##_descriptive-name` (restricted), or `A##_descriptive-name` (AI subsidiary)
- `P` = public repo (`规格/`), `R` = restricted repo (`RESTRICTED/规格/`), `A` = AI subsidiary repo (`AI子公司/规格/`)
- Numbers use a single global counter shared across all repos
- Use two-digit zero-padded numbers: P01, P02, ... R14, A15, P16, P17, etc.
- Next available number: 18

## Spec Template

Each spec directory should contain:

```
规格/P##_descriptive-name/
├── requirements.md   # What needs to be done
├── design.md         # How it will be done
├── tasks.md          # Detailed work items and breakdown
└── status.md         # Implementation progress (added when work begins)
```

### requirements.md
- Clear description of what needs to be done
- Success criteria
- Constraints and assumptions
- Any blocking issues or dependencies

### design.md
- Overall approach
- Key decisions and rationale
- Architecture or structure
- Technical details
- Alternative approaches considered

### tasks.md
- Detailed breakdown of work items
- Dependencies between tasks
- Estimated effort (if applicable)
- Organized logically or by priority

### status.md (created when work starts)
- Current overall status: Planning/In Progress/Complete/Blocked
- Completed work with dates
- Remaining work items
- Session notes for context continuity
- Testing/verification instructions
- Files that have changed

## Example Spec

See a new spec created with:

```bash
# This creates the directory structure and template files
claude "Create a new spec for [your topic]"
```

## Best Practices

1. **Write specs before implementation** - Define what, why, and how
2. **Keep specs focused** - One topic per spec directory
3. **Update status.md regularly** - Track progress for continuity
4. **Link related specs** - Cross-reference in design/requirements
5. **Archive completed specs** - Move to archive if no longer active
