"""P28 测试问题集 — KB + ERP 混合场景"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TestQuestion:
    id: str
    question: str
    category: str  # kb_only | erp_only | mixed
    description: str = ""


QUESTIONS = [
    # ── KB-only: 公司/产品/行业知识 ──
    TestQuestion(
        id="KB-01",
        question="恩派克的主要产品有哪些？各产品的市场定位如何？",
        category="kb_only",
        description="公司产品线概览",
    ),
    TestQuestion(
        id="KB-02",
        question="复合铜箔和传统铜箔相比有什么技术优势？",
        category="kb_only",
        description="产品技术对比",
    ),
    TestQuestion(
        id="KB-03",
        question="目前固态电池行业的发展趋势是什么？对复合集流体有何影响？",
        category="kb_only",
        description="行业趋势分析",
    ),
    TestQuestion(
        id="KB-04",
        question="恩派克的主要竞争对手有哪些？竞争格局如何？",
        category="kb_only",
        description="竞争分析",
    ),

    # ── ERP-only: 采购/库存/资产 ──
    TestQuestion(
        id="ERP-01",
        question="目前库存中铜箔相关物料有哪些？各自库存数量是多少？",
        category="erp_only",
        description="库存查询",
    ),
    TestQuestion(
        id="ERP-02",
        question="最近的采购订单有哪些？金额最大的是哪几笔？",
        category="erp_only",
        description="采购单据查询",
    ),
    TestQuestion(
        id="ERP-03",
        question="公司目前有哪些固定资产？按部门分布情况如何？",
        category="erp_only",
        description="固定资产查询",
    ),
    TestQuestion(
        id="ERP-04",
        question="今天铜期货的价格是多少？最近一个月的走势如何？",
        category="erp_only",
        description="期货数据查询",
    ),

    # ── Mixed: 需要同时查 KB + ERP ──
    TestQuestion(
        id="MIX-01",
        question="根据公司产品规划和当前库存情况，铜箔相关原材料的备货是否充足？",
        category="mixed",
        description="需要KB(产品规划)+ERP(库存)综合判断",
    ),
    TestQuestion(
        id="MIX-02",
        question="结合铜期货走势和公司采购记录，最近的铜材采购成本是否合理？",
        category="mixed",
        description="需要ERP(期货+采购)+KB(成本分析)综合判断",
    ),
]
