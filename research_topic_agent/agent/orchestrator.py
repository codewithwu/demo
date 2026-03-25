"""Agent编排器 - 核心工作流编排"""

from typing import Optional

from .intent_parser import IntentParser
from .state import TopicStateManager
from ..models import (
    ResearchQuestion,
    Paper,
    ResearchPath,
    ConfidenceAssessment,
    ResearchTopic,
)
from ..retrieval.retriever import PaperRetriever
from ..analysis.surveyor import DirectionSurveyor
from ..analysis.comparator import PathComparator
from ..analysis.convergence import ConvergenceAnalyzer
from ..credibility.grader import SourceGrader
from ..credibility.conflict_detector import ConflictDetector
from ..demo_data import get_mock_paths


class TopicAgentOrchestrator:
    """科研选题Agent编排器"""

    def __init__(self):
        self._intent_parser = IntentParser()
        self._state_manager = TopicStateManager()
        self._retriever = PaperRetriever()
        self._surveyor = DirectionSurveyor()
        self._comparator = PathComparator()
        self._convergence_analyzer = ConvergenceAnalyzer()
        self._source_grader = SourceGrader()
        self._conflict_detector = ConflictDetector()

    @property
    def state_manager(self) -> TopicStateManager:
        return self._state_manager

    def run(self, user_input: str) -> ResearchTopic:
        """
        执行完整的选题流程

        Args:
            user_input: 用户输入，如"我想研究大语言模型在医疗诊断中的应用"

        Returns:
            最终的科研选题建议
        """
        print("\n" + "=" * 60)
        print("科研选题副驾 - 选题Agent")
        print("=" * 60)

        # Step 1: 意图解析
        print("\n[Step 1] 解析研究意图...")
        research_question = self._intent_parser.parse(user_input)
        self._state_manager.set_research_question(research_question)
        self._print_research_question(research_question)

        # 用户确认
        if not self._confirm_step("研究方向解析正确吗?"):
            raise ValueError("用户拒绝当前解析结果")

        # Step 2: 文献检索
        print("\n[Step 2] 检索相关文献...")
        papers = self._retriever.retrieve(research_question, limit=8)
        self._state_manager.set_retrieved_papers(papers)
        self._print_retrieved_papers(papers)

        # 用户确认
        if not self._confirm_step("检索结果是否相关?"):
            raise ValueError("用户对检索结果不满意")

        # Step 3: 方向调研
        print("\n[Step 3] 调研研究方向全景...")
        survey_result = self._surveyor.survey(papers, research_question)
        self._state_manager.set_survey_result(survey_result)
        self._print_survey_result(survey_result)

        # Step 4: 路径比较
        print("\n[Step 4] 比较候选研究路径...")
        candidate_paths = get_mock_paths()
        comparison_result = self._comparator.compare(
            candidate_paths, papers
        )
        self._state_manager.set_path_comparison(comparison_result)
        self._print_path_comparison(comparison_result)

        # 用户确认
        if not self._confirm_step("候选路径选择是否合适?"):
            raise ValueError("用户对候选路径不满意")

        # Step 5: 收敛判断
        print("\n[Step 5] 进行收敛判断...")
        confidence = self._convergence_analyzer.analyze(
            candidate_paths, papers
        )
        self._state_manager.set_convergence_result(
            {"confidence": confidence}
        )

        # 来源分级和冲突检测
        source_grades = self._source_grader.grade_papers(papers)
        conflicts = self._conflict_detector.detect(papers)

        # 综合评估
        final_confidence = self._merge_confidence_and_conflicts(
            confidence, conflicts
        )

        self._print_confidence_assessment(final_confidence)

        # 生成最终选题
        self._state_manager.set_final_topic(
            candidate_paths, final_confidence
        )

        # 最终确认
        print("\n" + "=" * 60)
        print("最终选题建议")
        print("=" * 60)
        final_topic = self._state_manager.state.final_topic
        self._print_final_topic(final_topic)

        confirmed = self._confirm_step("是否接受此选题建议?")
        self._state_manager.set_user_confirmed(confirmed)

        return final_topic

    def _confirm_step(self, prompt: str) -> bool:
        """请求用户确认"""
        print(f"\n>>> {prompt} (y/n): ", end="")
        response = input().strip().lower()
        return response in ("y", "yes", "是", "")

    def _print_research_question(
        self, rq: ResearchQuestion
    ) -> None:
        """打印研究问题"""
        print(f"  主题: {rq.topic}")
        if rq.scope:
            print(f"  范围: {rq.scope}")
        if rq.keywords:
            print(f"  关键词: {', '.join(rq.keywords)}")

    def _print_retrieved_papers(self, papers: list[Paper]) -> None:
        """打印检索结果"""
        print(f"  共检索到 {len(papers)} 篇论文:")
        for i, paper in enumerate(papers, 1):
            grade_star = "★" * paper.source_grade.value
            print(f"  {i}. [{grade_star}] {paper.title}")
            print(f"     {paper.venue}, {paper.year} | 引用: {paper.citations}")

    def _print_survey_result(self, result: dict) -> None:
        """打印调研结果"""
        print("  研究方向全景:")
        for topic, desc in result.get("research_topics", {}).items():
            print(f"    - {topic}: {desc}")

        print("\n  研究趋势:")
        for trend in result.get("trends", []):
            print(f"    * {trend}")

        print("\n  研究空白点:")
        for gap in result.get("gaps", []):
            print(f"    ! {gap}")

    def _print_path_comparison(self, result: dict) -> None:
        """打印路径比较结果"""
        paths = result.get("paths", [])
        print("  候选研究路径对比:")
        print(
            f"  {'路径':<20} {'可行性':<10} {'创新性':<10} {'风险':<15}"
        )
        print("  " + "-" * 60)
        for path in paths:
            print(
                f"  {path['name']:<20} "
                f"{path['feasibility']:<10.0%} "
                f"{path['novelty']:<10} "
                f"{path['risk']:<15}"
            )

    def _print_confidence_assessment(
        self, confidence: ConfidenceAssessment
    ) -> None:
        """打印置信度评估"""
        print("  置信度评估:")
        print(f"    综合置信度: {confidence.overall:.0%}")
        print(f"    来源质量: {confidence.source_quality:.0%}")
        print(f"    证据数量: {confidence.evidence_quantity:.0%}")
        print(f"    时效性: {confidence.recency:.0%}")

        if confidence.conflicts:
            print(f"\n  潜在冲突 ({len(confidence.conflicts)}):")
            for conflict in confidence.conflicts:
                print(f"    ! {conflict}")

    def _print_final_topic(self, topic: ResearchTopic) -> None:
        """打印最终选题"""
        print(f"\n  研究问题: {topic.research_question.topic}")
        print(f"  综合置信度: {topic.confidence.overall:.0%}")
        print("\n  推荐路径:")
        for i, path in enumerate(topic.research_paths[:3], 1):
            print(f"    {i}. {path.name} (可行性: {path.feasibility:.0%})")
            print(f"       假设: {path.hypothesis}")

        if topic.recommendations:
            print("\n  建议:")
            for rec in topic.recommendations:
                print(f"    * {rec}")

    def _merge_confidence_and_conflicts(
        self,
        confidence: ConfidenceAssessment,
        conflicts: list[str],
    ) -> ConfidenceAssessment:
        """合并置信度和冲突信息"""
        return ConfidenceAssessment(
            overall=confidence.overall,
            source_quality=confidence.source_quality,
            evidence_quantity=confidence.evidence_quantity,
            recency=confidence.recency,
            conflicts=conflicts,
        )
