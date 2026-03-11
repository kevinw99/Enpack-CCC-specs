# Tasks: MCP知识库服务 (MCP Knowledge Base Server)

## Phase 1: Foundation
- [ ] Task 1.1 - Set up project structure (源代码/mcp-kb-server/)
- [ ] Task 1.2 - Initialize Python project with pyproject.toml and dependencies
- [ ] Task 1.3 - Implement basic MCP server skeleton with stdio transport
- [ ] Task 1.4 - Register server with Claude Desktop config for testing
- [ ] Task 1.5 - Implement `list_topics` tool (simplest tool, validates MCP pipeline works)

## Phase 2: Document Indexing
- [ ] Task 2.1 - Implement file scanner (walk 知识库/ and 研究/ directories)
- [ ] Task 2.2 - Implement markdown parser (extract sections, metadata, headers)
- [ ] Task 2.3 - Implement chunker (split large sections, add overlap)
- [ ] Task 2.4 - Implement embedder (generate vectors via OpenAI or local model)
- [ ] Task 2.5 - Implement SQLite vector store (store and query embeddings)
- [ ] Task 2.6 - Build indexing CLI command (`python -m server index`)
- [ ] Task 2.7 - Run full index of knowledge base, verify chunk quality

## Phase 3: Core Tools
- [ ] Task 3.1 - Implement `search_knowledge_base` tool (semantic search + source attribution)
- [ ] Task 3.2 - Implement `get_document` tool (retrieve by path or topic keyword)
- [ ] Task 3.3 - Implement `get_company_profile` tool (structured company info lookup)
- [ ] Task 3.4 - Implement `lookup_product` tool (product catalog search)
- [ ] Task 3.5 - Implement `lookup_competitor` tool (competitor info search)
- [ ] Task 3.6 - Implement `get_industry_context` tool (industry background search)

## Phase 4: Quality & Testing
- [ ] Task 4.1 - Test with P18 seed questions (Q-001 through Q-004)
- [ ] Task 4.2 - Test bilingual queries (Chinese and English)
- [ ] Task 4.3 - Tune search relevance (adjust chunk size, embedding model, result count)
- [ ] Task 4.4 - Add keyword fallback search for exact-match queries
- [ ] Task 4.5 - Benchmark response time (target < 3 seconds)
- [ ] Task 4.6 - Write basic test suite

## Phase 5: Integration & Documentation
- [ ] Task 5.1 - Write README with setup and usage instructions
- [ ] Task 5.2 - Document Claude Desktop configuration
- [ ] Task 5.3 - Create demo script showing typical Q&A flows
- [ ] Task 5.4 - Review with stakeholders using real business questions
- [ ] Task 5.5 - Identify Phase 2 requirements (structured data tools) based on feedback

## Future: Phase 2 Scope (Structured Data)
- [ ] Task F.1 - Design ERP data integration approach
- [ ] Task F.2 - Design CRM data integration approach
- [ ] Task F.3 - Add inventory/cost lookup tools
- [ ] Task F.4 - Add customer/supplier history tools
- [ ] Task F.5 - Add market data / futures price tools

## Notes
- Phase 1-2 can start immediately without waiting for P18/P19
- Phase 4 testing should use P18 questions once available
- Phase 5 feedback loop may trigger updates to P19 fill plan
- Future phase depends on P19 data source requirements output
