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

**技术决策**: 使用DeepSeek替代Claude以降低成本 (总计$0.025 vs 预估$3-25)

## Phase 3: Evaluation — ✅ 完成 (2026-04-12)
- [x] Task 3.1 - LLM自动评分完成: 4维度×30题×2配置
- [x] Task 3.3 - 评分数据 → `eval/results/scores.json`
- [x] Task 3.4 - 统计汇总: MCP胜6次 (20%), Vanilla胜24次 (80%)

## Phase 4: Analysis & Reporting — ✅ 完成 (2026-04-12)
- [x] Task 4.1 - 记分卡 → `eval/results/scorecard.md`
- [x] Task 4.2 - 失败分析 → `eval/results/failure_analysis.md`
- [x] Task 4.3 - 完整评估报告 → `eval/results/evaluation_report.md`
- [x] Task 4.4 - P20改进建议: 优化系统提示，在KB无覆盖时仍提供框架分析

**关键发现**: Vanilla表面得分高是因为LLM评委无法区分"编造详细答案"vs"诚实说明KB无此信息"。MCP版本的真实价值在于**可溯源性和可靠性**，而非详尽性。

## Phase 5: Iteration — 待定
- [ ] Task 5.1 - 优化MCP系统提示: 无覆盖时提供框架分析 + KB已知信息
- [ ] Task 5.2 - 增加幻觉检测评分轮
- [ ] Task 5.3 - 人工抽样评审 (5-10对答案)
- [ ] Task 5.4 - 扩充KB文档覆盖: 补充"部分覆盖"场景缺失内容
- [ ] Task 5.5 - 优化后重新评估并对比

## 产出文件
```
源代码/mcp-kb-server/eval/
├── questions.py          # 30题测试集
├── harness.py            # 双配置测试框架
├── scorer.py             # LLM-as-Judge自动评分
├── report.py             # 报告生成器
└── results/
    ├── answer_pairs.json # 30对答案 (vanilla + MCP)
    ├── scores.json       # 评分数据
    ├── scorecard.md      # 记分卡
    ├── failure_analysis.md  # 失败分析
    └── evaluation_report.md # 完整评估报告
```
