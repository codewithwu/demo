"""路径比较器 - 对比候选研究路径的优劣"""

from typing import TypedDict

from ..models import ResearchPath, Paper


class PathComparisonResult(TypedDict):
    """路径比较结果"""
    paths: list[dict]
    comparison_matrix: dict
    recommendation: str


class PathComparator:
    """研究路径比较器"""

    def compare(
        self, paths: list[ResearchPath], papers: list[Paper]
    ) -> PathComparisonResult:
        """
        比较候选研究路径

        Args:
            paths: 候选研究路径列表
            papers: 相关论文列表

        Returns:
            比较结果
        """
        # 构建路径对比表
        path_comparisons = []
        for path in paths:
            # 计算证据强度
            evidence_strength = self._calculate_evidence_strength(
                path, papers
            )

            # 评估创新性
            novelty = self._assess_novelty(path, papers)

            path_comparisons.append({
                "id": path.id,
                "name": path.name,
                "feasibility": path.feasibility,
                "novelty": novelty,
                "risk": path.risk or "中等",
                "evidence_strength": evidence_strength,
                "supporting_count": len(path.supporting_papers),
            })

        # 构建比较矩阵
        comparison_matrix = self._build_comparison_matrix(path_comparisons)

        # 生成推荐
        recommendation = self._generate_recommendation(path_comparisons)

        return PathComparisonResult(
            paths=path_comparisons,
            comparison_matrix=comparison_matrix,
            recommendation=recommendation,
        )

    def _calculate_evidence_strength(
        self, path: ResearchPath, papers: list[Paper]
    ) -> float:
        """计算路径的证据强度"""
        if not path.supporting_papers:
            return 0.3

        # 获取支持论文
        supporting = {
            p.id: p for p in papers if p.id in path.supporting_papers
        }

        if not supporting:
            return 0.3

        # 基于来源分级和引用计算证据强度
        total_evidence = 0.0
        for paper in supporting.values():
            # 来源分级 * 引用权重
            source_weight = {
                3: 1.0,
                2: 0.6,
                1: 0.3,
                0: 0.1,
            }.get(paper.source_grade.value, 0.1)

            # 引用越多，证据越强（但有上限）
            citation_weight = min(paper.citations / 500, 1.0)
            total_evidence += source_weight * (0.5 + 0.5 * citation_weight)

        return min(total_evidence / len(path.supporting_papers), 1.0)

    def _assess_novelty(self, path: ResearchPath, papers: list[Paper]) -> str:
        """评估创新性"""
        # 检查是否有相关研究
        related_count = sum(
            1 for paper in papers
            if any(kw in paper.title.lower()
                   for kw in path.name.lower().split())
        )

        if related_count == 0:
            return "高"
        elif related_count <= 2:
            return "中"
        else:
            return "一般"

    def _build_comparison_matrix(
        self, paths: list[dict]
    ) -> dict:
        """构建多维度比较矩阵"""
        dimensions = ["feasibility", "novelty", "evidence_strength", "risk"]

        matrix = {}
        for dim in dimensions:
            if dim == "novelty":
                # 创新性需要特殊处理
                matrix[dim] = {
                    p["name"]: (
                        "高" if p[dim] == "高" else
                        "中" if p[dim] == "中" else "一般"
                    )
                    for p in paths
                }
            elif dim == "risk":
                matrix[dim] = {p["name"]: p[dim] for p in paths}
            else:
                matrix[dim] = {
                    p["name"]: f"{p[dim]:.0%}" for p in paths
                }

        return matrix

    def _generate_recommendation(
        self, paths: list[dict]
    ) -> str:
        """生成推荐"""
        if not paths:
            return "无足够候选路径"

        # 综合评分
        scored_paths = []
        for p in paths:
            score = (
                p["feasibility"] * 0.4 +
                p["evidence_strength"] * 0.4 +
                (1.0 if p["novelty"] == "高" else 0.5 if p["novelty"] == "中" else 0.2) * 0.2
            )
            scored_paths.append((p["name"], score))

        scored_paths.sort(key=lambda x: x[1], reverse=True)
        best_name, best_score = scored_paths[0]

        return f"推荐 '{best_name}'，综合得分 {best_score:.2f}"
