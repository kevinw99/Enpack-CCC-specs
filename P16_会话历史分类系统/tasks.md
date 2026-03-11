# Tasks: 会话历史分类系统

## Phase 1: Core Parser + Classifier
- [x] Create spec directory and documentation
- [x] Implement data models (session.py, category.py, index.py)
- [x] Implement settings and entity registry
- [x] Implement JSONL parser (streaming)
- [x] Implement message extractor
- [x] Implement classifier signals (file_path, text_pattern, keyword)
- [x] Implement composite classifier
- [x] Unit tests for parser and classifier

## Phase 2: HTML/Markdown Replay Generator
- [x] Interactive HTML generator (dark theme, search, filter, collapse)
- [x] Markdown replay generator
- [x] Index generator (sessions-index.json)

## Phase 3: CLI Commands
- [x] `scan` - Full scan + classify + build indexes
- [x] `replay` - Generate replay for entity
- [x] `search` - Search across sessions
- [x] `list` - List sessions with categories
- [x] `stats` - Categorization statistics

## Phase 4: Multi-Category + Uncategorized
- [x] Extend entity registry for all categories
- [x] Cross-entity linkage
- [x] Master index at 会话历史/all-sessions.json
- [x] Categorization report

## Phase 5: Integration + Automation
- [x] Incremental scan mode (--incremental)
- [x] Post-session hook support

## Phase 6: Readable Replay Redesign
- [x] Create Turn dataclass model (models/turn.py)
- [x] Add cwd field to SessionMessage, parse from JSONL
- [x] Build turn_extractor.py (segment, extract final text, tool summary, auto-title, person)
- [x] Build readable_replay_generator.py (per-session Markdown files in replay/)
- [x] Build replay_index_generator.py (replay-index.md per-entity + master)
- [x] Update CLI: replay uses new format by default, --raw for old format
- [x] Unit tests for turn_extractor and readable_replay (23 tests passing)
- [x] End-to-end test with real session data

## Phase 7: Multi-Spec Session Splitting
- [x] Create TurnEntityClassifier (classifier/turn_entity_classifier.py)
- [x] Revert scan to multi-entity indexing (sessions indexed under all matched entities)
- [x] Update ReadableReplayGenerator to split by entity segments
- [x] Add stale replay file cleanup before regeneration
- [x] Unit tests for turn entity classifier (9 tests)
- [x] End-to-end verification: R14/R15 session correctly split

## Phase 8: Native Integration (Hook + Skill)

### 背景分析

当前使用方式需要手动执行：
```bash
cd 源代码 && python3 -m session_history scan -i
```

目标：让 session_history 融入 Claude Code 的日常工作流，无需显式调用 Python。

### 方案设计

**推荐方案：SessionEnd Hook（自动捕获）+ /history Skill（按需查询）**

#### A. SessionEnd Hook — 自动索引

| 项目 | 说明 |
|------|------|
| 触发时机 | 每次会话结束时 |
| 执行内容 | `python3 -m session_history scan -i`（增量扫描） |
| 运行方式 | async=true（异步，不阻塞退出） |
| 配置位置 | `.claude/settings.json`（项目级） |

实现：在现有 `SessionEnd` hook 中追加一条命令：
```json
{
  "type": "command",
  "command": "cd /Users/kweng/AI/Enpack_CCC/源代码 && python3 -m session_history scan -i >> /tmp/session_history.log 2>&1",
  "async": true
}
```

优点：
- 完全自动，用户无感知
- 增量扫描极快（仅处理新/修改的 JSONL）
- 每次会话结束后索引立即更新

局限：
- 当前会话的 JSONL 是否已落盘？需验证 SessionEnd 时 JSONL 是否已写完
- 异步执行，无法获知成功与否（日志写入 /tmp）

#### B. /history Skill — 按需交互

| 项目 | 说明 |
|------|------|
| 调用方式 | `/history`、`/history scan`、`/history replay P16`、`/history stats` |
| 配置位置 | `.claude/commands/history.md`（沿用现有命令模式） |
| 参数传递 | `$ARGUMENTS` 传入子命令和参数 |

Skill 内容设计：
- 无参数时：执行 `scan -i` + `stats`，展示当前索引概况
- `scan`：执行全量或增量扫描
- `replay <entity>`：生成指定实体的回放文件
- `search <keyword>`：跨会话搜索
- `stats`：展示分类统计
- `list`：列出所有会话及分类

优点：
- 与现有 `/process`、`/log` 模式一致
- 可传参，灵活度高
- Claude 可读取输出并总结

### 备选方案（未推荐）

#### C. SessionStart Hook — 进入项目时自动扫描
- 优点：开始工作前索引已最新
- 缺点：如果 SessionEnd 已覆盖，这里是冗余的；增加启动延迟
- 结论：仅在 SessionEnd hook 不可靠时作为备选

#### D. Stop Hook — 每次 Claude 回复后扫描
- 结论：不推荐。触发过于频繁，得不偿失

#### E. PreCompact Hook — 上下文压缩前保存
- 用途不同：更适合保存当前上下文摘要，不是索引的时机
- 结论：可作为未来增强（保存压缩前的上下文快照），但不解决索引问题

### 实施任务

- [ ] 验证 SessionEnd 时 JSONL 文件是否已完整写入
- [x] 在 `.claude/settings.json` 的 SessionEnd 中追加 scan -i 命令
- [x] 创建 `.claude/commands/history.md`（/history skill）
- [ ] 测试：结束会话 → 检查索引是否更新
- [ ] 测试：`/history stats`、`/history replay P16` 等子命令
- [ ] 可选：scan -i 完成后输出简要统计到日志

## Verification
- [x] Run all CLI commands against real session data
- [x] Verify HTML replay opens correctly in browser (--raw mode)
- [x] Verify categorization accuracy
- [x] Verify readable replay format (turn-based, per-session files)
- [x] Verify multi-spec session splitting (R14/R15 each get only their turns)
