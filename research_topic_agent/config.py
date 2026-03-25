"""配置文件"""

# 来源分级权重
SOURCE_GRADE_WEIGHTS = {
    "high": 1.0,
    "medium": 0.6,
    "low": 0.3,
    "unknown": 0.1,
}

# 置信度计算权重
CONFIDENCE_WEIGHTS = {
    "source_quality": 0.4,
    "evidence_quantity": 0.3,
    "recency": 0.3,
}

# 时间衰减因子（论文年龄对置信度的影响）
RECENCY_DECAY_YEARS = 10

# 检索相关度阈值
RETRIEVAL_RELEVANCE_THRESHOLD = 0.3

# 路径比较维度
PATH_COMPARISON_DIMENSIONS = [
    "feasibility",
    "novelty",
    "risk",
    "evidence_strength",
]
