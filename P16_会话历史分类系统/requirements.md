# Requirements: 会话历史分类系统

## Overview
Python tool to parse Claude Code JSONL session files, classify conversations by project entity (specs, source projects, research topics), and generate interactive HTML + Markdown replays with search/filter capabilities.

## Objectives
- Parse all Claude Code session JSONL files (~15MB across 15+ sessions)
- Classify sessions by entity using file paths, text patterns, and keywords
- Store lightweight pointer indexes (no data duplication) under each entity's `history/` directory
- Generate interactive single-file HTML replays with dark theme, search, and filtering
- Generate clean Markdown replays for offline reading
- Provide CLI for scan, replay, search, list, and stats commands

## Scope
**Included:**
- JSONL parsing with streaming support for large files
- Multi-signal classification (file paths, text patterns, keywords)
- Six entity categories: specs, source projects, research, knowledge base, tools, uncategorized
- Interactive HTML replay (single-file, no external deps)
- Markdown replay generation
- CLI with argparse
- Incremental scan mode
- Unit tests

**Excluded:**
- Real-time session monitoring
- External dependency requirements (stdlib only)
- Modifying original JSONL files

## Success Criteria
- [ ] All 15+ sessions scanned and classified
- [ ] Sessions correctly mapped to entities (specs, source projects, etc.)
- [ ] Interactive HTML replay opens in browser with search/filter/collapse
- [ ] CLI commands work: scan, replay, search, list, stats
- [ ] Zero external dependencies (stdlib + pytest for tests only)
- [ ] Incremental scan processes only modified files

## Constraints & Assumptions
- Python 3.8+ (stdlib only, no pip install required)
- JSONL files at `~/.claude/projects/-Users-kweng-AI-Enpack-CCC/`
- Sessions can belong to multiple entities
- Thinking blocks excluded by default in replays
- Pointer-based storage: no duplication of JSONL data

## Dependencies
- Claude Code JSONL session files
- Existing project directory structure (规格/, 源代码/, 研究/, 知识库/)
