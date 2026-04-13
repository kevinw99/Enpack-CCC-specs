# Tasks: KB 适配问题集生成 (P24)

## Phase 0: 规格 ✅
- [x] Task 0.1: 需求文档 (requirements.md)
- [x] Task 0.2: 设计文档 (design.md)
- [x] Task 0.3: 任务分解 (tasks.md)

## Phase 1: KB 内容审查 ✅
- [x] Task 1.1: 阅读公开 KB 文档 (知识库/ + 研究/)，提取可问知识点
- [x] Task 1.2: 阅读 RESTRICTED KB 文档，提取可问知识点
- [x] Task 1.3: 汇总知识点清单，按域分类

## Phase 2: 问题生成

### V1: A 类问题 (KB独占优势) ✅
- [x] Task 2.1: 从用户指南 16 个种子问题生成变体 (15 题) — 方法②
- [x] Task 2.2: 从 P18 部分/完全覆盖问题生成变体 (9 题) — 方法②
- [x] Task 2.3: 从 KB 文档反向生成问题 (36 题) — 方法①
- [x] Task 2.4: 合并候选池，语义去重 → 60 题 A 类

### V2: B/C 类问题 + 合并 ✅
- [x] Task 2.5: 生成 B 类问题 — 通用知识 (18 题)
  - 方法③: 从行业通识生成 (17 题)
  - 方法⑤: 角色模拟法 (1 题)
- [x] Task 2.6: 生成 C 类问题 — KB未覆盖 + 对抗性 (10 题)
  - 方法④: 从 P19 缺口清单生成 (5 题)
  - 方法⑥: 对抗性生成 (5 题，含对抗性理由注释)
- [x] Task 2.7: 合并所有类别 → 88 题
  - A: 60 (68%) / B: 18 (20%) / C: 10 (11%)
  - ID 编号: KB-Axx, KB-Bxx, KB-Cxx

## Phase 3: 质量控制 + 盲评协议设计
- [x] Task 3.1: 标注每题 KB 来源文档 (A 类已完成)
- [x] Task 3.2: 检查分布平衡（域/复杂度/类型）(A 类已完成)
- [x] Task 3.3: 区分度检查（MCP vs Vanilla 增值验证）(A 类已完成)
- [x] Task 3.4: B/C 类问题质量审查
  - B 类: 18题均为公开行业知识，KB无专有信息
  - C 类: 5题P19缺口(需ERP) + 5题对抗性(KB模板/无数据)
- [ ] Task 3.5: 盲评协议设计 (待P21重新评估时实施)
  - 设计回答展示随机化方案 (coin flip per question)
  - 制作评估者表单模板 (仅含问题+两个匿名回答+评分项)
  - 定义揭盲流程和分层分析模板
  - 定义三个假设的统计检验方法

## Phase 4: 输出
- [x] Task 4.1: 生成 questions_kb.py — V1 版本 (60 题 A 类)
- [x] Task 4.2: 生成 Markdown 审阅版本 — V1 版本
- [x] Task 4.3: 统计摘要 — V1 版本
- [x] Task 4.4: 更新 questions_kb.py — V2 版本 (88 题全类别)
  - KBQuestion dataclass 添加 category + expected_outcome 字段
  - ID 编号更新: KB-Axx / KB-Bxx / KB-Cxx
- [x] Task 4.5: 更新 Markdown 审阅版本 — V2 版本 (按类别分节)
- [ ] Task 4.6: 生成盲评工具/脚本 (待P21重新评估时实施)
- [x] Task 4.7: 更新统计摘要 — print_stats() 含类别/预期结果分布
