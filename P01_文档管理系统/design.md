# Document Management System - Design

**Document Type**: Design Specification
**Created**: 2025-01-05
**Status**: Complete

---

## Directory Structure

```
/Users/kweng/AI/Enpack_CCC/
├── 知识库/                    # Company knowledge
│   ├── 01_公司档案/
│   ├── 02_业务运营/
│   ├── 03_技术规范/
│   ├── 04_运营分析/
│   ├── 05_行业背景/
│   ├── 06_ai-opportunities/
│   └── 07_synthesis-recommendations/
│
├── 规格/                             # Project specifications
│   ├── 01_document-management-system/
│   └── 02_knowledge-base-setup/
│
├── 研究/                          # Research and analysis
│   ├── ai-opportunities/
│   ├── industry-analysis/
│   └── notes/
│
├── 文档/                              # Public documentation
└── testing/                           # Testing and verification
```

---

## Naming Standards

**Files**: `lowercase-with-hyphens.md`
- Examples: `peak-bottom-tracking.md`, `制造过程-EN.md`
- All lowercase, no spaces, no underscores
- Max 60 characters for readability

**Directories**: Descriptive lowercase-with-hyphens
- Numbered specs: `##_descriptive-name/` (e.g., `01_document-management-system/`)
- Categories: descriptive names (e.g., `研究/`, `testing/`)

---

## Document Structure

Every document includes:
1. Title and metadata header
2. Summary/purpose section
3. Main content with clear hierarchy
4. Related documents cross-links
5. Change history

---

## Index System

Each category has 项目说明-EN.md with:
- Category description
- Complete document listing
- Quick reference guide
- Statistics and last updated date

Master index at `.kiro/项目说明-EN.md` provides central navigation.

---

## Change History

| Date | Version | Author |
|------|---------|--------|
| 2025-01-05 | 1.0 | Claude |

