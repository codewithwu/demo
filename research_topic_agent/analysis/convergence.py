"""收敛判断器 - 综合证据判断选题可行性"""

from ..models import ResearchPath, Paper, ConfidenceAssessment


class ConvergenceAnalyzer:
    """收敛判断分析器"""

    def analyze(
        self, paths: list[ResearchPath], papers: list[Paper]
    ) -> ConfidenceAssessment:
        """
        分析收敛性，评估选题置信度

        Args:
            paths: 候选研究路径
            papers: 相关论文

        Returns:
            置信度评估
        """
        # 计算各维度得分
        source_quality = self._evaluate_source_quality(papers)
        evidence_quantity = self._evaluate_evidence_quantity(
            paths, papers
        )
        recency = self._evaluate_recency(papers)

        # 综合得分
        overall = (
            source_quality * 0.4 +
            evidence_quantity * 0.3 +
            recency * 0.3
        )

        return ConfidenceAssessment(
            overall=overall,
            source_quality=source_quality,
            evidence_quantity=evidence_quantity,
            recency=recency,
            conflicts=[],  # 冲突由专门的检测器处理
        )

    def _evaluate_source_quality(self, papers: list[Paper]) -> float:
        """评估来源质量"""
        if not papers:
            return 0.0

        # 按分级统计
        grade_weights = {
            3: 1.0,
            2: 0.6,
            1: 0.3,
            0: 0.1,
        }

        total_weight = 0.0
        for paper in papers:
            weight = grade_weights.get(paper.source_grade.value, 0.1)
            # 引用量也影响权重
            citation_factor = min(paper.citations / 200, 1.5)
            total_weight += weight * citation_factor

        # 归一化
        avg_weight = total_weight / len(papers)
        return min(avg_weight, 1.0)

    def _evaluate_evidence_quantity(
        self, paths: list[ResearchPath], papers: list[Paper]
    ) -> float:
        """评估证据数量"""
        if not paths:
            return 0.0

        # 统计每条路径的支持论文数量
        total_supporting = 0
        for path in paths:
            supporting = [
                pid for pid in path.supporting_papers
                if pid in {p.id for p in papers}
            ]
            total_supporting += len(supporting)

        # 每条路径至少需要2-3篇支持论文
        ideal = len(paths) * 3
        ratio = total_supporting / ideal if ideal > 0 else 0

        return min(ratio, 1.0)

    def _evaluate_recency(self, papers: list[Paper]) -> float:
        """评估时效性"""
        if not papers:
            return 0.0

        # 论文年龄越小，得分越高
        current_year = 2024
        max_age = 5  # 超过5年的论文价值递减

        total_recency = 0.0
        for paper in papers:
            age = current_year - paper.year
            if age <= 1:
                recency = 1.0
            elif age <= max_age:
                recency = 1.0 - (age - 1) / (max_age - 1) * 0.3
            else:
                recency = 0.7 - (age - max_age) * 0.1

            total_recency += max(recency, 0.1)

        return total_recency / len(papers)
