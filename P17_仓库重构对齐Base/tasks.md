# P17: Tasks — 仓库重构对齐 Base

## Phase 1: Audit & Document

- [ ] 1.1 Compare all base-owned files: diff this repo vs base/main for each file
- [ ] 1.2 Check if `.claude/settings.json` has diverged from base
- [ ] 1.3 Audit `源代码/session-persistence/` — confirm it's distinct from base's session_history
- [ ] 1.4 Create `REPO_GUIDE.md` following openclaw's pattern (two-layer version)

## Phase 2: Merge Latest Base

- [ ] 2.1 `git merge base/main` — merge 2 new commits (fb5cf9e)
- [ ] 2.2 Resolve any merge conflicts
- [ ] 2.3 Verify all base-owned files match base/main after merge

## Phase 3: Clean Up Overlaps

- [ ] 3.1 Revert any locally-modified base-owned files to base version
- [ ] 3.2 Remove any project code that duplicates base functionality
- [ ] 3.3 Verify `/process` command is intact (project-specific)
- [ ] 3.4 Verify `.session-history.json` is compatible with latest base session_history code

## Phase 4: Verify Session History

- [ ] 4.1 Run `/history scan` — full scan, check for errors
- [ ] 4.2 Run `/history stats` — record baseline numbers
- [ ] 4.3 Run `/history replay` for 3+ entities — verify replay files generated
- [ ] 4.4 Run `/history list` — verify entity classification is correct
- [ ] 4.5 Spot-check replay content for correctness

## Phase 5: Final Verification

- [ ] 5.1 Run `git diff base/main -- <base-owned-files>` — should be empty
- [ ] 5.2 Run `/log` command — verify it works
- [ ] 5.3 Commit all changes with clear message
- [ ] 5.4 Update P17 status.md
