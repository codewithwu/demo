"""文献检索器"""

from ..models import Paper, ResearchQuestion
from .mock_db import MockPaperDatabase


class PaperRetriever:
    """学术文献检索器"""

    def __init__(self):
        self._db = MockPaperDatabase()

    def retrieve(
        self, research_question: ResearchQuestion, limit: int = 10
    ) -> list[Paper]:
        """
        根据研究问题检索相关论文

        Args:
            research_question: 结构化研究问题
            limit: 返回数量限制

        Returns:
            检索到的论文列表，按相关度降序
        """
        # 合并主题、范围、关键词构建查询
        query_parts = [research_question.topic]
        if research_question.scope:
            query_parts.append(research_question.scope)
        query_parts.extend(research_question.keywords)
        query = " ".join(query_parts)

        # 检索
        results = self._db.search(
            query=query,
            domain="medical AI",
            limit=limit,
        )

        papers = [paper for paper, _ in results]
        return papers

    def get_paper(self, paper_id: str) -> Paper | None:
        """获取指定论文"""
        return self._db.get_paper(paper_id)

    def get_papers_by_ids(self, paper_ids: list[str]) -> list[Paper]:
        """批量获取论文"""
        return self._db.get_papers_by_ids(paper_ids)
