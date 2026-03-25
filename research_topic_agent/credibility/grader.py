"""来源分级器 - 评估文献来源可信度"""

from typing import TypedDict

from ..models import Paper, SourceGrade


class PaperGrade(TypedDict):
    """论文分级结果"""
    paper_id: str
    grade: SourceGrade
    stars: int
    reason: str


class SourceGrader:
    """来源分级器"""

    # 顶会/期刊白名单
    TOP_CONFERENCES = {
        "Nature Medicine",
        "NEJM AI",
        "Lancet Digital Health",
        "Nature Biomedical Engineering",
        "AAAI",
        "NeurIPS",
        "CVPR",
        "IEEE S&P",
        "CHIL",
    }

    REGULAR_JOURNALS = {
        "Journal of Medical Informatics",
    }

    def grade_papers(self, papers: list[Paper]) -> list[PaperGrade]:
        """
        对论文进行来源分级

        Args:
            papers: 论文列表

        Returns:
            分级结果列表
        """
        results = []
        for paper in papers:
            grade = self._grade_paper(paper)
            results.append(grade)

        return results

    def _grade_paper(self, paper: Paper) -> PaperGrade:
        """对单篇论文分级"""
        grade = paper.source_grade
        stars = grade.value
        reason = self._get_grade_reason(paper)

        return PaperGrade(
            paper_id=paper.id,
            grade=grade,
            stars=stars,
            reason=reason,
        )

    def _get_grade_reason(self, paper: Paper) -> str:
        """获取分级原因"""
        if paper.venue in self.TOP_CONFERENCES:
            return f"顶会发表: {paper.venue}"
        elif paper.venue in self.REGULAR_JOURNALS:
            return f"核心期刊: {paper.venue}"
        elif paper.venue_type.value == "preprint":
            return "预印本，未经过同行评审"
        elif paper.venue_type.value == "blog":
            return "博客/非正式发表"
        else:
            return f"其他来源: {paper.venue}"

    def get_overall_quality_score(self, papers: list[Paper]) -> float:
        """
        计算整体质量得分 (0-1)

        Args:
            papers: 论文列表

        Returns:
            质量得分
        """
        if not papers:
            return 0.0

        total = 0.0
        for paper in papers:
            # 来源基础分
            base_score = paper.source_grade.value / 3.0

            # 引用量调整
            citation_score = min(paper.citations / 300, 1.0)

            # 综合得分
            total += base_score * 0.6 + citation_score * 0.4

        return total / len(papers)
