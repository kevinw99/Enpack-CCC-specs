# P17: 仓库重构 — 对齐 Base + OpenClaw 模式

## Overview

Restructure the Enpack_CCC repository to follow the same three-layer architecture as the openclaw fork: **core project (Enpack_CCC)** + **base template (ai-project-base)** + clear file ownership boundaries. Eliminate code duplication with base, merge latest base updates, and verify session history integrity.

## Background

The openclaw repo establishes a clean pattern:

| Layer | Remote | Owns | Edit where? |
|-------|--------|------|-------------|
| **Base** | `base` (ai-project-base) | `PROJECT_GUIDELINES.md`, `WORK_LOG.md`, `specs/00_template/`, `src/session_history/`, `.claude/commands/{log,history}.md`, `.claude/skills/{log,history,create-task}.md`, `.claude/settings.json`, `.gitignore` | In `~/AI/base`, pull via merge |
| **Project** | `origin` (this repo) | Everything else — specs, source code, knowledge base, research, docs, project-specific commands/skills | In this repo |

Enpack_CCC currently has:
- Base remote configured and active (`base` → ai-project-base)
- Base files merged in, but **no REPO_GUIDE.md** documenting file ownership
- One project-specific command (`/process`) not in base — correct
- `.session-history.json` — project-specific config — correct
- `源代码/session-persistence/` — old JS session persistence (P03), potentially overlaps with `src/session_history/` from base
- Base is 2 commits behind (`fb5cf9e` — incremental scan merge + uncategorized replay)

## Objectives

1. **Create REPO_GUIDE.md** — Document the two-layer structure (no upstream, unlike openclaw which has three layers)
2. **Merge latest base** — Pull `base/main` (fb5cf9e) into this repo
3. **Resolve any conflicts** — Ensure base merge is clean
4. **Audit for code duplication** — Identify and eliminate any code that duplicates base functionality
5. **Verify session history** — Run full scan/replay cycle to confirm no regressions

## Scope

### In Scope
- Create `REPO_GUIDE.md` documenting file ownership
- Merge latest `base/main`
- Resolve merge conflicts if any
- Audit `源代码/session-persistence/` vs `src/session_history/` overlap
- Audit `.claude/` for any files that should be base-owned but were modified locally
- Run `/history scan` and `/history replay` to verify integrity
- Update `.session-history.json` if needed for compatibility

### Out of Scope
- Renaming existing spec directories (P01-P16 are stable)
- Changing the Chinese directory naming convention (it's project-specific and correct)
- Modifying base code (any base fixes go to ~/AI/base first)
- Restructuring knowledge base or research directories

## Success Criteria

- [ ] `REPO_GUIDE.md` exists and documents file ownership clearly
- [ ] `git log --oneline base/main..HEAD` shows base/main is fully merged
- [ ] No duplicate code between `src/session_history/` (base) and project-specific code
- [ ] `/history scan` completes without errors
- [ ] `/history replay` for at least 3 entities generates valid replay files
- [ ] All base-owned files match base/main exactly (no local modifications)

## Constraints

- Must not break existing session history data
- Must preserve all 16 existing spec directories
- Must keep `.session-history.json` project-specific config intact
- Base files must only be modified in ~/AI/base repo
