# Design Document: Chat Session Persistence

## Overview

The chat session persistence system captures complete Claude Code sessions and formats them for review. The design uses a middleware approach that intercepts messages and tool calls, formats them with color codes, and writes them to multiple output formats asynchronously.

## Architecture

### Core Components

1. **SessionManager** - Orchestrates session lifecycle and coordinates other components
2. **MessageCapture** - Intercepts and captures all messages and tool interactions
3. **ColorFormatter** - Applies color schemes to different message types
4. **MultiFormatWriter** - Writes sessions to multiple output formats
5. **SessionIndexer** - Provides search and retrieval capabilities
6. **RedactionService** - Detects and redacts sensitive information
7. **SessionBrowserGenerator** - Creates web-based session browsing interface

### Integration Approach

Since this is a Claude Code project, the session persistence system should be implemented as:

1. **Hook-based capture** - Use Claude Code's hook system (if available) or environment monitoring
2. **File watcher approach** - Monitor Claude Code's conversation directory for new sessions
3. **Post-processing tool** - Process Claude Code session logs after conversations complete

Given the nature of Claude Code, the most practical approach is **post-processing** with a monitoring daemon that watches for new session data.

## Components and Interfaces

### SessionManager

Manages the complete lifecycle of a chat session, from creation through saving to persistent storage.

```javascript
class SessionManager {
  constructor(config) {
    this.sessionId = this.generateSessionId();
    this.startTime = Date.now();
    this.messages = [];
    this.metadata = {
      filesAccessed: new Set(),
      skillsUsed: new Set(),
      toolsCalled: new Map(),
      tags: new Set(),
    };
    this.colorFormatter = new ColorFormatter(config.colorScheme);
    this.writer = new MultiFormatWriter(config.outputPath);
    this.redactionService = new RedactionService(config.redactionRules);
  }

  captureMessage(message) {
    // Capture and enrich message with metadata
  }

  async saveSession(options = {}) {
    // Save session to multiple formats
  }

  generateSessionId() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const random = Math.random().toString(36).substring(2, 8);
    return `session-${timestamp}-${random}`;
  }
}
```

### ColorFormatter

Applies ANSI color codes to different message types for terminal output.

**Color Scheme (Default):**
- User messages: Cyan (`\x1b[36m`)
- AI responses: Green (`\x1b[32m`)
- Tool calls: Yellow (`\x1b[33m`)
- Tool output: Gray (`\x1b[90m`)
- System messages: Magenta (`\x1b[35m`)
- Errors: Red (`\x1b[31m`)
- Timestamps: Dim (`\x1b[2m`)

**Alternative Scheme (Solarized):**
- Supports Solarized color palette for terminals using that theme

### MultiFormatWriter

Writes session data to multiple output formats asynchronously.

**Formats:**
1. **Terminal** - ANSI color-coded log file
2. **HTML** - Web-viewable session with CSS styling
3. **Markdown** - Documentation-friendly format
4. **Plain Text** - Simple text format without colors
5. **JSON** - Structured data for programmatic access

### SessionIndexer

Provides search and retrieval capabilities across all captured sessions.

**Indices:**
- By date (temporal organization)
- By tag (topic/project area organization)
- By file (file access tracking)
- Full-text (content search)

### RedactionService

Detects and redacts sensitive information before session storage.

**Patterns to Detect:**
- API keys and tokens (20+ character alphanumeric strings)
- Passwords (explicit password patterns)
- Email addresses (standard email format)
- Bearer tokens (OAuth tokens)
- Social security numbers (XXX-XX-XXXX format)

## Data Storage Structure

### Directory Organization

```
sessions/
├── 2025/
│   ├── 01/
│   │   ├── 15/
│   │   │   ├── session-2025-01-15T10-30-45-abc123-terminal.log
│   │   │   ├── session-2025-01-15T10-30-45-abc123-session.html
│   │   │   ├── session-2025-01-15T10-30-45-abc123-session.md
│   │   │   ├── session-2025-01-15T10-30-45-abc123-session.txt
│   │   │   ├── session-2025-01-15T10-30-45-abc123-session.json
│   │   │   └── session-2025-01-15T14-22-18-def456-terminal.log
│   │   └── 16/
│   └── 02/
├── index/
│   ├── by-date.json
│   ├── by-tag.json
│   ├── by-file.json
│   └── full-text-index.json
└── .session-persistence-config.json (optional user config)
```

### Session Index Structure

```json
{
  "sessions": [
    {
      "sessionId": "session-2025-01-15T10-30-45-abc123",
      "startTime": 1705315845000,
      "endTime": 1705318445000,
      "duration": 2600000,
      "messageCount": 42,
      "tags": ["implementation", "testing"],
      "filesAccessed": [
        "/Users/kweng/AI/Enpack_CCC/源代码/core.js",
        "/Users/kweng/AI/Enpack_CCC/项目说明-EN.md"
      ],
      "summary": "Implemented core functionality and updated documentation",
      "paths": {
        "terminal": "sessions/2025/01/15/session-2025-01-15T10-30-45-abc123-terminal.log",
        "html": "sessions/2025/01/15/session-2025-01-15T10-30-45-abc123-session.html",
        "markdown": "sessions/2025/01/15/session-2025-01-15T10-30-45-abc123-session.md",
        "text": "sessions/2025/01/15/session-2025-01-15T10-30-45-abc123-session.txt",
        "json": "sessions/2025/01/15/session-2025-01-15T10-30-45-abc123-session.json"
      }
    }
  ],
  "lastUpdated": 1705318445000
}
```

## Implementation Strategy

### Phase 1: Basic Capture and Formatting (Week 1)

1. Implement SessionManager with basic message capture
2. Implement ColorFormatter with terminal color codes
3. Implement file writing for terminal.log and plain text formats
4. Create configuration system
5. Test with manual message injection

### Phase 2: Multi-Format Support (Week 2)

1. Implement HTML generation with CSS styling
2. Implement Markdown generation
3. Implement JSON structured data export
4. Add metadata extraction and tracking
5. Test output quality across formats

### Phase 3: Integration with Claude Code (Week 3)

1. Research Claude Code session data structure
2. Implement message interception/monitoring
3. Add automatic session start/end detection
4. Handle background tasks and async tool calls
5. Test with actual Claude Code sessions

### Phase 4: Search and Indexing (Week 4)

1. Implement SessionIndexer for building search indices
2. Add full-text search capability
3. Add filtering by date, tags, and files
4. Create CLI tool for searching sessions
5. Build session browser interface

### Phase 5: Redaction and Privacy (Week 5)

1. Implement RedactionService with pattern matching
2. Add sensitive data detection
3. Create secure storage for unredacted versions
4. Add redaction logging and audit trail
5. Test with various sensitive data patterns

### Phase 6: Polish and Optimization (Week 6)

1. Performance optimization
2. Error handling improvements
3. Documentation and examples
4. User configuration options
5. Final testing and bug fixes

## Configuration

### Default Configuration

Located at project root: `.session-persistence-config.json`

```json
{
  "outputPath": "./sessions",
  "colorScheme": "default",
  "formats": ["terminal", "html", "markdown", "text", "json"],
  "enabled": true,
  "redaction": {
    "enabled": true,
    "apiKeys": true,
    "credentials": true,
    "emails": false
  },
  "retention": {
    "days": 90,
    "compress": true,
    "compressAfterDays": 30
  },
  "indexing": {
    "enabled": true,
    "fullTextSearch": true,
    "updateInterval": 300000
  },
  "projectTags": [
    "research",
    "implementation",
    "testing",
    "documentation",
    "refactoring",
    "debugging",
    "configuration",
    "deployment"
  ]
}
```

### User-Configurable Settings

Users can override defaults by creating `.session-persistence-config.json` in the project root:

```json
{
  "colorScheme": "solarized",
  "formats": ["markdown", "json"],
  "redaction": {
    "emails": true
  },
  "outputPath": "/path/to/custom/sessions/directory"
}
```

## Error Handling

### File Write Failures

- Retry with exponential backoff (3 attempts)
- If all retries fail, queue session data in memory
- Attempt to write to alternate location (/tmp)
- Log error but do not interrupt chat session

### Malformed Session Data

- Validate session structure before writing
- Handle missing fields gracefully with defaults
- Log validation errors for debugging
- Produce partial session file if possible

### Disk Space Issues

- Check available disk space before writing
- Implement session rotation policy (keep last 90 days by default)
- Compress old sessions to .gz format
- Provide configuration for retention policy

## Performance Considerations

### Asynchronous Writing

All file I/O operations run asynchronously to avoid blocking chat interactions. Session data is queued in memory and written in batches.

### Incremental Indexing

Search indices are updated incrementally as new sessions are saved rather than rebuilding the entire index.

### Lazy Loading

When searching, only load session JSON metadata initially. Load full session content only when user requests it.

### Memory Management

Limit in-memory session buffer to 100 messages. Auto-flush to disk when limit reached.

## Testing Strategy

### Unit Tests

1. Test ColorFormatter with various message types
2. Test RedactionService pattern matching
3. Test MultiFormatWriter file generation
4. Test SessionManager metadata extraction

### Integration Tests

1. Test complete session capture and save workflow
2. Test multi-format output generation
3. Test index building and updating
4. Test search and retrieval functionality

### Manual Testing

1. Run session persistence during actual Claude Code sessions
2. Verify color rendering in different terminal emulators
3. Test HTML rendering in different browsers
4. Verify search returns correct results

## Session Browser Interface

The session browser provides a web-based interface for viewing and navigating all captured sessions. It consists of an index page showing all sessions and individual session detail pages.

### Features

- **Session list** with sortable/filterable columns
- **Search functionality** across all session content
- **Tag-based filtering** for quick discovery
- **Date-based organization** for temporal navigation
- **Session details** page with full conversation view
- **Metadata display** including files accessed, tools used, duration
- **Responsive design** for desktop and mobile viewing
- **Single HTML file** for offline viewing (no web server required)

## Future Enhancements

1. **Session Replay** - Interactive replay of sessions with timing
2. **Diff Highlighting** - Show code changes made during session
3. **Session Sharing** - Generate shareable links with automatic redaction
4. **Analytics Dashboard** - Visualize session patterns and productivity metrics
5. **Integration with Version Control** - Link sessions to git commits
6. **Export to Documentation** - Convert sessions to project documentation
