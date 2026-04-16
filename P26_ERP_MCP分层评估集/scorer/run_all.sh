#!/bin/bash
# 一键跑 T0/T1 评分 + 对比
# 前提：results/T0/answers.jsonl 和 results/T1/answers.jsonl 已存在

set -e
cd "$(dirname "$0")/.."

SCHEMA_DIR=/Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server/schema
WIKI_DIR=/Users/kweng/AI/Enpack_CCC/源代码/mcp-kingdee-server/wiki

WITH_JUDGE=${WITH_JUDGE:-0}  # 设 WITH_JUDGE=1 才跑 LLM judge（耗 API）

for tag in T0 T1; do
    echo "==> 评分 $tag (自动指标)"
    python3 -m scorer.validity \
        --answers results/$tag/answers.jsonl \
        --questions questions/_all.json \
        --schema-dir "$SCHEMA_DIR" \
        --out results/$tag/validity.json
    python3 -m scorer.refusal \
        --answers results/$tag/answers.jsonl \
        --questions questions/_all.json \
        --out results/$tag/refusal.json

    if [ "$WITH_JUDGE" = "1" ]; then
        echo "==> 评分 $tag (LLM judge)"
        python3 -m scorer.judge --metric factual \
            --answers results/$tag/answers.jsonl \
            --questions questions/_all.json \
            --out results/$tag/factual.json
        python3 -m scorer.judge --metric business \
            --answers results/$tag/answers.jsonl \
            --questions questions/_all.json \
            --wiki-dir "$WIKI_DIR" \
            --out results/$tag/business.json
    fi
done

echo "==> 生成对比报告"
python3 -m scorer.aggregate \
    --t0 results/T0 \
    --t1 results/T1 \
    --out results/comparison.md

echo "完成：results/comparison.md"
