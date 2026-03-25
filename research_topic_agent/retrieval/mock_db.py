"""Mock文献数据库"""

from ..demo_data import get_mock_papers
from ..models import Paper


class MockPaperDatabase:
    """Mock学术文献数据库"""

    def __init__(self):
        self._papers = get_mock_papers()
        self._index = {p.id: p for p in self._papers}

    def search(
        self, query: str, domain: str = "", limit: int = 10
    ) -> list[tuple[Paper, float]]:
        """
        搜索相关论文

        Args:
            query: 查询关键词
            domain: 研究领域筛选
            limit: 返回数量限制

        Returns:
            (论文, 相关度得分) 列表，按相关度降序
        """
        query_lower = query.lower()
        query_keywords = set(query_lower.replace(",", " ").split())

        results = []
        for paper in self._papers:
            # 领域筛选
            if domain and paper.domain != domain:
                continue

            # 计算相关度
            relevance = self._calculate_relevance(paper, query_keywords)
            if relevance > 0:
                results.append((paper, relevance))

        # 排序
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:limit]

    def _calculate_relevance(self, paper: Paper, query_keywords: set[str]) -> float:
        """计算论文与查询的相关度"""
        score = 0.0

        # 标题匹配
        title_words = set(paper.title.lower().replace(":", " ").replace(",", " ").split())
        title_match = query_keywords & title_words
        score += len(title_match) * 0.3

        # 关键词匹配
        keyword_set = set(k.lower() for k in paper.keywords)
        keyword_match = query_keywords & keyword_set
        score += len(keyword_match) * 0.4

        # 摘要匹配
        abstract_words = set(paper.abstract.lower().split())
        abstract_match = query_keywords & abstract_words
        score += len(abstract_match) * 0.2

        # 归一化到0-1
        max_possible = len(query_keywords) * 0.9
        return min(score / max_possible, 1.0) if max_possible > 0 else 0.0

    def get_paper(self, paper_id: str) -> Paper | None:
        """根据ID获取论文"""
        return self._index.get(paper_id)

    def get_papers_by_ids(self, paper_ids: list[str]) -> list[Paper]:
        """根据ID列表获取论文"""
        return [self._index[pid] for pid in paper_ids if pid in self._index]
