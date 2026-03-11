# Content Localization & Naming Strategy - Design

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│         Audience Identification Layer                │
│  (Metadata tagging system for all documents)        │
└──────────────────┬──────────────────────────────────┘
                   │
                   ├─► Management/Executive
                   ├─► Business/Non-technical
                   ├─► Technical
                   └─► Customer-facing

                   ↓
┌─────────────────────────────────────────────────────┐
│      Language Assignment Rules Engine                │
│  (Routes content to appropriate language)           │
└──────────────────┬──────────────────────────────────┘
                   │
                   ├─► Chinese (Simplified)
                   │   └─ Management, Business, Customer
                   │
                   └─► English
                       └─ Technical specifications

                   ↓
┌─────────────────────────────────────────────────────┐
│       File Naming & Organization System              │
│  (Chinese names, pinyin mapping, directories)       │
└─────────────────────────────────────────────────────┘
```

## Implementation Components

### 1. Document Metadata System

#### 1.1 Front-Matter Template (YAML)
Every document must include metadata at the top:

```yaml
---
title: "产品规格说明"
audience:
  primary: "technical"
  secondary: ["management"]
language: "zh-CN"
content_type: "specification"
last_updated: "2026-01-08"
version: "1.0"
localization_status: "original"
translations:
  - language: "en"
    status: "in-progress"
    path: "../../英文-文档/技术资料/product-spec.md"
---
```

**Audience Values**:
- `management` - Executive, C-level, strategic
- `business` - Product managers, operations, business analysts
- `technical` - Engineers, developers, architects
- `customer` - End users, external partners
- `all` - Universal documents

**Localization Status Values**:
- `original` - Source language
- `translated` - Translated from another language
- `hybrid` - Contains mixed languages
- `outdated` - Needs update/retranslation

#### 1.2 Metadata Registry
Maintain a `文档注册表.md` file that catalogs all documents:

```markdown
# Documentation Registry

| File Name | Chinese Name | Audience | Language | Type | Status |
|-----------|--------------|----------|----------|------|--------|
| product-spec.md | 产品规格说明 | technical | en | spec | active |
| exec-summary.md | 执行摘要 | management | zh-CN | guide | active |
```

### 2. Chinese File Naming Convention

#### 2.1 Naming Rules

**Format**: `中文名称.md`

**Guidelines**:
- Use simplified Chinese characters
- Clear, descriptive names (2-5 characters typically)
- Use common business/technical terminology familiar to audience
- NO spaces, NO special characters (except hyphens in pinyin alternatives)
- NO English abbreviations in Chinese names (e.g., not "API-说明-EN.md")

**Examples**:

| Document Purpose | Chinese Name |
|-----------------|--------------|
| Product specification | `产品规格说明-EN.md` |
| Customer guide | `客户指南.md` |
| Executive summary | `执行摘要.md` |
| Technical architecture | `系统架构设计.md` |
| Installation guide | `安装指南.md` |
| API documentation | `应用编程接口文档.md` |
| Company profile | `公司概览.md` |
| Meeting minutes | `会议记录.md` |
| Pricing information | `定价信息.md` |
| Quarterly report | `季度报告.md` |

#### 2.2 Directory Structure

```
project-root/
│
├── 文档/
│   ├── 中文文档/
│   │   ├── 管理层/          # Management/Executive documents
│   │   │   ├── 执行摘要.md
│   │   │   ├── 季度报告.md
│   │   │   └── 战略计划.md
│   │   │
│   │   ├── 业务运营/        # Business/Operations documents
│   │   │   ├── 客户指南.md
│   │   │   ├── 操作手册.md
│   │   │   └── 常见问题.md
│   │   │
│   │   └── 客户文档/        # Customer-facing documents
│   │       ├── 用户指南.md
│   │       ├── 故障排除.md
│   │       └── 最佳实践.md
│   │
│   └── 英文-文档/
│       ├── technical/       # Technical specifications
│       │   ├── system-architecture.md
│       │   ├── api-documentation.md
│       │   ├── database-schema.md
│       │   └── deployment-guide.md
│       │
│       └── reference/       # Technical references
│           ├── code-standards.md
│           └── git-workflow.md
│
└── .claude/
    └── localization/
        └── pinyin-mapping.md   # Lookup table for conversions
```

#### 2.3 Pinyin Mapping for URLs

Create a mapping file for web accessibility:

```markdown
# Pinyin Mapping Reference

| Chinese Name | Pinyin URL Slug | English Title |
|--------------|-----------------|---------------|
| 产品规格说明 | chanpin-guige-shuoming | Product Specification |
| 客户指南 | kehu-zhinan | Customer Guide |
| 执行摘要 | zhixing-zhaiyao | Executive Summary |
```

This allows URLs like: `/文档/zh/chanpin-guige-shuoming/`

### 3. Language Assignment Rules - Decision Matrix

```
┌─────────────────────────┬──────────────────┬─────────────────────────┐
│ Audience Category       │ Primary Language │ Secondary Language      │
├─────────────────────────┼──────────────────┼─────────────────────────┤
│ Management/Executive    │ Chinese (ZH-CN)  │ English (optional)      │
│ Business/Operations     │ Chinese (ZH-CN)  │ English (if partners)   │
│ Technical/Engineering   │ English          │ Chinese (if needed)     │
│ Customer-facing         │ Chinese (ZH-CN)  │ English (for expats)    │
│ Mixed Audience          │ See rules below  │                         │
└─────────────────────────┴──────────────────┴─────────────────────────┘

Rules for Mixed Audiences:
1. Technical spec with executive summary → English for spec, Chinese for summary
2. Internal guide used by ops and eng → Chinese name, English content (or bilingual)
3. Public-facing with international access → Chinese primary, English fallback
```

### 4. Migration Strategy

#### Phase 1: Preparation (Week 1)
- [ ] Audit all existing files and identify audiences
- [ ] Create 文档注册表.md
- [ ] Set up new directory structure
- [ ] Create naming convention guide

#### Phase 2: High-Priority Migration (Week 2-3)
- [ ] Rename management/executive documents
- [ ] Rename customer-facing documents
- [ ] Update all internal links
- [ ] Create metadata headers

#### Phase 3: Technical & Support (Week 4)
- [ ] Rename business/operations documents
- [ ] Ensure English technical docs properly organized
- [ ] Finalize pinyin mapping
- [ ] Document the complete system

#### Phase 4: Automation & Enforcement (Week 5)
- [ ] Create validation scripts
- [ ] Set up Git hooks to enforce naming
- [ ] Create templates for new documents
- [ ] Train team on new conventions

### 5. Validation & Quality Control

#### 5.1 Pre-commit Hook
Validate files before commit:
- Check for proper audience metadata
- Verify file names match naming convention
- Check for broken links after renames
- Validate metadata format

#### 5.2 Documentation Template
Create templates for each document type to ensure consistency:

```markdown
---
title: "中文标题"
audience:
  primary: "管理层"  # management, business, technical, customer
language: "zh-CN"   # zh-CN or en
content_type: "指南" # spec, guide, reference, report, etc.
last_updated: "2026-01-08"
version: "1.0"
---

# 中文标题

[Content here]
```

### 6. Link Mapping & Redirection

When files are renamed:
1. Create a link mapping file: `/文档/.link-redirects.md`
2. Update all internal references in one pass
3. For web-accessible docs, set up server redirects (301)
4. Document old → new name mappings for reference

## Special Considerations

### Technical Documentation
- **Code comments**: Stay in English
- **API documentation**: English (standard practice)
- **Architecture diagrams**: Language-agnostic (labels in appropriate language)
- **Examples/tutorials**: English for technical, Chinese for customer tutorials

### Translation Maintenance
- Do NOT manually translate; use professional translation tools when needed
- Keep source (English/Chinese) and translation in sync
- Track translation status in metadata
- Review translations quarterly

### Bilingual Documents
For documents that serve multiple audiences in different languages:
- Store as separate files (one per language)
- Link them clearly in metadata
- Maintain version parity
- Update both when either is modified
