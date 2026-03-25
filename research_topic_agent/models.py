"""数据模型定义"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class VenueType(Enum):
    """发表载体类型"""
    TOP_CONFERENCE = "top_conference"      # 顶会 (3星)
    JOURNAL = "journal"                     # 期刊 (2星)
    PREPRINT = "preprint"                  # 预印本 (1星)
    BLOG = "blog"                          # 博客 (0星)


class SourceGrade(Enum):
    """来源分级"""
    HIGH = 3    # 顶会/核心期刊
    MEDIUM = 2  # 普通期刊/会议
    LOW = 1     # 预印本/博客
    UNKNOWN = 0 # 未知来源


@dataclass
class Paper:
    """学术论文"""
    id: str
    title: str
    authors: list[str]
    abstract: str
    venue: str                          # 发表 venue
    venue_type: VenueType
    year: int
    citations: int = 0
    keywords: list[str] = field(default_factory=list)
    domain: str = ""                    # 研究领域

    @property
    def source_grade(self) -> SourceGrade:
        return {
            VenueType.TOP_CONFERENCE: SourceGrade.HIGH,
            VenueType.JOURNAL: SourceGrade.MEDIUM,
            VenueType.PREPRINT: SourceGrade.LOW,
            VenueType.BLOG: SourceGrade.UNKNOWN,
        }.get(self.venue_type, SourceGrade.UNKNOWN)


@dataclass
class Claim:
    """论文中的主张/结论"""
    id: str
    paper_id: str
    content: str
    supporting_papers: list[str] = field(default_factory=list)  # 支持此结论的其他论文
    contradicting_papers: list[str] = field(default_factory=list)  # 矛盾论文


@dataclass
class ResearchPath:
    """研究路径/方向"""
    id: str
    name: str
    hypothesis: str                     # 核心假设
    methodology: str                     # 方法论描述
    novelty: str = ""                    # 创新点
    feasibility: float = 0.5            # 可行性 0-1
    risk: str = ""                       # 风险描述
    supporting_papers: list[str] = field(default_factory=list)


@dataclass
class ResearchQuestion:
    """结构化的研究问题"""
    id: str
    raw_input: str                       # 用户原始输入
    topic: str                           # 研究主题
    scope: str                           # 研究范围
    keywords: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)


@dataclass
class Evidence:
    """证据"""
    claim: str
    source_paper_id: str
    supporting_strength: float = 0.5    # 支持强度 0-1
    confidence: float = 0.5              # 置信度 0-1


@dataclass
class ConfidenceAssessment:
    """置信度评估"""
    overall: float                       # 综合置信度 0-1
    source_quality: float = 0.5         # 来源质量得分
    evidence_quantity: float = 0.5       # 证据数量得分
    recency: float = 0.5                # 时效性得分
    conflicts: list[str] = field(default_factory=list)  # 冲突描述列表


@dataclass
class ResearchTopic:
    """研究选题（最终输出）"""
    id: str
    research_question: ResearchQuestion
    research_paths: list[ResearchPath]
    evidence_chain: list[Evidence]
    confidence: ConfidenceAssessment
    recommendations: list[str] = field(default_factory=list)  # 建议


@dataclass
class TopicState:
    """选题流程状态"""
    current_step: str = "initial"        # 当前步骤
    research_question: Optional[ResearchQuestion] = None
    retrieved_papers: list[Paper] = field(default_factory=list)
    survey_result: Optional[dict] = None
    path_comparison: Optional[dict] = None
    convergence_result: Optional[dict] = None
    final_topic: Optional[ResearchTopic] = None
    user_confirmed: bool = False
    messages: list[str] = field(default_factory=list)
