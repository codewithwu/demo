"""冲突检测器 - 检测论文间的矛盾结论"""

from typing import TypedDict

from ..models import Paper


class Conflict(TypedDict):
    """冲突描述"""
    topic: str
    claim_a: str
    claim_b: str
    paper_a: str
    paper_b: str
    severity: str


class ConflictDetector:
    """冲突检测器"""

    # 冲突主题关键词映射
    CONFLICT_PATTERNS = {
        ("accuracy", "limitation"): "性能与局限性的矛盾",
        ("privacy", "high accuracy"): "隐私与性能的权衡",
        ("high", "challenges"): "高期望与现实挑战的矛盾",
        ("effective", "risks"): "有效性与风险的对立",
        ("novel", "limitations"): "创新性与局限性的张力",
    }

    # 已知的冲突对（用于Mock演示）
    KNOWN_CONFLICTS = [
        {
            "topic": "LLM诊断准确性",
            "claim_a": "Dr. GPT报告92%准确率",
            "claim_b": "LLMs难以处理 nuanced medical contexts",
            "paper_a": "p1",
            "paper_b": "p9",
            "severity": "medium",
        },
        {
            "topic": "隐私vs性能",
            "claim_a": "差分隐私可保证95%效用",
            "claim_b": "隐私保护会显著降低模型性能",
            "paper_a": "p6",
            "paper_b": "p6",
            "severity": "low",
        },
    ]

    def detect(self, papers: list[Paper]) -> list[str]:
        """
        检测论文间的潜在冲突

        Args:
            papers: 论文列表

        Returns:
            冲突描述列表
        """
        conflicts = []

        # 方法1: 检测已知冲突
        for conflict in self.KNOWN_CONFLICTS:
            paper_ids = {p.id for p in papers}
            if conflict["paper_a"] in paper_ids and conflict["paper_b"] in paper_ids:
                conflicts.append(
                    f"[{conflict['severity'].upper()}] {conflict['topic']}: "
                    f"{conflict['claim_a']} vs {conflict['claim_b']}"
                )

        # 方法2: 基于关键词的简单冲突检测
        title_keywords = [kw for p in papers for kw in p.title.lower().split()]

        # 检测"挑战/限制"与"高性能"并存
        has_challenges = any(
            "challenge" in p.title.lower() or "limitation" in p.title.lower()
            for p in papers
        )
        has_high_performance = any(
            "state-of-the-art" in p.title.lower() or
            "92%" in p.title or "96%" in p.title
            for p in papers
        )

        if has_challenges and has_high_performance:
            conflicts.append(
                "[INFO] 检索集中同时包含高性能报告和局限性研究，"
                "建议综合评估"
            )

        # 方法3: 检测极端引用差异
        sorted_by_citations = sorted(papers, key=lambda p: p.citations, reverse=True)
        if len(sorted_by_citations) >= 2:
            highest = sorted_by_citations[0]
            lowest = sorted_by_citations[-1]
            if highest.citations > lowest.citations * 10:
                conflicts.append(
                    f"[INFO] 论文引用量差异大: "
                    f"{highest.title[:30]}... ({highest.citations}次引用) vs "
                    f"{lowest.title[:30]}... ({lowest.citations}次引用)"
                )

        return conflicts

    def get_conflict_severity(self, conflicts: list[str]) -> str:
        """评估冲突严重程度"""
        if not conflicts:
            return "low"

        has_high = any("[HIGH]" in c or "[CRITICAL]" in c for c in conflicts)
        has_medium = any("[MEDIUM]" in c for c in conflicts)

        if has_high:
            return "high"
        elif has_medium:
            return "medium"
        else:
            return "low"
