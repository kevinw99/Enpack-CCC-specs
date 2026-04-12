# Tasks: MCP问答质量评估 (MCP Q&A Quality Evaluation)

## Phase 1: Framework Setup — ✅ 完成 (2026-04-12)
- [x] Task 1.1 - 评分维度确定: 准确性/具体性/相关性/可操作性 (1-5分)
- [x] Task 1.2 - 从P18选定30题测试集 (覆盖7部门、3覆盖度、3复杂度)
- [x] Task 1.3 - 盲评协议设计: 随机A/B顺序，LLM-as-Judge
- [x] Task 1.4 - 评估模板: `eval/scorer.py` 自动化评分

## Phase 2: Test Harness — ✅ 完成 (2026-04-12)
- [x] Task 2.1 - 搭建测试框架 `eval/harness.py`
- [x] Task 2.2 - Config A: Vanilla DeepSeek (无知识库)
- [x] Task 2.3 - Config B: DeepSeek + KB搜索结果注入 (模拟MCP增强)
- [x] Task 2.5 - LLM-as-Judge自动评分 `eval/scorer.py`
- [x] Task 2.6 - 生成30题答案对 → `eval/results/answer_pairs.json`

**技术决策**: 使用DeepSeek替代Claude以降低成本 (总计$0.068)

## Phase 3: Evaluation — ✅ 完成 (2026-04-12)
- [x] Task 3.1 - LLM自动评分完成: 4维度×30题×2配置
- [x] Task 3.3 - 评分数据 → `eval/results/scores.json`
- [x] Task 3.4 - 统计汇总: MCP胜6次 (20%), Vanilla胜24次 (80%)

**关键发现**: Vanilla表面得分高是因为LLM评委无法区分"编造详细答案"vs"诚实说明KB无此信息"

## Phase 4: Analysis & Reporting — ✅ 完成 (2026-04-12)
- [x] Task 4.1 - 记分卡 → `eval/results/scorecard.md`
- [x] Task 4.2 - 失败分析 → `eval/results/failure_analysis.md`
- [x] Task 4.3 - 完整评估报告 → `eval/results/evaluation_report.md`
- [x] Task 4.4 - P20改进建议: 优化系统提示，在KB无覆盖时仍提供框架分析

## Phase 5: Iteration — ✅ 完成 (2026-04-13)
- [x] Task 5.1 - 优化MCP系统提示: "先答文档部分，再补行业知识，明确标注来源"
- [x] Task 5.2 - 增加"可信度"评分维度 (信息来源可追溯性, 1-5分)
- [x] Task 5.3 - V2评估: 改进prompt + 5维评分 → MCP胜率 **60%** (从20%逆转)
- [ ] Task 5.4 - 用 Claude 做评委做交叉验证
- [ ] Task 5.5 - 人工抽样评审 (5-10对答案)
- [ ] Task 5.6 - 扩充KB文档覆盖: 补充"部分覆盖"场景缺失内容

**V2结果**: 两项改进 (prompt优化 + 可信度维度) 使MCP胜率从20%逆转至60%

| 版本 | MCP胜 | Vanilla胜 | MCP均分 | V均分 |
|------|-------|-----------|---------|-------|
| V1 (4维) | 6 (20%) | 24 (80%) | 4.00 | 4.74 |
| V1重评 (5维) | 10 (33%) | 20 (67%) | 4.06 | 4.52 |
| **V2 (5维)** | **18 (60%)** | **10 (33%)** | **4.51** | **4.38** |

## 产出文件
```
源代码/mcp-kb-server/eval/
├── questions.py              # 30题测试集
├── harness.py                # 双配置测试框架
├── scorer.py                 # LLM-as-Judge自动评分 (5维)
├── report.py                 # 报告生成器
└── results/
    ├── answer_pairs.json     # V1: 30对答案
    ├── answer_pairs_v2.json  # V2: 改进prompt后答案
    ├── scores.json           # V1重评 (5维)
    ├── scores_v2.json        # V2评分
    ├── scorecard.md          # V1原始记分卡 (4维)
    ├── scorecard_v1_5dim.md  # V1重评记分卡 (5维)
    ├── scorecard_v2.md       # V2记分卡
    ├── failure_analysis*.md  # 各版本失败分析
    ├── evaluation_report.md  # V1评估报告
    └── evaluation_report_v2.md # V2对比报告
```
