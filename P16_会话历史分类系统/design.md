# Design: 会话历史分类系统

## Approach
Pointer-based storage model: JSON indexes with message UUIDs + line numbers reference original JSONL files. HTML/Markdown replays generated on demand from original data. No data duplication.

## Architecture

```
源代码/session_history/
  __init__.py
  main.py                    # CLI entry point
  requirements.txt           # pytest only
  config/
    settings.py              # Settings dataclass
    entity_registry.py       # Auto-discover entities from project structure
  models/
    session.py               # Session, SessionMessage dataclasses (incl. cwd field)
    category.py              # EntityType, Entity, EntityMatch
    index.py                 # EntityIndex, SessionReference, MessagePointer
    turn.py                  # Turn dataclass (user prompt + AI response)
  parser/
    jsonl_reader.py          # Streaming JSONL parser
    message_extractor.py     # Extract text, file paths from messages
  classifier/
    file_path_signal.py      # Score from tool_use file paths (weight: 0.50)
    text_pattern_signal.py   # Score from regex patterns (weight: 0.35)
    keyword_signal.py        # Score from entity name/keyword (weight: 0.15)
    composite_classifier.py  # Combine signals with configurable weights
    turn_entity_classifier.py  # Turn-level entity detection for multi-spec splitting
  generator/
    html_generator.py              # Single-file HTML with inline CSS+JS
    markdown_generator.py          # Raw Markdown replay (--raw mode)
    readable_replay_generator.py   # Turn-based per-session Markdown files (default)
    replay_index_generator.py      # Generate replay-index.md TOC files
    turn_extractor.py              # Segment messages into user→AI turns
    index_generator.py             # Write sessions-index.json
  tests/
    test_jsonl_reader.py
    test_classifier.py
    test_generators.py
    test_turn_entity_classifier.py
    fixtures/sample_session.jsonl
```

## Storage Model

```
规格/P12_内部数据收集系统/
  └── history/
      ├── sessions-index.json              # Pointers to relevant sessions/messages
      ├── replay-index.md                  # Table of contents for readable replays
      ├── replay/                          # Per-session readable replay files
      │   ├── kweng_2026-02-03_02-17.md
      │   └── kweng_2026-02-04_07-58.md
      ├── replay.html                      # Interactive HTML (--raw mode)
      └── replay.md                        # Raw Markdown (--raw mode)

会话历史/                                   # Project-level session history root
  ├── uncategorized/                       # Sessions matching no entity
  │   └── replay/                          # Uncategorized session replays
  ├── replay-index.md                      # Master replay TOC
  ├── all-sessions.json                    # Master index: session -> categories
  └── categorization-report.md             # Statistics
```

## Readable Replay Format (Phase 6)

Each replay file covers one session, organized by **turns** (user prompt + AI response):

- **Turn** = one user prompt + all assistant messages until the next user prompt
- tool_result messages from user role are NOT new turns (they're tool feedback)
- **Final response** = text blocks after the last tool_use (the AI's summary, not preamble)
- **Tool summary** = count by tool name + file paths / bash descriptions
- **Auto-title** = first line of user prompt, truncated to 60 chars
- **Long prompts** (>500 chars) use `<details>` collapsible
- **Person** extracted from JSONL file path (`/Users/kweng/...` → `kweng`)
- **Filename** = `{person}_{YYYY-MM-DD}_{HH-MM}.md`

## Classification Algorithm

Multi-signal scoring per message per entity:

| Signal | Weight | Example |
|--------|--------|---------|
| File path in tool_use | 0.50 | Tool reads `规格/P12_.../design.md` -> spec P12 |
| Explicit text pattern | 0.35 | "Spec #P12", "规格/P12_" in message |
| Keyword matching | 0.15 | "内部数据收集" in message text |

Session confidence = weighted average of matched messages. Threshold: 0.15.

## Entity Categories

| Category | Storage Location | Examples |
|----------|-----------------|----------|
| Specs | `规格/P##_name/history/` | P12_内部数据收集系统, P13_大文档分块处理系统 |
| Source Projects | `源代码/project/history/` | chunked_processor, experiment_analyzer |
| Research | `研究/topic/history/` | 复合箔研究, 定价分析 |
| Knowledge Base | `知识库/area/history/` | 01_公司档案, 02_业务运营 |
| Tools | `工具/history/` | Session persistence, doc validation |
| Uncategorized | `会话历史/uncategorized/` | General Q&A, setup discussions |

## Multi-Spec Session Splitting (Phase 7)

Sessions often span multiple specs sequentially (e.g., turns 1-2 about R14, turns 3-34 about R15). The system detects spec boundaries within a session's turns and generates separate replay files per spec segment.

**Turn-level classification** (per turn, in order):
1. Check `turn.tool_narrative` for entity `path_patterns` (includes legacy aliases)
2. Check `turn.user_prompt` + `turn.assistant_response` for entity `text_patterns`
3. If no match → unclassified (absorbed into adjacent classified segment)

**Grouping rules**:
- Consecutive turns with same entity → one segment
- Unclassified turns absorbed into preceding segment; if at start, into following segment
- Only SPEC entities participate in turn-level splitting

**Indexing**: Sessions are indexed under ALL matched entities (not just primary), so a multi-spec session appears in both entities' indexes.

**Replay generation**: For entity X, only the segment(s) matching X are written. Filename uses the segment's first turn timestamp. Old replay files are cleaned up before regeneration.

## Key Decisions
- **Python**: Consistent with main codebase. Zero external dependencies.
- **Pointer-based**: No data duplication. Replays always reflect latest JSONL content.
- **Single-file HTML**: All CSS+JS inline. Dark theme matching session-persistence styling.
- **Exclude thinking blocks** by default in replays (configurable).
- **P##/R## naming**: Specs use P## (public) and R## (restricted) prefixes with a global counter to avoid collisions.

## JSONL Message Format

Each line is a JSON object with:
- `type`: "user", "assistant", "system", "progress", "file-history-snapshot"
- `uuid`: Unique message ID
- `parentUuid`: Parent message ID (for threading)
- `sessionId`: Session UUID
- `timestamp`: ISO timestamp
- `message.role`: "user" or "assistant"
- `message.content`: String or array of content blocks
  - `{type: "text", text: "..."}` - Text content
  - `{type: "tool_use", name: "Read", input: {file_path: "..."}}` - Tool calls
  - `{type: "tool_result", content: "..."}` - Tool results
  - `{type: "thinking", thinking: "..."}` - Thinking blocks
