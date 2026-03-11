# P17: Design — 仓库重构对齐 Base

## Approach

Follow the openclaw fork pattern: flat root with clear layer boundaries. Enpack_CCC is simpler than openclaw (two layers instead of three — no upstream).

## Target Structure

```
~/AI/Enpack_CCC/
│
│  ── From base (edit in ~/AI/base, pull here) ──
├── PROJECT_GUIDELINES.md        # Workflow conventions
├── WORK_LOG.md                  # Session work log
├── specs/00_template/           # Spec templates
├── specs/README.md              # Spec index
├── src/session_history/         # Session history tool (Python)
├── .claude/commands/log.md      # /log command
├── .claude/commands/history.md  # /history command
├── .claude/commands/README.md   # Commands docs
├── .claude/skills/log.md        # Log skill
├── .claude/skills/history.md    # History skill
├── .claude/skills/create-task.md # Task scaffolding skill
├── .claude/skills/README.md     # Skills docs
├── .claude/settings.json        # Hooks config
├── .gitignore                   # Ignore rules
│
│  ── Project-specific (edit here) ──
├── REPO_GUIDE.md                # ← NEW: File ownership documentation
├── README.md                    # Project README
├── .session-history.json        # Entity config for session_history
├── .claude/commands/process.md  # /process command (project-specific)
├── 规格/P01-P16.../             # Project specs (Chinese convention)
├── 源代码/                       # Project source code
├── 知识库/                       # Knowledge base
├── 研究/                         # Research
├── 文档/                         # Documentation
├── 会话历史/                     # Session history storage
├── AI同步数据源/                  # Data sync sources
├── .kiro/                        # Archive of previous work
└── package.json, jest.config.js  # Node tooling
```

## Key Decisions

### Decision 1: Two-layer model (not three)
**Rationale**: Enpack_CCC has no upstream project to fork from. It IS the core project. So we only have `base` + `project` layers, unlike openclaw which has `base` + `upstream` + `project`.

### Decision 2: Keep `源代码/session-persistence/` as archived project code
**Rationale**: This was P03's implementation — a JavaScript-based session capture tool. It's historically distinct from base's `src/session_history/` (Python classification/replay tool). They solve different problems:
- `源代码/session-persistence/` — captures sessions in real-time (P03, JavaScript)
- `src/session_history/` — classifies and replays captured sessions (base, Python)

Keep it as project-specific code, but note the relationship in REPO_GUIDE.md.

### Decision 3: `.claude/settings.json` ownership
**Rationale**: Base provides the template settings.json (with /log stop hook). This project may add project-specific hooks. Currently both should be identical in structure. If the project needs custom hooks, they should be additive — base provides the foundation, project can extend.

**Current state**: Need to verify if Enpack_CCC's settings.json has diverged from base's version.

### Decision 4: `specs/` vs `规格/` coexistence
**Rationale**: Base owns `specs/00_template/` and `specs/README.md`. Project uses `规格/` for its own specs. These are separate directories and don't conflict. Keep both.

## Implementation Plan

### Phase 1: Audit & Document (no code changes)
1. Compare base-owned files between this repo and base/main
2. Identify any local modifications to base-owned files
3. Check `源代码/session-persistence/` for any code that should be in base
4. Create REPO_GUIDE.md

### Phase 2: Merge Latest Base
1. `git merge base/main` — pull 2 new commits (incremental scan + uncategorized replay)
2. Resolve any conflicts
3. Verify merged files match base/main

### Phase 3: Clean Up Overlaps
1. If any base-owned files were modified locally, revert to base version
2. If any project code duplicates base functionality, remove the duplicate
3. Ensure `/process` command stays as project-specific

### Phase 4: Verify Session History
1. Run `python3 -m session_history scan` — full scan
2. Check categorization report
3. Run `python3 -m session_history replay` for several entities
4. Verify replay files are generated correctly
5. Run `python3 -m session_history stats` — confirm no regressions

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Merge conflicts with base | Work on clean branch, resolve carefully |
| Session history data loss | Run scan before and after, compare stats |
| Breaking existing workflows | Test /log, /history, /process commands after changes |
| .session-history.json incompatibility | Check base's new code handles project config correctly |
