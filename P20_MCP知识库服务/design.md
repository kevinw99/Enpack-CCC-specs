# Design: MCP知识库服务 (MCP Knowledge Base Server)

## Approach

Build a Python-based MCP server that indexes the knowledge base into a vector store and exposes semantic search + structured lookup tools. Start with the simplest architecture that works, then extend.

## Architecture

```
┌─────────────────────────────────────────────┐
│  AI Client (Claude Desktop / Claude Code)    │
│  User asks: "采购10吨氧化铜合理吗?"           │
└──────────────┬──────────────────────────────┘
               │ MCP Protocol (stdio/SSE)
               ▼
┌─────────────────────────────────────────────┐
│  MCP Server: enpack-kb-server                │
│                                              │
│  Tools:                                      │
│  ├── search_knowledge_base(query, filters)   │
│  ├── get_document(path_or_topic)             │
│  ├── list_topics()                           │
│  ├── get_company_profile(aspect)             │
│  ├── lookup_product(product_name)            │
│  ├── lookup_competitor(company_name)         │
│  └── get_industry_context(topic)             │
│                                              │
│  Resources:                                  │
│  ├── kb://index — Knowledge base index       │
│  └── kb://stats — Coverage statistics        │
│                                              │
│  Internal:                                   │
│  ├── Document Loader (markdown parser)       │
│  ├── Chunker (splits docs into sections)     │
│  ├── Embedder (generates vectors)            │
│  └── Vector Store (search index)             │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│  Data Layer                                  │
│  ├── 知识库/ (markdown files)                │
│  ├── 研究/ (research outputs)                │
│  ├── embeddings.db (SQLite + vectors)        │
│  └── [Future] ERP/CRM API connections        │
└─────────────────────────────────────────────┘
```

## MCP Tools Design

### Tool 1: `search_knowledge_base`
```json
{
  "name": "search_knowledge_base",
  "description": "Search the Enpack knowledge base using natural language. Returns relevant document sections with source attribution. Supports Chinese and English queries.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Natural language search query" },
      "category": { "type": "string", "enum": ["company", "operations", "tech", "analysis", "industry", "research", "all"], "default": "all" },
      "max_results": { "type": "integer", "default": 5 }
    },
    "required": ["query"]
  }
}
```

### Tool 2: `get_document`
```json
{
  "name": "get_document",
  "description": "Retrieve a specific knowledge base document by topic keyword or file path.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": { "type": "string", "description": "Topic keyword (e.g., '产品组合', 'pricing', '供应链')" },
      "path": { "type": "string", "description": "Direct file path within the knowledge base" }
    }
  }
}
```

### Tool 3: `list_topics`
```json
{
  "name": "list_topics",
  "description": "List all available knowledge base categories and topics with document counts.",
  "inputSchema": { "type": "object", "properties": {} }
}
```

### Tool 4: `get_company_profile`
```json
{
  "name": "get_company_profile",
  "description": "Get specific aspects of the Enpack/CCC company profile.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "aspect": { "type": "string", "enum": ["overview", "history", "org_structure", "financials", "key_personnel", "mission"], "description": "Which aspect of the company profile to retrieve" }
    },
    "required": ["aspect"]
  }
}
```

### Tool 5: `lookup_product`
```json
{
  "name": "lookup_product",
  "description": "Look up product information including specifications, pricing context, and market position.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "product_name": { "type": "string", "description": "Product name or category (e.g., '复合铜箔', '复合铝箔', 'MA')" }
    },
    "required": ["product_name"]
  }
}
```

### Tool 6: `lookup_competitor`
```json
{
  "name": "lookup_competitor",
  "description": "Look up competitor company information and comparison with Enpack.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "company_name": { "type": "string", "description": "Competitor company name" }
    },
    "required": ["company_name"]
  }
}
```

### Tool 7: `get_industry_context`
```json
{
  "name": "get_industry_context",
  "description": "Get industry background information on a specific topic (standards, trends, regulations).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "topic": { "type": "string", "description": "Industry topic (e.g., 'battery safety standards', '固态电池', 'composite foil market')" }
    },
    "required": ["topic"]
  }
}
```

## Technical Implementation

### Stack
- **Language**: Python 3.11+
- **MCP SDK**: `mcp` (official Python SDK)
- **Embeddings**: OpenAI `text-embedding-3-small` (good Chinese support, low cost) or local alternative
- **Vector Store**: `sqlite-vec` (SQLite extension) or `chromadb` (simpler API)
- **Markdown Parsing**: `markdown-it-py` or simple regex-based section splitter
- **Transport**: stdio (for Claude Desktop/Code integration)

### Document Processing Pipeline

```
1. Scan: Walk 知识库/ and 研究/ directories
2. Parse: Extract sections from each markdown file (split on ## headers)
3. Enrich: Add metadata (file path, category, language, section title)
4. Chunk: Split large sections (>1000 tokens) into overlapping chunks
5. Embed: Generate vector embeddings for each chunk
6. Store: Insert into SQLite vector database
7. Index: Build keyword index for exact-match fallback
```

### Project Structure

```
源代码/mcp-kb-server/
├── pyproject.toml
├── README.md
├── src/
│   ├── server.py          # MCP server entry point
│   ├── tools/
│   │   ├── search.py      # search_knowledge_base
│   │   ├── documents.py   # get_document, list_topics
│   │   ├── company.py     # get_company_profile
│   │   ├── products.py    # lookup_product
│   │   ├── competitors.py # lookup_competitor
│   │   └── industry.py    # get_industry_context
│   ├── indexer/
│   │   ├── scanner.py     # File discovery
│   │   ├── parser.py      # Markdown parsing
│   │   ├── chunker.py     # Document chunking
│   │   └── embedder.py    # Embedding generation
│   ├── store/
│   │   └── vector_db.py   # SQLite vector store
│   └── config.py          # Configuration
├── data/
│   └── embeddings.db      # Generated vector database
└── tests/
    ├── test_search.py
    ├── test_tools.py
    └── test_indexer.py
```

## Key Decisions

- **Python over TypeScript**: Better Chinese NLP ecosystem, simpler embedding pipeline, team familiarity
- **SQLite over cloud vector DB**: Local-first, no external dependencies, good enough for <1000 documents
- **Tools over Resources**: MCP tools allow parameterized queries; resources are static. Tools are more flexible for search
- **Stdio transport**: Simplest integration with Claude Desktop and Claude Code
- **Section-level chunking**: Split on markdown headers, not arbitrary token counts — preserves semantic coherence

## Alternative Approaches

- **LlamaIndex/LangChain**: More features but heavier dependency, more abstraction layers. Rejected for simplicity.
- **Qdrant/Pinecone**: Cloud vector DBs. Overkill for <1000 docs. Can migrate later if needed.
- **TypeScript MCP**: Viable but Python has better markdown/NLP tooling for Chinese content.

## Risk Mitigation

- Risk: Chinese embedding quality → Mitigation: Test with multilingual models, use hybrid search (vector + keyword)
- Risk: Slow indexing → Mitigation: Incremental indexing based on file modification time
- Risk: MCP SDK changes → Mitigation: Pin SDK version, keep tool interface stable
- Risk: Documents too large for context → Mitigation: Return ranked chunks not full documents, let AI synthesize
