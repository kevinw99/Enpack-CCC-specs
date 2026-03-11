# Design: MCP问答质量评估 (MCP Q&A Quality Evaluation)

## Approach

A/B evaluation: run each test question through two configurations, score both answers, compare.

## Evaluation Pipeline

```
┌────────────────────────────┐
│  Test Question Set (P18)   │
│  30-50 questions           │
└──────────┬─────────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐  ┌──────────┐
│ Config A │  │ Config B  │
│ Vanilla  │  │ MCP-Aug.  │
│ Claude   │  │ Claude +  │
│ (no KB)  │  │ P20 tools │
└────┬────┘  └─────┬─────┘
     │             │
     ▼             ▼
┌─────────────────────────┐
│  Answer Pairs (A, B)    │
│  Randomized labels      │
└──────────┬──────────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌─────────┐  ┌──────────┐
│ Auto     │  │ Human    │
│ Metrics  │  │ Scoring  │
└────┬────┘  └─────┬────┘
     │             │
     ▼             ▼
┌─────────────────────────┐
│  Scorecard & Report     │
└─────────────────────────┘
```

## Test Configurations

### Config A: Vanilla LLM (Baseline)
- Model: Claude (same version as MCP config)
- System prompt: Minimal — "You are a helpful business assistant. Answer the following question."
- No access to knowledge base, no MCP tools
- The model relies on its training data only

### Config B: MCP-Augmented
- Model: Claude (same version)
- System prompt: Same minimal prompt
- MCP tools available: all P20 tools (search_knowledge_base, get_document, etc.)
- Model can query the knowledge base to ground its answers

### Config C (Optional): Vanilla + System Prompt
- Model: Claude (same version)
- System prompt: Includes a summary of Enpack company info (manually crafted)
- No MCP tools, but has static context
- This tests whether simple prompt engineering can match MCP

## Automated Metrics

### 1. Grounding Score
- Extract factual claims from each answer
- Check each claim against knowledge base content
- Score = % of claims that can be traced to KB documents
- Tool: Simple keyword/semantic matching against KB chunks

### 2. Specificity Score
- Count specific entities (company names, product names, numbers, dates) in the answer
- More specific entities = higher specificity
- Tool: Named entity counting

### 3. Response Length
- Token count of each answer
- Not a quality metric per se, but useful for analysis

### 4. Tool Usage (MCP only)
- Which tools were called, how many times
- Did the model effectively use the knowledge base?

## Human Evaluation Protocol

### Blind Evaluation
1. Present evaluator with the question and two answers (labeled "Answer 1" and "Answer 2")
2. Randomize which is MCP vs vanilla (evaluator doesn't know)
3. Evaluator scores each answer on dimensions 1-4 (accuracy, specificity, relevance, actionability)
4. Evaluator picks overall winner (or tie)

### Scoring Rubric

**Factual Accuracy (准确性)**
| Score | Description |
|-------|-------------|
| 5 | All facts correct, well-aligned with company reality |
| 4 | Mostly correct, minor inaccuracies |
| 3 | Some correct facts, some errors or vagueness |
| 2 | Mostly generic or incorrect |
| 1 | Significantly wrong or fabricated |

**Specificity (具体性)**
| Score | Description |
|-------|-------------|
| 5 | Includes specific numbers, names, dates, products from Enpack |
| 4 | References specific Enpack details but missing some |
| 3 | Mix of specific and generic information |
| 2 | Mostly generic industry knowledge |
| 1 | Entirely generic, could apply to any company |

**Relevance (相关性)**
| Score | Description |
|-------|-------------|
| 5 | Directly answers the question with focused content |
| 4 | Answers the question with minor tangents |
| 3 | Partially answers, some relevant content |
| 2 | Loosely related but doesn't answer the question |
| 1 | Off-topic or misunderstands the question |

**Actionability (可操作性)**
| Score | Description |
|-------|-------------|
| 5 | User can immediately take action based on the answer |
| 4 | Provides good guidance, some follow-up needed |
| 3 | Gives direction but lacks concrete steps |
| 2 | Too vague to act on |
| 1 | No actionable content |

## Output Deliverables

### 1. evaluation-results.md
- Per-question scores for both configurations
- Win/loss/tie summary
- Average scores per dimension

### 2. scorecard.md
```
| Dimension | Vanilla Avg | MCP Avg | Delta | MCP Win% |
|-----------|-------------|---------|-------|----------|
| Accuracy  | ?           | ?       | ?     | ?        |
| Specificity| ?          | ?       | ?     | ?        |
| Relevance | ?           | ?       | ?     | ?        |
| Actionability| ?        | ?       | ?     | ?        |
| Overall   | ?           | ?       | ?     | ?        |
```

### 3. failure-analysis.md
- Question categories where MCP underperforms or ties
- Root cause analysis (missing KB content, poor retrieval, irrelevant tools used)
- Specific recommendations for P20 improvement

### 4. recommendations.md
- Changes to P20 tools, indexing, or chunking based on findings
- Content additions needed in KB (feeds back to P19)
- Whether Config C (system prompt) is a viable alternative for some question types

## Test Harness Implementation

```python
# Simplified structure
class EvalHarness:
    def __init__(self, questions: list, mcp_client, vanilla_client):
        self.questions = questions
        self.mcp = mcp_client
        self.vanilla = vanilla_client

    def run_evaluation(self):
        results = []
        for q in self.questions:
            vanilla_answer = self.vanilla.ask(q.question_zh)
            mcp_answer = self.mcp.ask(q.question_zh)  # with MCP tools
            results.append({
                "question": q,
                "vanilla": vanilla_answer,
                "mcp": mcp_answer,
                "auto_metrics": self.compute_auto_metrics(vanilla_answer, mcp_answer),
            })
        return results
```

Location: `源代码/mcp-kb-server/eval/` (alongside the MCP server)

## Key Decisions

- **Blind evaluation**: Prevents bias toward MCP answers
- **Same model**: Isolates the effect of MCP tools from model capability differences
- **Multiple dimensions**: Accuracy alone doesn't capture value; actionability matters for business users
- **Both auto + human**: Auto metrics for scale, human scoring for nuance

## Risk Mitigation

- Risk: Small sample size → Mitigation: Minimum 30 questions, statistical significance check
- Risk: Evaluator bias → Mitigation: Blind labels, clear rubric, multiple evaluators if possible
- Risk: MCP not ready → Mitigation: Can start building harness and rubrics before P20 is complete
- Risk: Vanilla model already knows about Enpack from training → Mitigation: Check for this, note it in analysis
