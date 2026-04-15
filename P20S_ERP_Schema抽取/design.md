# Design: P20S ERP Schema 抽取

## Approach Overview

三通道抽取 + 合并产出：

```
┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
│  Channel A      │  │  Channel B       │  │  Channel C      │
│  T_META_* SQL   │  │  BOS 元数据导出   │  │  LLM 规则推断   │
│  (官方主通道)   │  │  (补充)          │  │  (兜底)         │
└────────┬────────┘  └────────┬─────────┘  └────────┬────────┘
         │                    │                      │
         └────────────────────┼──────────────────────┘
                              ▼
                   ┌──────────────────────┐
                   │   Schema Merger      │
                   │  (优先级: A > B > C) │
                   └──────────┬───────────┘
                              ▼
         ┌─────────────────────────────────────────┐
         │  Output: schema/{form_id}.md + index.json│
         └─────────────────────────────────────────┘
```

## Channel A: T_META_* SQL 抽取

### 关键元数据表

| 表名 | 用途 | 关键字段 |
|------|------|---------|
| `T_META_OBJECTTYPE` | 业务对象定义 | FID, FOBJECTTYPEID, FNAME_L2 |
| `T_META_TABLE` | 表定义 | FID, FTABLENAME, FOBJECTTYPEID |
| `T_META_FIELD` | 字段定义 | FID, FFIELDNAME, FFIELDNAME_L2, FDATATYPE, FDESCRIPTION |
| `T_META_FORMELEMENT` | 表单元素 | 控件属性 |
| `T_META_FORMRELATION` | 表单关联 | 外键关系 |

> ⚠️ 实际表名需要在金蝶数据库实际连接后确认，以上基于公开文档和通用 K/3 Cloud 结构。

### 访问方式

金蝶云星空 REST API **不直接支持 SQL**，需通过以下途径：

1. **途径 1**: 若有数据库只读账号，直接 SQL 查询（最简单）
2. **途径 2**: 通过 P20E 的 `kingdee_describe_form` 逐表获取，然后解析
3. **途径 3**: BOS 平台有"元数据查询"开放 API

本规格优先使用途径 2（已有 MCP 基础），途径 1 作为加速选项。

## Channel B: BOS 设计器导出

- 用户在金蝶 BOS 设计器导出业务对象 → `.bos` 或 `.xml` 文件
- 解析脚本提取字段、关联、控件属性
- 适用于自定义业务对象（T_META 可能不完整的情况）

## Channel C: LLM 辅助注解

### 命名规则库

```yaml
table_prefixes:
  T_BD_: 基础数据 (Base Data)
  T_SAL_: 销售 (Sales)
  T_PUR_: 采购 (Purchase)
  T_IM_: 库存 (Inventory Management)
  T_AP_: 应付 (Accounts Payable)
  T_AR_: 应收 (Accounts Receivable)
  T_GL_: 总账 (General Ledger)
  T_ENG_: 工程 (Engineering)
  T_PRD_: 生产 (Production)
  T_HR_: 人力资源

field_prefixes:
  F:     标准字段前缀
  FNumber: 编码
  FName:   名称
  FDate:   日期
  FAmount: 金额
  FQty:    数量
  FStatus: 状态
  F*Id:    外键
  FDocumentStatus: 单据状态
  FApproveStatus:  审批状态
```

### LLM Prompt 模板

```
你是一个金蝶 ERP 专家。根据以下信息推断该字段的业务含义：

表名: {table_name} (前缀 {prefix} = {module})
字段名: {field_name}
字段类型: {data_type}
样本数据: {sample_values}  # 可选，取 5-10 个去重值

请输出 JSON：
{
  "chinese_name": "...",
  "business_meaning": "...",
  "possible_enum_values": {...},   # 若样本显示枚举性
  "confidence": "high|medium|low"
}
```

## Schema Merger

合并优先级：

1. **Channel A 官方元数据** — 最高可信度，有中文名直接用
2. **Channel B BOS 导出** — 补充 Channel A 缺失项
3. **Channel C LLM 推断** — 标注 `⚠️ AI 推断`，供人工审核

输出时明确标注每条信息的来源（`source: official | bos | llm`）。

## Output Format

### 单表文件 `schema/{form_id}.md`

```markdown
# {FormName_CN} ({FormId})

**表名**: T_BD_MATERIAL
**模块**: 基础资料
**中文名**: 物料档案
**用途**: 存储所有物料（原料、半成品、成品）的主数据

## 字段清单

| 字段名 | 中文名 | 类型 | 说明 | 来源 |
|--------|--------|------|------|------|
| FMATERIALID | 物料内码 | int | 主键 | official |
| FNUMBER | 物料编码 | varchar(30) | 业务编码 | official |
| FSTATUS | 状态 | char(1) | A=未审核 B=已审核 C=已禁用 | llm+样本 ⚠️ |
| ...

## 枚举值

### FSTATUS (状态)
- A: 未审核
- B: 已审核 ⭐ 常用
- C: 已禁用

## 关联关系

- FGROUPID → T_BD_MATERIALGROUP.FMATERIALGROUPID (物料分组)
- FCATEGORYID → T_BD_MATERIALCATEGORY.FCATEGORYID (物料类别)

## 样本查询

...
```

### 索引文件 `schema/index.json`

```json
{
  "version": "2026-04-15",
  "tables": [
    {
      "form_id": "BD_MATERIAL",
      "table_name": "T_BD_MATERIAL",
      "chinese_name": "物料档案",
      "module": "基础资料",
      "field_count": 87,
      "file": "schema/BD_MATERIAL.md"
    },
    ...
  ]
}
```

## Pipeline Implementation

```
源代码/mcp-kingdee-server/schema_extractor/
├── __init__.py
├── cli.py                    # 命令入口: python -m schema_extractor --forms BD_MATERIAL,...
├── channels/
│   ├── official.py           # Channel A
│   ├── bos_parser.py         # Channel B
│   └── llm_annotator.py      # Channel C
├── merger.py                 # Schema Merger
├── renderer.py               # 输出 MD + JSON
└── rules/
    └── naming_rules.yaml     # LLM 命名规则库
```

产出物目录：`源代码/mcp-kingdee-server/schema/`

## Integration with P20E

1. 新增 MCP 工具 `kingdee_get_schema(form_id)` — 从本地 schema 缓存返回精简元数据
2. 替代原 `describe_form` 65KB 响应 → 返回 schema md 文件（约 3-5KB）
3. Schema 版本化：每次抽取带时间戳，支持回滚
