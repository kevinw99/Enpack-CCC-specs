# Design: 实验数据分析建模系统

## System Architecture

### 整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          实验数据分析建模系统                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   数据层     │  │   分析层     │  │   模型层     │  │   应用层     │ │
│  │  Data Layer  │  │ Analysis     │  │   Model      │  │ Application  │ │
│  │              │  │   Layer      │  │   Layer      │  │   Layer      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │                 │                 │                 │         │
│  ┌──────▼───────────────────────────────────────────────────────────┐   │
│  │                        核心数据框架 (pandas DataFrame)             │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
```

### 模块结构

```
experiment_analyzer/
├── __init__.py
├── config/
│   ├── __init__.py
│   ├── settings.py          # 全局配置
│   └── parameters.yaml      # 参数定义（名称、单位、范围）
│
├── data/
│   ├── __init__.py
│   ├── loader.py            # 数据加载器（Markdown, CSV, Excel）
│   ├── validator.py         # 数据验证
│   ├── cleaner.py           # 数据清洗
│   └── transformer.py       # 数据转换
│
├── analysis/
│   ├── __init__.py
│   ├── descriptive.py       # 描述性统计
│   ├── correlation.py       # 相关性分析
│   ├── trend.py             # 趋势分析
│   └── anomaly.py           # 异常检测
│
├── models/
│   ├── __init__.py
│   ├── base.py              # 模型基类
│   ├── regression.py        # 回归模型
│   ├── ensemble.py          # 集成模型
│   ├── neural.py            # 神经网络模型
│   ├── evaluator.py         # 模型评估
│   └── registry.py          # 模型注册和版本管理
│
├── optimization/
│   ├── __init__.py
│   ├── single_objective.py  # 单目标优化
│   ├── multi_objective.py   # 多目标优化
│   ├── doe.py               # 实验设计
│   └── recommender.py       # 参数推荐引擎
│
├── visualization/
│   ├── __init__.py
│   ├── plots.py             # 静态图表
│   ├── interactive.py       # 交互式图表
│   └── dashboard.py         # 仪表板
│
├── reports/
│   ├── __init__.py
│   ├── generator.py         # 报告生成器
│   └── templates/           # 报告模板
│
└── notebooks/
    ├── 01_data_exploration.ipynb
    ├── 02_correlation_analysis.ipynb
    ├── 03_model_training.ipynb
    ├── 04_optimization.ipynb
    └── 05_experiment_review.ipynb
```

## Approach

### 阶段性实施策略

```
Phase 1: 数据基础          Phase 2: 分析能力         Phase 3: 建模预测         Phase 4: 优化应用
(Week 1-2)                 (Week 3-4)                (Week 5-6)               (Week 7-8)
┌─────────────────┐        ┌─────────────────┐       ┌─────────────────┐      ┌─────────────────┐
│ • 数据结构设计   │   →    │ • 统计分析      │   →   │ • 模型选择      │  →   │ • 参数优化      │
│ • 数据导入工具   │        │ • 相关性分析    │       │ • 模型训练      │      │ • 预测服务      │
│ • 数据验证      │        │ • 可视化        │       │ • 模型评估      │      │ • DOE建议       │
│ • 数据清洗      │        │ • 异常检测      │       │ • 模型对比      │      │ • 报告生成      │
└─────────────────┘        └─────────────────┘       └─────────────────┘      └─────────────────┘
```

### 数据流程

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                     数据来源                             │
                    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
                    │  │ Markdown │  │   CSV    │  │  Excel   │  │   JSON   ││
                    │  │  Tables  │  │  Files   │  │  Files   │  │  Files   ││
                    │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│
                    └───────┼──────────────┼──────────────┼──────────────┼────┘
                            │              │              │              │
                            ▼              ▼              ▼              ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │              统一数据加载器 (DataLoader)                  │
                    └─────────────────────────┬───────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │              数据验证 (DataValidator)                    │
                    │  • 类型检查  • 范围检查  • 完整性检查  • 一致性检查        │
                    └─────────────────────────┬───────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │              数据清洗 (DataCleaner)                       │
                    │  • 缺失值处理  • 异常值处理  • 格式标准化  • 单位转换       │
                    └─────────────────────────┬───────────────────────────────┘
                                              │
                                              ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │              标准化数据集 (DataFrame)                     │
                    │  experiment_id | date | parameters... | results...      │
                    └─────────────────────────────────────────────────────────┘
```

## Key Decisions

### D1: 数据存储格式
**决定**: 采用 CSV 作为主要存储格式，配合 JSON 元数据

**理由**:
- CSV 通用性强，易于查看和编辑
- 兼容 Excel，便于非技术人员使用
- pandas 原生支持，加载高效
- Git 友好，便于版本控制

**替代方案**: SQLite 数据库（更适合大数据量场景，暂不需要）

### D2: 建模框架
**决定**: 以 scikit-learn 为主，保留扩展到深度学习的能力

**理由**:
- scikit-learn 接口统一，易于使用
- 提供丰富的传统机器学习算法
- 初期数据量适合传统方法
- 如需深度学习，可无缝切换到 PyTorch

**备选**: statsmodels（统计模型）、XGBoost（梯度提升）

### D3: 可视化方案
**决定**: matplotlib + plotly 组合

**理由**:
- matplotlib: 静态图表，适合报告
- plotly: 交互式图表，适合探索分析
- 两者互补，覆盖不同使用场景

### D4: 工作环境
**决定**: Jupyter Notebook 为主，命令行脚本为辅

**理由**:
- Notebook 便于探索性分析和记录
- 支持代码、文档、可视化一体化
- 便于分享和复现

### D5: 参数配置方式
**决定**: YAML 配置文件 + 代码默认值

**理由**:
- YAML 可读性好，易于修改
- 支持中文参数名称
- 分离配置与代码

## Technical Details

### 1. 数据模型定义

```python
# config/parameters.yaml 示例结构
parameters:
  ma_evaporation:
    - name: "vacuum_degree"
      chinese_name: "真空度"
      unit: "Pa"
      range: [2.0e-4, 3.0e-3]
      type: "float"

    - name: "evaporation_temp"
      chinese_name: "蒸发源温度"
      unit: "°C"
      range: [1200, 1700]
      type: "float"

    - name: "deposition_rate"
      chinese_name: "沉积速率"
      unit: "μm/s"
      range: [0.32, 1.04]
      type: "float"

quality_indicators:
  - name: "thickness"
    chinese_name: "厚度"
    unit: "μm"
    target: 8.0
    tolerance: 0.5

  - name: "sheet_resistance"
    chinese_name: "方阻"
    unit: "mΩ/□"
    target_max: 40
```

### 2. 数据加载器设计

```python
class DataLoader:
    """统一数据加载接口"""

    @staticmethod
    def from_markdown(file_path: str) -> pd.DataFrame:
        """从Markdown表格加载数据"""
        # 解析Markdown表格
        # 转换为DataFrame
        pass

    @staticmethod
    def from_csv(file_path: str) -> pd.DataFrame:
        """从CSV加载数据"""
        pass

    @staticmethod
    def from_excel(file_path: str, sheet_name: str = None) -> pd.DataFrame:
        """从Excel加载数据"""
        pass

    @staticmethod
    def auto_detect(file_path: str) -> pd.DataFrame:
        """自动检测文件类型并加载"""
        pass
```

### 3. 模型评估框架

```python
class ModelEvaluator:
    """模型评估器"""

    metrics = {
        'r2': r2_score,           # 决定系数
        'rmse': root_mean_squared_error,  # 均方根误差
        'mae': mean_absolute_error,       # 平均绝对误差
        'mape': mean_absolute_percentage_error  # 平均绝对百分比误差
    }

    def evaluate(self, model, X_test, y_test) -> Dict:
        """计算所有评估指标"""
        pass

    def cross_validate(self, model, X, y, cv=5) -> Dict:
        """交叉验证"""
        pass

    def compare_models(self, models: List, X, y) -> pd.DataFrame:
        """模型对比"""
        pass
```

### 4. 参数优化引擎

```python
class ParameterOptimizer:
    """参数优化器"""

    def optimize_single_objective(
        self,
        model,
        target_name: str,
        target_value: float,
        constraints: Dict = None
    ) -> Dict:
        """单目标优化 - 找到达到目标值的最优参数"""
        pass

    def optimize_multi_objective(
        self,
        model,
        objectives: List[Dict],  # [{'name': 'yield', 'direction': 'maximize'}, ...]
        constraints: Dict = None
    ) -> List[Dict]:
        """多目标优化 - 返回Pareto最优解集"""
        pass

    def suggest_next_experiment(
        self,
        current_data: pd.DataFrame,
        model,
        strategy: str = 'uncertainty'  # 'uncertainty', 'expected_improvement'
    ) -> Dict:
        """基于当前数据和模型，建议下一组实验参数"""
        pass
```

### 5. 报告生成器

```python
class ReportGenerator:
    """实验复盘报告生成器"""

    def generate_experiment_review(
        self,
        experiment_data: pd.DataFrame,
        analysis_results: Dict,
        output_format: str = 'markdown'
    ) -> str:
        """生成实验复盘报告"""
        sections = [
            self._summary_section(experiment_data),
            self._parameter_analysis_section(analysis_results),
            self._correlation_section(analysis_results),
            self._recommendation_section(analysis_results)
        ]
        return self._compile_report(sections, output_format)
```

## Data Schema

### 标准化实验数据表结构

```
experiments.csv
├── experiment_id      # 实验编号 (string)
├── date              # 实验日期 (datetime)
├── batch_id          # 批次号 (string)
├── operator          # 操作员 (string)
├── equipment_id      # 设备编号 (string)
│
├── [工艺参数 - MA蒸镀]
│   ├── vacuum_degree           # 真空度 (float, Pa)
│   ├── evaporation_temp        # 蒸发源温度 (float, °C)
│   ├── deposition_rate         # 沉积速率 (float, μm/s)
│   ├── substrate_temp          # 基膜温度 (float, °C)
│   ├── line_speed              # 走膜速度 (float, m/min)
│   └── ...
│
├── [工艺参数 - 涂碳]
│   ├── carbon_thickness        # 碳层厚度 (float, nm)
│   ├── curing_temp             # 固化温度 (float, °C)
│   └── ...
│
├── [工艺参数 - 预处理]
│   ├── plasma_power            # 等离子功率 (float, W)
│   ├── treatment_time          # 处理时间 (float, s)
│   └── ...
│
├── [质量指标]
│   ├── thickness               # 厚度 (float, μm)
│   ├── width                   # 幅宽 (float, mm)
│   ├── roughness_ra            # 粗糙度Ra (float, μm)
│   ├── roughness_rz            # 粗糙度Rz (float, μm)
│   ├── dyne_value              # 达因值 (float, dyn/cm)
│   ├── tensile_md              # 拉伸强度MD (float, MPa)
│   ├── tensile_td              # 拉伸强度TD (float, MPa)
│   ├── elongation_md           # 伸长率MD (float, %)
│   ├── elongation_td           # 伸长率TD (float, %)
│   ├── sheet_resistance_a      # 方阻A面 (float, mΩ/□)
│   ├── sheet_resistance_b      # 方阻B面 (float, mΩ/□)
│   ├── adhesion_test           # 附着力测试 (bool)
│   └── ...
│
├── [元数据]
│   ├── pass_fail               # 总体判定 (bool)
│   ├── notes                   # 备注 (string)
│   └── raw_material_batch      # 原材料批次 (string)
```

## Model Selection Strategy

### 建模方法选择决策树

```
                            开始
                              │
                              ▼
                    ┌─────────────────┐
                    │ 数据量是否 > 500 │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │ No                          │ Yes
              ▼                             ▼
    ┌─────────────────┐          ┌─────────────────┐
    │ 使用简单模型:    │          │ 数据关系是否线性？│
    │ • 线性回归      │          └────────┬────────┘
    │ • Ridge回归     │                   │
    │ • 多项式回归    │        ┌──────────┴──────────┐
    └─────────────────┘        │ Yes                │ No
                               ▼                    ▼
                    ┌─────────────────┐  ┌─────────────────┐
                    │ • 线性回归      │  │ • 随机森林      │
                    │ • ElasticNet   │  │ • XGBoost       │
                    │ • 响应面法(RSM)│  │ • 神经网络      │
                    └─────────────────┘  │ • SVR           │
                                         └─────────────────┘
```

### 模型对比基准

| 模型类型 | 适用场景 | 优点 | 缺点 | 最低数据量 |
|---------|---------|------|------|-----------|
| 线性回归 | 线性关系、快速基准 | 可解释性强、计算快 | 无法捕捉非线性 | 30 |
| 多项式回归 | 轻度非线性 | 仍可解释、灵活度增加 | 易过拟合 | 50 |
| Ridge/Lasso | 多重共线性 | 正则化防过拟合 | 仍是线性模型 | 30 |
| 随机森林 | 非线性、稳健性 | 不需预处理、特征重要性 | 黑箱、较慢 | 100 |
| XGBoost | 高精度预测 | 性能优异、可调参 | 需调参、易过拟合 | 200 |
| 神经网络 | 复杂非线性 | 拟合能力强 | 需大量数据、黑箱 | 500+ |

## Visualization Design

### 核心可视化图表

#### 1. 参数相关性热力图
```
用途: 展示所有参数两两之间的相关系数
工具: seaborn.heatmap
输出: 静态图 + 交互式版本
```

#### 2. 参数-结果散点矩阵
```
用途: 探索单个参数与多个质量指标的关系
工具: plotly.scatter_matrix
输出: 交互式图表
```

#### 3. 响应面图 (3D Surface)
```
用途: 展示两个参数对一个输出的联合影响
工具: plotly.surface
输出: 交互式3D图
```

#### 4. 等高线图 (Contour)
```
用途: 响应面的2D投影，便于识别最优区域
工具: matplotlib.contour
输出: 静态图
```

#### 5. 特征重要性条形图
```
用途: 模型解释 - 哪些参数最重要
工具: matplotlib.barh
输出: 静态图
```

#### 6. 预测vs实际散点图
```
用途: 模型验证 - 预测准确度可视化
工具: matplotlib.scatter (45度参考线)
输出: 静态图
```

#### 7. 残差分布图
```
用途: 模型诊断 - 检查残差是否随机分布
工具: matplotlib.scatter + histogram
输出: 静态图
```

## Alternative Approaches

### A1: 数据存储 - SQLite 数据库

**方案**: 使用 SQLite 存储所有实验数据

**优点**:
- 支持复杂查询
- 数据完整性保护
- 适合大数据量

**缺点**:
- 增加技术复杂度
- 对非技术用户不友好
- 当前数据量不需要

**结论**: 保留为未来扩展选项

### A2: 建模框架 - AutoML (auto-sklearn / H2O)

**方案**: 使用自动机器学习框架自动选择和调参

**优点**:
- 自动化程度高
- 可能发现更优模型
- 减少人工调参

**缺点**:
- 计算资源消耗大
- 结果可解释性降低
- 对小数据集可能过拟合

**结论**: 初期不采用，数据量增大后可考虑

### A3: 部署方式 - Web 应用 (Streamlit / Dash)

**方案**: 开发 Web 界面供非技术用户使用

**优点**:
- 降低使用门槛
- 便于团队协作
- 可远程访问

**缺点**:
- 开发工作量增加
- 需要部署和维护
- 可能影响迭代速度

**结论**: 二期考虑，一期专注核心分析能力

## Risk Mitigation

### R1: 数据不足风险
**风险**: 初期数据量有限，模型可能欠拟合或不稳定

**缓解措施**:
- 优先使用简单模型（线性回归、多项式回归）
- 采用交叉验证评估模型稳定性
- 持续收集数据，定期重新训练
- 使用数据增强技术（如Bootstrap）

### R2: 数据质量风险
**风险**: 实验数据可能存在错误或不一致

**缓解措施**:
- 实施严格的数据验证规则
- 异常值检测和标记
- 建立数据录入规范
- 定期数据审计

### R3: 模型过拟合风险
**风险**: 模型在训练数据上表现好，泛化能力差

**缓解措施**:
- 使用正则化技术（Ridge, Lasso, Dropout）
- 严格的训练/测试集划分
- 交叉验证
- 监控验证集指标

### R4: 参数遗漏风险
**风险**: 遗漏关键影响因素导致模型不准确

**缓解措施**:
- 与工艺专家合作确认参数清单
- 持续收集和补充参数
- 残差分析识别遗漏因素
- 保持模型可更新性

### R5: 用户采纳风险
**风险**: 工程师不信任或不使用模型结果

**缓解措施**:
- 提供模型可解释性（特征重要性、SHAP值）
- 从简单模型开始建立信任
- 记录预测vs实际的验证结果
- 将模型建议作为参考而非强制

## Performance Benchmarks

### 系统性能目标

| 操作 | 目标响应时间 | 测试条件 |
|-----|-------------|---------|
| 数据加载 | < 5s | 1000条记录 |
| 统计分析 | < 10s | 1000条 × 30列 |
| 相关性矩阵 | < 5s | 30 × 30 参数 |
| 模型训练（线性） | < 10s | 1000条训练数据 |
| 模型训练（RF） | < 60s | 1000条训练数据 |
| 单次预测 | < 1s | 单组参数 |
| 参数优化 | < 30s | 单目标 |
| 报告生成 | < 10s | 完整报告 |

## Revision History

| 版本 | 日期 | 变更说明 | 作者 |
|-----|------|---------|------|
| 1.0 | 2026-01-27 | 初稿创建 | Claude |
