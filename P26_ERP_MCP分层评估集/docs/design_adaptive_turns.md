# Design: Adaptive Turn Routing for MCP Runner

**Status**: Design proposal (not implemented)  
**Author**: Claude (auto-generated from v1-v5 iteration data)  
**Date**: 2026-04-18

## Problem

All question types hit MAX_TURNS=12 regardless of complexity:
- L1 (basic lookups): avg 11.2 turns — wastes 8+ turns on schema discovery for trivial queries
- L4-L8 (complex): avg 12.0 turns — legitimately needs turns but still runs out

The one-size-fits-all turn budget means:
1. Simple questions waste turns on unnecessary schema exploration
2. Complex questions don't get enough turns for multi-step analysis
3. Both suffer because the prompt's "turn budget" warning kicks in at turn 9

## Proposed Solution: Question Pre-Classifier + Dynamic Budget

### Architecture

```
Question → Pre-Classifier → Turn Budget → answer_one()
                ↓
         Complexity class:
         - SIMPLE (L1/L2): 6 turns, skip list_cached_schemas
         - MEDIUM (L3/L4): 12 turns (current)  
         - COMPLEX (L5/L6/L8): 16 turns, extended schema phase
         - PSEUDO (L7): 0 turns (already handled by pre-filter)
```

### Pre-Classifier Design

**Option A: Metadata-based (zero-cost)**
Use existing question metadata:
- `required_forms` length: 1 form = SIMPLE, 2 = MEDIUM, 3+ = COMPLEX
- `layer`: L1/L2 = SIMPLE, L3/L4 = MEDIUM, L5/L6/L8 = COMPLEX
- `pseudo_question`: PSEUDO

**Option B: LLM-based (one extra API call)**
Quick classification prompt (50 tokens out):
```
Given this question, classify complexity: SIMPLE/MEDIUM/COMPLEX
- SIMPLE: single table lookup, list/filter
- MEDIUM: status interpretation, conditional logic
- COMPLEX: cross-table join, time-series, multi-step analysis
```

**Recommendation**: Start with Option A (free, deterministic). The layer metadata is already a good proxy for complexity.

### Dynamic Budget Implementation

```python
TURN_BUDGETS = {
    "SIMPLE": 6,
    "MEDIUM": 12,
    "COMPLEX": 16,
    "PSEUDO": 0,
}

def classify_question(q: dict) -> str:
    if q.get("pseudo_question"):
        return "PSEUDO"
    n_forms = len(q.get("required_forms", []))
    layer = q.get("layer", "")
    if layer in ("L1", "L2") or n_forms <= 1:
        return "SIMPLE"
    if layer in ("L5", "L6", "L8") or n_forms >= 3:
        return "COMPLEX"
    return "MEDIUM"
```

### Prompt Adaptation

For SIMPLE questions, inject a streamlined prompt section:
```
这是一个简单查询题。跳过 list_cached_schemas，直接 get_schema → query_bills。
最多 6 轮工具调用。
```

For COMPLEX questions:
```
这是一个复杂分析题，需要跨表关联。先用 get_relations 规划路径，再逐表 get_schema。
最多 16 轮工具调用。到第 13 轮未查数据要立即收尾。
```

### Expected Impact

| Class | Current avg turns | Budget | Expected factual change |
|-------|------------------|--------|------------------------|
| SIMPLE | 11.2 (wasting ~5) | 6 | +0.2 (faster to answer, less confusion) |
| MEDIUM | 12.0 (borderline) | 12 | neutral |
| COMPLEX | 12.0 (often truncated) | 16 | +0.5 (4 more turns for data queries) |

### Risks

1. **Misclassification**: A question classified SIMPLE that actually needs cross-table logic will fail in 6 turns. Mitigation: fall back to MEDIUM if SIMPLE hits budget.
2. **Cost increase**: COMPLEX at 16 turns means ~33% more API calls for those questions. Acceptable if accuracy improves.
3. **Prompt length**: Different prompt sections per class adds complexity. Keep it to 2-3 lines of difference.

### Implementation Effort

~2 hours: add `classify_question()`, parameterize `MAX_TURNS` per question, adjust prompt budget warning. No architectural changes.

## Decision

Implement in v7 if v6 shows turn budget is still the binding constraint (>80% of non-pseudo questions hitting MAX_TURNS).
