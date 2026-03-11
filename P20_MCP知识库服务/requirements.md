# Requirements: MCP知识库服务 (MCP Knowledge Base Server)

## Overview

Build a Model Context Protocol (MCP) server that enables AI assistants (Claude, etc.) to answer business questions by querying the Enpack knowledge base and connected data sources. This is the implementation layer that makes the knowledge base actionable — employees ask questions in natural language, and the MCP provides the AI with the right context to answer.

## Background

From the 2/22 conversation, the core vision is clear: an AI that can pull together information from multiple internal sources to support daily business decisions — procurement approvals, supplier negotiations, sales pricing, inventory management, and more.

The MCP approach is ideal because:
- It provides structured tools that AI assistants can call
- It keeps data access controlled and auditable
- It works with any MCP-compatible AI client (Claude Desktop, Claude Code, etc.)
- It separates data access logic from AI reasoning

## Objectives

1. Build an MCP server that exposes the knowledge base as searchable, queryable tools
2. Support semantic search across all knowledge base documents
3. Provide structured data lookup tools for key business entities (products, customers, suppliers, costs)
4. Enable multi-source synthesis (combine KB content + structured data to answer complex questions)
5. Design for extensibility — easy to add new data sources (ERP, CRM) in future phases

## Scope

### Phase 1 (MVP) — Knowledge Base Search
- Semantic search across all 知识库/ documents
- Search across all 研究/ research outputs
- Document retrieval by topic/category
- Company profile and business context queries

### Phase 2 — Structured Data Tools
- Product catalog lookup (产品组合 data)
- Cost and pricing reference (from 研究/定价分析/)
- Competitor information lookup (from 研究/客户细分研究/, P08 公司档案)
- Industry standards reference (from 知识库/05_行业背景/)

### Phase 3 — External Data Integration (Future)
- ERP connection: inventory, purchase history, order records, cost data
- CRM connection: customer profiles, cooperation history
- Email/meeting search: supplier communication history
- Market data: commodity prices, futures trends
- External info: company credit checks, industry news

### Out of Scope (for now)
- Real-time data streaming
- Write operations (MCP is read-only for safety)
- User authentication (handled by MCP client)
- Mobile/web UI (users interact via AI chat client)

## Success Criteria

- [ ] MCP server starts and registers with Claude Desktop / Claude Code
- [ ] `search_knowledge_base` tool returns relevant documents for natural language queries
- [ ] `get_document` tool retrieves specific KB documents by path or topic
- [ ] `list_topics` tool shows available knowledge categories
- [ ] Server handles Chinese and English queries
- [ ] Response time < 3 seconds for KB search
- [ ] Can answer at least 80% of P18 "KB-answerable" questions (those tagged kb_coverage: full/partial)

## Technical Requirements

### MCP Protocol
- Implement MCP server using official SDK (Python or TypeScript)
- Expose tools (not just resources) for active querying
- Support streaming responses for large result sets

### Search & Retrieval
- Vector embeddings for semantic search (consider: OpenAI embeddings, local model, or Anthropic)
- Chunk documents appropriately for retrieval (leverage P13 大文档分块处理系统 if applicable)
- Return source attribution with every answer (which document, which section)

### Data Layer
- Index all markdown files in 知识库/ and 研究/ directories
- Support incremental re-indexing when documents change
- Store embeddings locally (SQLite + vector extension, or file-based)

### Infrastructure
- Run locally or on a simple server (no heavy cloud infra for MVP)
- Configuration via environment variables or config file
- Logging for all queries (for future analysis and improvement)

## Constraints & Assumptions

- Knowledge base is in markdown format (mix of Chinese and English)
- MCP client handles the conversational UI — server just provides tools
- MVP uses existing knowledge base content only; external data comes in Phase 3
- Must work on macOS (development environment)

## Dependencies

- P18 (样本问题收集) — defines what questions the MCP must answer
- P19 (知识库缺口分析) — identifies what content/data is available vs. missing
- P13 (大文档分块处理系统) — document chunking approach may be reusable
- Current knowledge base content (知识库/, 研究/)
- MCP SDK (Python: `mcp` package, or TypeScript: `@modelcontextprotocol/sdk`)

## Questions & Clarifications

- Preferred language for MCP implementation: Python or TypeScript?
- Should the MCP server be deployable to Render (existing infra) or local-only for now?
- What embedding model to use? (Cost vs. quality tradeoff)
- Should we support querying across multiple Enpack repos or just this one (CCC)?
