# 样本问题库 (Sample Question Bank)

**Created**: 2026-03-08
**Last Updated**: 2026-03-08
**Total Questions**: 52
**Coverage**: 7 departments

## Summary Statistics

| Department | Count | Simple | Medium | Complex |
|------------|-------|--------|--------|---------|
| 采购 (Procurement) | 10 | 2 | 4 | 4 |
| 销售 (Sales) | 9 | 2 | 3 | 4 |
| 生产 (Production) | 8 | 2 | 3 | 3 |
| 研发 (R&D) | 7 | 1 | 3 | 3 |
| 供应链 (Supply Chain) | 6 | 1 | 3 | 2 |
| 财务 (Finance) | 6 | 2 | 2 | 2 |
| 管理 (Management) | 6 | 0 | 2 | 4 |

| Answer Type | Count |
|-------------|-------|
| lookup | 12 |
| analysis | 22 |
| recommendation | 18 |

---

## 一、采购部 (Procurement)

### Q-001: 采购审批合理性
- **question_zh**: 有一份采购申请买入卡尺1支。我可以调阅这个人买过几支卡尺，这个部门有多少支卡尺，购买的是否合理。
- **question_en**: A purchase request for 1 caliper. Can I check how many calipers this person has bought, how many the department has, and whether this purchase is reasonable?
- **department**: 采购
- **scenario**: 采购审批时判断申请合理性
- **data_sources**: ERP(采购记录), ERP(资产台账), ERP(部门资产)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: 2/22 screenshot (翁伟嘉)

### Q-002: 原材料采购量分析
- **question_zh**: 采购要买入10吨氧化铜。我可以调取到氧化铜的现有库存对应的订单需求情况，根据期货走势分析买入10吨是多了还是少了，是否合理。
- **question_en**: Procurement wants to buy 10 tons of copper oxide. Can I pull current inventory vs order demand, and analyze against futures trends whether 10 tons is too much or too little?
- **department**: 采购
- **scenario**: 大宗原材料采购量决策
- **data_sources**: ERP(库存), ERP(订单), 期货数据(外部), 历史采购记录
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: none
- **priority**: high
- **source**: 2/22 screenshot (翁伟嘉)

### Q-003: 供应商谈判准备
- **question_zh**: 我要和供应商谈判。我可以调取之前和这位供应商的会议记录、往来邮件和信息、合作次数和每次合作的表现，该供应商的外网信息评价、在产业链内的优势劣势，来为我提供谈判的信息。
- **question_en**: I need to negotiate with a supplier. Can I pull our meeting records, emails, cooperation history, performance ratings, plus their public reputation and industry position to prepare?
- **department**: 采购/供应链
- **scenario**: 供应商谈判前信息准备
- **data_sources**: 会议记录, 邮件系统, CRM(合作记录), 外部信息(企业信用/评价), 行业分析
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: 2/22 screenshot (翁伟嘉)

### Q-005: 供应商价格对比
- **question_zh**: PET薄膜目前有哪几家供应商在供货？各家的价格、交期、质量评分分别是多少？有没有新的潜在供应商可以考虑？
- **question_en**: Which suppliers currently supply PET film? What are their prices, lead times, and quality scores? Are there potential new suppliers to consider?
- **department**: 采购
- **scenario**: 供应商评估与比价
- **data_sources**: ERP(采购价格), CRM(供应商档案), 外部信息(行业供应商)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-006: 采购成本趋势
- **question_zh**: 过去12个月铜箔基材的采购单价变化趋势是怎样的？和同期铜价走势相比，我们的采购价是偏高还是偏低？
- **question_en**: What's the price trend for copper foil base material over the past 12 months? Compared to copper futures, are we buying high or low?
- **department**: 采购
- **scenario**: 采购成本分析与市场对标
- **data_sources**: ERP(采购历史), 期货数据(外部), 行业价格指数
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-007: 采购合同到期提醒
- **question_zh**: 未来3个月内有哪些供应商合同即将到期？这些合同的金额和续签条件是什么？
- **question_en**: Which supplier contracts expire in the next 3 months? What are the contract values and renewal terms?
- **department**: 采购
- **scenario**: 合同管理与续签准备
- **data_sources**: ERP(合同管理), CRM(供应商档案)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-008: 采购替代材料分析
- **question_zh**: 目前铝箔基材成本占比较高，有没有替代材料可以降低成本？替代后对产品性能会有什么影响？
- **question_en**: Aluminum foil base material cost is high. Are there alternative materials to reduce cost? How would they affect product performance?
- **department**: 采购/研发
- **scenario**: 降本替代方案评估
- **data_sources**: 知识库(技术标准), 研究报告, 外部信息(材料数据库)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

### Q-009: 供应商交期达成率
- **question_zh**: 上个季度各主要供应商的交期达成率是多少？哪些供应商经常延迟？
- **question_en**: What was each major supplier's on-time delivery rate last quarter? Which ones frequently delayed?
- **department**: 采购
- **scenario**: 供应商绩效考核
- **data_sources**: ERP(收货记录), ERP(采购订单)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-010: 采购预算执行情况
- **question_zh**: 本月采购部的预算执行到什么程度了？哪些品类超支？哪些还有余额？
- **question_en**: How is procurement's budget execution this month? Which categories are over budget? Which have remaining balance?
- **department**: 采购/财务
- **scenario**: 预算管控
- **data_sources**: ERP(采购订单), ERP(财务预算)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

---

## 二、销售部 (Sales)

### Q-004: 销售定价决策
- **question_zh**: 销售申请用5元的价格卖出10万平米的MA。我可以快速的分析这个价格对于我们目前的成本是否值得去做，还有这个客户是否值得去合作等等......
- **question_en**: Sales wants to sell 100k sqm of MA at 5 yuan. Can I quickly analyze whether this price covers our costs and whether this customer is worth working with?
- **department**: 销售
- **scenario**: 销售报价审批
- **data_sources**: ERP(成本数据), ERP(定价历史), CRM(客户档案), 利润率分析模型
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: none
- **priority**: high
- **source**: 2/22 screenshot (翁伟嘉)

### Q-011: 客户订单趋势
- **question_zh**: U&S ENERGY过去6个月的下单趋势怎么样？订单量是在增长还是下降？下个季度预计会怎样？
- **question_en**: What's the order trend from U&S ENERGY over the past 6 months? Growing or declining? What's the forecast for next quarter?
- **department**: 销售
- **scenario**: 大客户订单分析与预测
- **data_sources**: ERP(订单记录), CRM(客户档案), 会议记录
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-012: 产品报价参考
- **question_zh**: 复合铜箔6μm规格的最近报价是多少？同行的报价水平大概是什么范围？我们报价有竞争力吗？
- **question_en**: What's our latest quote for 6μm composite copper foil? What's the industry price range? Are we competitive?
- **department**: 销售
- **scenario**: 竞争性报价制定
- **data_sources**: ERP(报价记录), 外部信息(行业报价), 知识库(竞争对手档案)
- **complexity**: medium
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-013: 客户应收账款
- **question_zh**: 目前哪些客户的应收账款超过了信用期限？金额分别是多少？需要重点催收的有哪几家？
- **question_en**: Which customers have receivables past their credit terms? What are the amounts? Which ones need priority collection?
- **department**: 销售/财务
- **scenario**: 应收账款管理
- **data_sources**: ERP(应收账款), CRM(客户信用档案)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-014: 新客户开发分析
- **question_zh**: 目前国内有哪些电池厂还没有使用复合集流体？他们的产能规模和技术路线是什么？哪些最有可能成为我们的客户？
- **question_en**: Which domestic battery makers haven't adopted composite current collectors yet? What are their capacities and tech routes? Which are most likely prospects?
- **department**: 销售/管理
- **scenario**: 市场开发与客户获取
- **data_sources**: 知识库(行业背景), 研究报告(公司档案), 外部信息(行业数据库)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-015: 客户投诉分析
- **question_zh**: 最近3个月收到的客户投诉有哪些？按产品和问题类型分类汇总一下。最常见的投诉是什么？
- **question_en**: What customer complaints have we received in the past 3 months? Summarize by product and issue type. What's the most common complaint?
- **department**: 销售
- **scenario**: 客户满意度管理
- **data_sources**: CRM(投诉记录), ERP(质检记录)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-016: 销售目标达成
- **question_zh**: 本月各销售人员的业绩目标完成了多少？哪些人完成率最高？哪些产品线卖得最好？
- **question_en**: How are individual sales reps tracking against targets this month? Who's performing best? Which product lines are selling most?
- **department**: 销售
- **scenario**: 销售绩效跟踪
- **data_sources**: ERP(销售数据), CRM(销售目标)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-017: 产品交叉销售
- **question_zh**: 我们的易开盖客户中，有哪些也在使用电池材料？有没有交叉销售复合集流体的机会？
- **question_en**: Among our easy-open lid customers, which ones also use battery materials? Are there cross-selling opportunities for composite current collectors?
- **department**: 销售
- **scenario**: 双主业客户交叉销售
- **data_sources**: CRM(客户档案), ERP(销售记录), 知识库(公司概览)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

---

## 三、生产部 (Production)

### Q-018: 生产进度查询
- **question_zh**: U&S ENERGY的第3批订单目前生产到什么阶段了？预计什么时候能完成？有没有延期风险？
- **question_en**: What stage is U&S ENERGY's 3rd batch order at? When is expected completion? Any delay risk?
- **department**: 生产
- **scenario**: 订单生产进度跟踪
- **data_sources**: ERP(生产工单), ERP(排产计划)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-019: 良率分析
- **question_zh**: 本月复合铜箔各条产线的良率分别是多少？和上个月相比有提升还是下降？良率低的产线主要问题出在哪里？
- **question_en**: What's the yield rate for each composite copper foil production line this month? Up or down vs last month? What's causing low yield on underperforming lines?
- **department**: 生产
- **scenario**: 产品良率监控与改善
- **data_sources**: ERP(质检数据), ERP(生产记录), 知识库(缺陷分类指南)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-020: 设备故障与停机
- **question_zh**: 过去一个月各条产线的停机时间分别是多少？停机原因分类是什么？哪台设备故障最频繁？
- **question_en**: How much downtime did each production line have last month? What were the causes? Which equipment had the most failures?
- **department**: 生产
- **scenario**: 设备管理与故障分析
- **data_sources**: ERP(设备维修记录), ERP(生产日志)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-021: 产能利用率
- **question_zh**: 目前5条铜箔线和5条铝箔线的实际产能利用率各是多少？按照目前的订单量，需要启动多少条产线？
- **question_en**: What's the current capacity utilization for our 5 copper foil lines and 5 aluminum foil lines? Based on current orders, how many lines should be running?
- **department**: 生产
- **scenario**: 产能规划与排产
- **data_sources**: ERP(生产数据), ERP(订单), 知识库(产能规划)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-022: 原材料消耗异常
- **question_zh**: 本周3号产线的PET薄膜消耗量比标准高了15%，可能的原因是什么？之前有没有类似的情况？
- **question_en**: Line 3's PET film consumption is 15% above standard this week. What might be causing this? Has this happened before?
- **department**: 生产
- **scenario**: 物料消耗异常分析
- **data_sources**: ERP(物料消耗), ERP(生产参数), 历史异常记录
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-023: 工艺参数优化
- **question_zh**: 根据最近3个月的生产数据，铜箔沉积工序的温度和电流密度在什么范围内良率最高？
- **question_en**: Based on the last 3 months of production data, at what temperature and current density ranges does copper deposition yield peak?
- **department**: 生产/研发
- **scenario**: 工艺参数优化
- **data_sources**: ERP(生产参数), ERP(质检数据), 研究报告(实验数据)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

### Q-024: 排产冲突
- **question_zh**: 下周有3个客户的订单需要同时排产，但只有2条可用产线。应该怎么排优先级？各自的交期和利润率是多少？
- **question_en**: Next week 3 customer orders need production but only 2 lines are available. How should we prioritize? What are the delivery dates and margins?
- **department**: 生产
- **scenario**: 排产优先级决策
- **data_sources**: ERP(订单), ERP(排产计划), ERP(成本数据)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-025: 班组绩效对比
- **question_zh**: 本月白班和夜班的产量、良率、废品率分别是多少？哪个班组表现更好？
- **question_en**: What are the output, yield, and scrap rates for day shift vs night shift this month? Which team performed better?
- **department**: 生产
- **scenario**: 班组绩效管理
- **data_sources**: ERP(生产记录), ERP(质检数据)
- **complexity**: simple
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: low
- **source**: brainstorm

---

## 四、研发部 (R&D)

### Q-026: 技术标准查询
- **question_zh**: 复合铜箔6μm产品需要满足哪些技术标准？抗拉强度和延伸率的要求分别是多少？
- **question_en**: What technical standards must 6μm composite copper foil meet? What are the tensile strength and elongation requirements?
- **department**: 研发
- **scenario**: 产品技术标准查阅
- **data_sources**: 知识库(技术标准), 知识库(测试程序指南)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: full
- **priority**: high
- **source**: brainstorm

### Q-027: 竞争对手技术对比
- **question_zh**: 重庆金美和双星新材在复合铜箔领域的技术路线和我们有什么区别？他们的产品性能参数怎么样？
- **question_en**: How do Chongqing Jinmei and Shuangxing New Materials differ from us in composite copper foil technology? What are their product specs?
- **department**: 研发
- **scenario**: 竞争技术分析
- **data_sources**: 知识库(竞争对手档案), 研究报告(公司档案研究), 外部信息(专利/论文)
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-028: 固态电池材料需求
- **question_zh**: 固态电池对集流体材料有什么特殊要求？我们现有的复合集流体技术能否适配？需要做哪些改进？
- **question_en**: What special requirements does solid-state batteries place on current collectors? Can our existing composite technology adapt? What improvements are needed?
- **department**: 研发
- **scenario**: 新技术路线评估
- **data_sources**: 知识库(技术路线图), 研究报告(固态电池), 外部信息(学术文献)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-029: 实验数据查询
- **question_zh**: 上个月做的高温老化实验结果怎么样？不同温度条件下样品的阻抗变化是什么趋势？
- **question_en**: What were the results of last month's high-temperature aging tests? How did sample impedance change across temperature conditions?
- **department**: 研发
- **scenario**: 实验数据分析
- **data_sources**: 实验数据库, 知识库(测试程序指南)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

### Q-030: 专利和知识产权
- **question_zh**: 我们目前在复合集流体领域有多少项专利？竞争对手有哪些关键专利？有没有专利侵权风险？
- **question_en**: How many patents do we hold in composite current collectors? What key patents do competitors hold? Any infringement risks?
- **department**: 研发
- **scenario**: 知识产权管理
- **data_sources**: 内部专利库, 外部信息(专利数据库)
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-031: 新产品开发进度
- **question_zh**: 复合铝箔新规格产品的开发进度到哪一步了？什么时候可以送样给客户？还有哪些技术难点需要攻克？
- **question_en**: How far along is the new composite aluminum foil spec development? When can we send samples to customers? What technical challenges remain?
- **department**: 研发
- **scenario**: 新产品开发进度跟踪
- **data_sources**: 项目管理系统, 会议记录, 实验数据
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-032: 行业技术趋势
- **question_zh**: 目前复合集流体行业的主流技术路线是什么？有没有新的技术突破可能影响我们的技术方向？
- **question_en**: What are the mainstream technology routes in composite current collectors? Are there new breakthroughs that might affect our technology direction?
- **department**: 研发
- **scenario**: 技术情报跟踪
- **data_sources**: 知识库(行业背景), 研究报告, 外部信息(学术/行业会议)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

---

## 五、供应链/物流 (Supply Chain)

### Q-033: 库存预警
- **question_zh**: 目前哪些原材料的库存低于安全库存线？预计还能支撑多少天的生产？
- **question_en**: Which raw materials are below safety stock levels? How many days of production can current stock support?
- **department**: 供应链
- **scenario**: 库存安全管理
- **data_sources**: ERP(库存), ERP(生产计划), ERP(安全库存设定)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-034: 物流成本分析
- **question_zh**: 从高邮工厂发货到各主要客户的物流成本分别是多少？有没有更优的物流方案可以降低成本？
- **question_en**: What's the shipping cost from Gaoyou plant to each major customer? Are there better logistics options to reduce cost?
- **department**: 供应链
- **scenario**: 物流成本优化
- **data_sources**: ERP(物流费用), 外部信息(物流服务商报价)
- **complexity**: medium
- **answer_type**: recommendation
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-035: 交期风险评估
- **question_zh**: 根据目前的库存、在制品和排产计划，下个月的订单交期有没有风险？哪些订单可能延迟？
- **question_en**: Given current inventory, WIP, and production schedule, are there delivery risks for next month's orders? Which might be delayed?
- **department**: 供应链
- **scenario**: 交期风险预警
- **data_sources**: ERP(库存), ERP(在制品), ERP(排产计划), ERP(订单)
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-036: 供应链中断应对
- **question_zh**: 如果某个关键供应商突然断供，我们有多少天的库存缓冲？备选供应商需要多长时间才能供货？
- **question_en**: If a key supplier suddenly stops delivery, how many days of buffer stock do we have? How long would it take an alternate supplier to start delivering?
- **department**: 供应链
- **scenario**: 供应链风险管理
- **data_sources**: ERP(库存), CRM(供应商档案), 知识库(供应链管理体系)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-037: 成品库存周转
- **question_zh**: 各产品型号的成品库存周转天数分别是多少？哪些产品积压严重？有没有呆滞库存需要处理？
- **question_en**: What's the inventory turnover for each product? Which products have excessive stock? Any dead stock needing disposal?
- **department**: 供应链
- **scenario**: 库存优化
- **data_sources**: ERP(库存), ERP(销售记录)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

### Q-038: 进口材料通关
- **question_zh**: 从韩国进口的靶材目前通关到什么阶段了？预计什么时候能到仓库？上一批通关用了多长时间？
- **question_en**: What stage is the imported target material from Korea at in customs? When will it arrive at the warehouse? How long did the last batch take?
- **department**: 供应链
- **scenario**: 进口物流跟踪
- **data_sources**: 物流系统, ERP(采购订单), 报关系统
- **complexity**: medium
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: medium
- **source**: brainstorm

---

## 六、财务部 (Finance)

### Q-039: 产品成本构成
- **question_zh**: 复合铜箔6μm产品的成本构成是怎样的？原材料、人工、能源、折旧各占多少比例？和上个季度相比有什么变化？
- **question_en**: What's the cost breakdown for 6μm composite copper foil? What's the ratio of materials, labor, energy, depreciation? How has it changed vs last quarter?
- **department**: 财务
- **scenario**: 产品成本分析
- **data_sources**: ERP(成本核算), ERP(生产数据)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-040: 盈亏平衡分析
- **question_zh**: 按照目前的成本结构，复合铜箔的盈亏平衡点是多少平米？如果产能利用率达到80%，毛利率能到多少？
- **question_en**: At current cost structure, what's the breakeven volume for composite copper foil in sqm? If capacity utilization reaches 80%, what margin can we achieve?
- **department**: 财务
- **scenario**: 盈利分析与预测
- **data_sources**: ERP(成本数据), ERP(产能数据), 财务模型
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-041: 现金流查询
- **question_zh**: 本月复合集流体事业部的经营现金流情况怎么样？应收和应付的账期分别是多少天？
- **question_en**: How is the CCC division's operating cash flow this month? What are the AR and AP days outstanding?
- **department**: 财务
- **scenario**: 现金流管理
- **data_sources**: ERP(财务数据), ERP(应收应付)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-042: 投资回报分析
- **question_zh**: 复合集流体项目已投入30.89亿元，按照目前的订单量和产能爬坡速度，预计什么时候能收回投资？
- **question_en**: The CCC project has invested 3.089B yuan. At current order volume and capacity ramp rate, when do we expect ROI breakeven?
- **department**: 财务/管理
- **scenario**: 投资回报评估
- **data_sources**: ERP(财务数据), ERP(订单), 知识库(公司概览), 财务模型
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-043: 费用报销审核
- **question_zh**: 这个月各部门的费用报销金额分别是多少？有没有超出预算的部门？最大的几笔报销是什么？
- **question_en**: What's each department's expense reimbursement total this month? Any departments over budget? What are the largest claims?
- **department**: 财务
- **scenario**: 费用管控
- **data_sources**: ERP(费用系统), ERP(预算)
- **complexity**: simple
- **answer_type**: lookup
- **kb_coverage**: none
- **priority**: low
- **source**: brainstorm

### Q-044: 税务优惠利用
- **question_zh**: 作为国家高新技术企业，我们目前享受了哪些税收优惠？研发费用加计扣除的金额是多少？还有没有其他可以申请的优惠政策？
- **question_en**: As a national high-tech enterprise, what tax benefits are we using? How much is our R&D expense super-deduction? Are there other policies we can apply for?
- **department**: 财务
- **scenario**: 税务筹划
- **data_sources**: 财务数据, 知识库(企业资质), 外部信息(税务政策)
- **complexity**: medium
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

---

## 七、管理层 (Management)

### Q-045: 经营仪表盘
- **question_zh**: 给我一份本周的经营简报：营收、订单、产量、良率、库存、应收款的关键数字和上周对比。
- **question_en**: Give me a weekly business brief: revenue, orders, output, yield, inventory, receivables — key numbers vs last week.
- **department**: 管理
- **scenario**: 高管经营决策支持
- **data_sources**: ERP(全模块), CRM, 生产系统
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: none
- **priority**: high
- **source**: brainstorm

### Q-046: 战略方向评估
- **question_zh**: 目前复合集流体行业的竞争格局怎么样？我们在技术、产能、客户方面和主要竞争对手相比处于什么位置？
- **question_en**: What's the current competitive landscape in composite current collectors? Where do we stand vs competitors in technology, capacity, and customers?
- **department**: 管理
- **scenario**: 战略竞争分析
- **data_sources**: 知识库(行业背景), 知识库(竞争对手档案), 研究报告, 外部信息
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-047: 人力资源需求
- **question_zh**: 按照明年的产能扩张计划，各部门需要增加多少人？目前的招聘进度怎么样？关键岗位有没有到位？
- **question_en**: Based on next year's capacity expansion plan, how many additional staff does each department need? How's recruitment progressing? Are key positions filled?
- **department**: 管理
- **scenario**: 人力资源规划
- **data_sources**: HR系统, ERP(产能规划), 知识库(组织结构)
- **complexity**: medium
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

### Q-048: 双主业协同分析
- **question_zh**: 金属包装和复合集流体两个事业部之间有哪些可以协同的地方？技术、客户、供应链方面有什么交叉点？
- **question_en**: What synergies exist between metal packaging and composite current collector divisions? Any crossover in technology, customers, supply chain?
- **department**: 管理
- **scenario**: 业务协同与战略规划
- **data_sources**: 知识库(公司概览), 知识库(业务运营), CRM, ERP
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: medium
- **source**: brainstorm

### Q-049: 风险预警
- **question_zh**: 目前公司面临的主要运营风险有哪些？原材料价格波动、客户集中度、技术路线变化等方面的风险分别有多大？
- **question_en**: What are the major operational risks facing the company? How significant are risks from material price volatility, customer concentration, and technology shifts?
- **department**: 管理
- **scenario**: 风险管理
- **data_sources**: 知识库(战略重点), 知识库(行业背景), ERP(财务数据), 外部信息
- **complexity**: complex
- **answer_type**: analysis
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-050: 政策与合规
- **question_zh**: GB38031-2025电池安全新国标对我们的产品有什么影响？我们需要做哪些调整来满足新标准？
- **question_en**: How does the new GB38031-2025 battery safety standard affect our products? What adjustments do we need to make?
- **department**: 管理/研发
- **scenario**: 政策法规合规
- **data_sources**: 知识库(GB38031-2025), 知识库(技术标准), 研究报告
- **complexity**: medium
- **answer_type**: recommendation
- **kb_coverage**: full
- **priority**: high
- **source**: brainstorm

### Q-051: 国际市场拓展
- **question_zh**: 除了韩国U&S ENERGY，还有哪些海外电池企业可能对复合集流体有需求？进入这些市场需要什么认证？
- **question_en**: Besides Korea's U&S ENERGY, which overseas battery companies might need composite current collectors? What certifications are needed for those markets?
- **department**: 管理/销售
- **scenario**: 国际业务拓展
- **data_sources**: 知识库(竞争对手档案), 研究报告, 外部信息(海外市场)
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm

### Q-052: 产能扩张决策
- **question_zh**: 目前的100条铜箔线规划，按照订单增长趋势，应该什么节奏扩产？每条新线的投资回报期预计多久？
- **question_en**: Given the 100-line copper foil capacity plan, at what pace should we expand based on order growth trends? What's the expected payback period per new line?
- **department**: 管理/财务
- **scenario**: 产能扩张投资决策
- **data_sources**: ERP(订单趋势), ERP(财务数据), 知识库(产能规划), 财务模型
- **complexity**: complex
- **answer_type**: recommendation
- **kb_coverage**: partial
- **priority**: high
- **source**: brainstorm
