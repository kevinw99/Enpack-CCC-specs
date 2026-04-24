#!/bin/bash
# P26 真实 MCP-level 全量跑 T0+T1+T2 + 六路 judge + 三路 aggregate + 基线冻结
# 无人值守执行，所有步骤 set -e 保证失败早停
set -e
cd "$(dirname "$0")/.."

PY=/Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server/.venv/bin/python
WIKI_DIR=/Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server/wiki
STAMP=$(date +%Y-%m-%d)
VERSION=${VERSION:-v1}    # override: VERSION=v2 bash scorer/run_mcp_full.sh
BASELINE_DIR=results/baselines/${STAMP}_${VERSION}_MCP-level
LOG=results/mcp_full_run_${VERSION}.log

mkdir -p "$BASELINE_DIR"
echo "==> P26 MCP-level full run $(date)" | tee "$LOG"

# ── Stage 1: T0 T1 T2 answer generation ────────────────────────────────
for stage in T0 T1 T2; do
    echo "" | tee -a "$LOG"
    echo "==> Running $stage ($(date))" | tee -a "$LOG"
    $PY -m scorer.mcp_runner --stage $stage \
        --questions questions/_all.json \
        --out results/${stage}_mcp/answers.jsonl 2>&1 | tee -a "$LOG"
done

# ── Stage 2: Validity + Refusal (cheap) ────────────────────────────────
for stage in T0 T1 T2; do
    echo "" | tee -a "$LOG"
    echo "==> Scoring $stage validity+refusal ($(date))" | tee -a "$LOG"
    $PY -m scorer.validity \
        --answers results/${stage}_mcp/answers.jsonl \
        --questions questions/_all.json \
        --schema-dir /Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server/schema \
        --out results/${stage}_mcp/validity.json 2>&1 | tee -a "$LOG"
    $PY -m scorer.refusal \
        --answers results/${stage}_mcp/answers.jsonl \
        --questions questions/_all.json \
        --out results/${stage}_mcp/refusal.json 2>&1 | tee -a "$LOG"
done

# ── Stage 3: LLM Judges (factual + business) ─────────────────────────────
for stage in T0 T1 T2; do
    echo "" | tee -a "$LOG"
    echo "==> Judges for $stage ($(date))" | tee -a "$LOG"
    $PY -m scorer.judge --metric factual \
        --answers results/${stage}_mcp/answers.jsonl \
        --questions questions/_all.json \
        --out results/${stage}_mcp/factual.json 2>&1 | tee -a "$LOG"
    $PY -m scorer.judge --metric business \
        --answers results/${stage}_mcp/answers.jsonl \
        --questions questions/_all.json \
        --wiki-dir "$WIKI_DIR" \
        --out results/${stage}_mcp/business.json 2>&1 | tee -a "$LOG"
done

# ── Stage 4: Aggregate ────────────────────────────────────────────────────
echo "" | tee -a "$LOG"
echo "==> Aggregate T0/T1/T2 ($(date))" | tee -a "$LOG"
$PY -m scorer.aggregate \
    --t0 results/T0_mcp --t1 results/T1_mcp --t2 results/T2_mcp \
    --out results/comparison_mcp.md 2>&1 | tee -a "$LOG"

# ── Stage 5: Freeze baseline snapshot ────────────────────────────────────
echo "" | tee -a "$LOG"
echo "==> Freezing baseline at $BASELINE_DIR ($(date))" | tee -a "$LOG"
for stage in T0 T1 T2; do
    mkdir -p "$BASELINE_DIR/$stage"
    cp results/${stage}_mcp/*.json "$BASELINE_DIR/$stage/"
    cp results/${stage}_mcp/answers.jsonl "$BASELINE_DIR/$stage/"
done
cp results/comparison_mcp.md "$BASELINE_DIR/"

# ── Stage 6: Emit SCORECARD.json ─────────────────────────────────────────
$PY <<PYEOF
import json
from pathlib import Path
base = Path("$BASELINE_DIR")
scorecard = {
    "baseline_id": "${STAMP}_${VERSION}_MCP-level",
    "date": "${STAMP}",
    "question_set": "P26 V1 / 60 questions",
    "model": "deepseek-chat (temperature=0)",
    "method": "Real MCP-level: LLM calls tools via stdio MCP protocol against src.server",
    "stages": {
        "T0": "query_* + describe_form + search_forms_online only (pre-P20S/P20T)",
        "T1": "T0 + kingdee_get_schema/_relations/_list_cached_schemas (P20S)",
        "T2": "T1 + kingdee_get_wiki (P20T)",
    },
    "states": {},
}
for tag in ["T0", "T1", "T2"]:
    v = json.loads((base / tag / "validity.json").read_text())["summary"]
    r = json.loads((base / tag / "refusal.json").read_text())["summary"]
    f = json.loads((base / tag / "factual.json").read_text())["summary"]
    b = json.loads((base / tag / "business.json").read_text())["summary"]
    scorecard["states"][tag] = {
        "overall": {
            "validity_rate": v.get("validity_overall_mean"),
            "hit_rate": v.get("hit_overall_mean"),
            "refusal_correctness_L7": r.get("refusal_rate"),
            "factual_mean_5": f.get("overall_mean"),
            "business_mean_5": b.get("overall_mean"),
        },
        "by_layer_validity": {k: s["mean"] for k, s in v.get("by_layer_validity", {}).items()},
        "by_layer_hit": {k: s["mean"] for k, s in v.get("by_layer_hit", {}).items()},
        "by_layer_factual": {k: s["mean"] for k, s in f.get("by_layer", {}).items()},
        "by_layer_business": {k: s["mean"] for k, s in b.get("by_layer", {}).items()},
    }
(base / "SCORECARD.json").write_text(json.dumps(scorecard, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"SCORECARD.json written")
PYEOF

echo "" | tee -a "$LOG"
echo "==> ALL DONE $(date)" | tee -a "$LOG"
echo "Baseline: $BASELINE_DIR" | tee -a "$LOG"
