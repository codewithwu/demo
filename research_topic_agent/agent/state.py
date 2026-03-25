"""Agent状态管理"""

from ..models import (
    ResearchQuestion,
    Paper,
    ResearchPath,
    ResearchTopic,
    ConfidenceAssessment,
    TopicState,
)


class TopicStateManager:
    """选题流程状态管理器"""

    def __init__(self):
        self._state = TopicState()

    @property
    def state(self) -> TopicState:
        """获取当前状态"""
        return self._state

    def reset(self) -> None:
        """重置状态"""
        self._state = TopicState()

    def set_step(self, step: str) -> None:
        """设置当前步骤"""
        self._state.current_step = step

    def set_research_question(
        self, research_question: ResearchQuestion
    ) -> None:
        """设置研究问题"""
        self._state.research_question = research_question
        self._state.messages.append(
            f"[步骤1] 解析研究问题: {research_question.topic}"
        )

    def set_retrieved_papers(self, papers: list[Paper]) -> None:
        """设置检索到的论文"""
        self._state.retrieved_papers = papers
        self._state.messages.append(
            f"[步骤2] 检索到 {len(papers)} 篇相关论文"
        )

    def set_survey_result(self, result: dict) -> None:
        """设置调研结果"""
        self._state.survey_result = result
        self._state.messages.append("[步骤3] 完成研究方向调研")

    def set_path_comparison(self, result: dict) -> None:
        """设置路径比较结果"""
        self._state.path_comparison = result
        self._state.messages.append("[步骤4] 完成候选路径比较")

    def set_convergence_result(self, result: dict) -> None:
        """设置收敛结果"""
        self._state.convergence_result = result
        self._state.messages.append("[步骤5] 完成收敛判断")

    def set_final_topic(
        self,
        research_paths: list[ResearchPath],
        confidence: ConfidenceAssessment,
    ) -> None:
        """设置最终选题"""
        if not self._state.research_question:
            raise ValueError("research_question must be set first")

        self._state.final_topic = ResearchTopic(
            id="topic_001",
            research_question=self._state.research_question,
            research_paths=research_paths,
            evidence_chain=[],  # TODO: 实现证据链
            confidence=confidence,
            recommendations=self._generate_recommendations(
                research_paths, confidence
            ),
        )
        self._state.messages.append("[完成] 选题建议已生成")

    def _generate_recommendations(
        self, paths: list[ResearchPath], confidence: ConfidenceAssessment
    ) -> list[str]:
        """生成建议"""
        recommendations = []

        # 基于可行性排序
        sorted_paths = sorted(paths, key=lambda p: p.feasibility, reverse=True)

        if sorted_paths:
            best = sorted_paths[0]
            recommendations.append(
                f"推荐路径: {best.name} (可行性: {best.feasibility:.0%})"
            )

        if confidence.conflicts:
            recommendations.append(
                f"注意: 存在 {len(confidence.conflicts)} 个潜在冲突点需人工确认"
            )

        return recommendations

    def confirm_step(self, step_name: str) -> None:
        """用户确认某步骤"""
        self._state.messages.append(f"[确认] 用户确认: {step_name}")

    def set_user_confirmed(self, confirmed: bool) -> None:
        """设置用户最终确认"""
        self._state.user_confirmed = confirmed

    def add_message(self, message: str) -> None:
        """添加消息"""
        self._state.messages.append(message)

    def get_summary(self) -> dict:
        """获取状态摘要"""
        return {
            "current_step": self._state.current_step,
            "research_question": self._state.research_question.topic
            if self._state.research_question
            else None,
            "papers_retrieved": len(self._state.retrieved_papers),
            "paths_count": (
                len(self._state.path_comparison.get("paths", []))
                if self._state.path_comparison
                else 0
            ),
            "final_topic_ready": self._state.final_topic is not None,
            "user_confirmed": self._state.user_confirmed,
            "messages": self._state.messages,
        }
