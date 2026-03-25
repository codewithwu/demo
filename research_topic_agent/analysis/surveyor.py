"""方向调研器 - 梳理研究方向的现状、趋势、空白点"""

from typing import TypedDict

from ..models import Paper, ResearchQuestion


class SurveyResult(TypedDict):
    """调研结果"""
    research_topics: dict[str, str]
    trends: list[str]
    gaps: list[str]
    key_papers: list[str]


class DirectionSurveyor:
    """研究方向调研器"""

    def survey(
        self, papers: list[Paper], question: ResearchQuestion
    ) -> SurveyResult:
        """
        对研究方向进行全景调研

        Args:
            papers: 检索到的相关论文
            question: 研究问题

        Returns:
            调研结果
        """
        # 分析研究方向
        topics = self._extract_research_topics(papers)

        # 识别研究趋势
        trends = self._extract_trends(papers)

        # 识别研究空白点
        gaps = self._extract_research_gaps(papers, question)

        # 识别关键论文
        key_papers = self._identify_key_papers(papers)

        return SurveyResult(
            research_topics=topics,
            trends=trends,
            gaps=gaps,
            key_papers=key_papers,
        )

    def _extract_research_topics(
        self, papers: list[Paper]
    ) -> dict[str, str]:
        """提取研究方向"""
        topics = {}

        # 基于关键词聚类
        all_keywords = []
        for paper in papers:
            all_keywords.extend(paper.keywords)

        # 统计高频关键词
        keyword_counts: dict[str, int] = {}
        for kw in all_keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1

        # 转换为研究方向描述
        for kw, count in sorted(
            keyword_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            if count >= 2:
                topics[kw] = f"涉及 {count} 篇论文，是当前研究热点"

        return topics

    def _extract_trends(self, papers: list[Paper]) -> list[str]:
        """提取研究趋势"""
        trends = []

        # 按年份分组
        year_counts: dict[int, int] = {}
        for paper in papers:
            year_counts[paper.year] = year_counts.get(paper.year, 0) + 1

        # 判断趋势
        if year_counts.get(2024, 0) >= 3:
            trends.append(
                "2024年研究活跃，大语言模型在医疗领域应用进入快速发展期"
            )

        # 基于关键词判断
        recent_papers = [p for p in papers if p.year >= 2023]
        if any("multi-modal" in p.keywords for p in recent_papers):
            trends.append("多模态融合成为新趋势，结合影像和文本")

        if any("privacy" in p.keywords or "RLHF" in p.keywords
               for p in recent_papers):
            trends.append("安全和隐私问题受到更多关注")

        return trends

    def _extract_research_gaps(
        self, papers: list[Paper], question: ResearchQuestion
    ) -> list[str]:
        """提取研究空白点"""
        gaps = []

        # 检查是否有中文相关研究
        has_chinese = any(
            "Chinese" in p.title or "中文" in p.title
            for p in papers
        )
        if not has_chinese:
            gaps.append("中文医学场景研究较少，存在本土化机会")

        # 检查是否有特定方法
        has_rag = any("RAG" in p.keywords for p in papers)
        if not has_rag:
            gaps.append("RAG增强生成在医疗诊断中的应用尚未充分探索")

        # 检查是否有限制性研究
        has_limitation = any("limitation" in p.title.lower()
                             for p in papers)
        if not has_limitation:
            gaps.append("对LLM局限性的系统研究不足")

        # 检查是否有时效性问题
        recent_count = sum(1 for p in papers if p.year >= 2023)
        if recent_count < len(papers) * 0.5:
            gaps.append("部分研究基于较早数据，可能存在时效性偏差")

        return gaps

    def _identify_key_papers(self, papers: list[Paper]) -> list[str]:
        """识别关键论文（高引用）"""
        sorted_papers = sorted(papers, key=lambda p: p.citations, reverse=True)
        return [p.id for p in sorted_papers[:3]]
