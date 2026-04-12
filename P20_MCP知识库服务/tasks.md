# Tasks: MCP知识库服务 (MCP Knowledge Base Server)

## Phase 1: Foundation ✅
- [x] Task 1.1 - Set up project structure (源代码/mcp-kb-server/)
- [x] Task 1.2 - Initialize Python project with pyproject.toml and dependencies
- [x] Task 1.3 - Implement basic MCP server skeleton with stdio transport
- [x] Task 1.4 - Register server with Claude Code config (.mcp.json with env vars)
- [x] Task 1.5 - Implement `list_topics` tool (simplest tool, validates MCP pipeline works)

## Phase 2: Document Indexing ✅
- [x] Task 2.1 - Implement file scanner (walk 知识库/ and 研究/ directories)
- [x] Task 2.2 - Implement markdown parser (extract sections, metadata, headers)
- [x] Task 2.3 - Implement chunker (split large sections, add overlap)
- [x] Task 2.4 - Implement embedder (local model: paraphrase-multilingual-MiniLM-L12-v2, 384 dims)
- [x] Task 2.5 - Implement SQLite vector store (brute-force cosine similarity, fine for <10k chunks)
- [x] Task 2.6 - Build indexing CLI command (`python -m src index` / `python -m src stats`)
- [x] Task 2.7 - Run full index: 47 files → 1259 sections → 1345 chunks in 17s

## Phase 3: Core Tools ✅
- [x] Task 3.1 - Implement `search_knowledge_base` tool (hybrid semantic + keyword search)
- [x] Task 3.2 - Implement `get_document` tool (path match + directory match + keyword fallback)
- [x] Task 3.3 - Implement `get_company_profile` tool (aspect-based query mapping)
- [x] Task 3.4 - Implement `lookup_product` tool (product catalog search)
- [x] Task 3.5 - Implement `lookup_competitor` tool (competitor info search)
- [x] Task 3.6 - Implement `get_industry_context` tool (industry background search)

## Phase 4: Quality & Testing (in progress)
- [x] Task 4.1 - Test with P18 seed questions (Q-030, Q-052, Q-008, Q-003, Q-047, Q-020)
- [x] Task 4.2 - Test bilingual queries (Chinese and English) — both work well
- [x] Task 4.3 - Tune search: hybrid semantic+keyword, keyword boost threshold=0.6
- [x] Task 4.4 - Add keyword fallback search for exact-match queries
- [ ] Task 4.5 - Benchmark response time (target < 3 seconds)
- [ ] Task 4.6 - Write basic test suite

## Phase 5: Integration & Documentation
- [x] Task 5.1 - README exists with setup and usage instructions
- [x] Task 5.2 - Claude Code MCP configuration (.mcp.json)
- [ ] Task 5.3 - Create demo script showing typical Q&A flows
- [ ] Task 5.4 - Review with stakeholders using real business questions
- [ ] Task 5.5 - Identify next requirements based on P21 质量评估 feedback

## ERP/External Data Integration (独立开发)
> **Note:** ERP MCP 由 Yongzhi 在 `yongzhi_erp_mcp_0325` 分支独立开发，
> 位于 `源代码/mcp-kingdee-server/`。已实现金蝶 ERP 数据查询和期货数据工具。
> 两个 MCP server 独立运行，AI 客户端可同时连接使用。

- [x] Task F.1 - ERP data integration: 金蝶云星空 MCP (by Yongzhi)
- [ ] Task F.2 - CRM data integration approach (future)
- [x] Task F.3 - Inventory/cost/materials lookup (in kingdee MCP)
- [ ] Task F.4 - Customer/supplier history tools (future)
- [x] Task F.5 - Futures price + purchase cost analysis tools (in kingdee MCP)

## Notes
- Phase 1-3 completed 2026-04-12
- Phase 4 tested with P18 questions — hybrid search improves recall for specific queries
- KB MCP and ERP MCP are complementary: KB for knowledge/context, ERP for live data
- Next: P21 will evaluate answer quality systematically
