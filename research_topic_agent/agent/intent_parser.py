"""意图解析器 - 将用户模糊想法转为结构化研究问题"""

import re
from typing import Optional

from ..models import ResearchQuestion


class IntentParser:
    """研究意图解析器"""

    def __init__(self):
        self._domain_keywords = {
            "medical": "medical AI",
            "医疗": "medical AI",
            "健康": "healthcare",
            "diagnosis": "medical diagnosis",
            "诊断": "medical diagnosis",
            "影像": "medical imaging",
            "imaging": "medical imaging",
            "药物": "drug discovery",
            "drug": "drug discovery",
        }

    def parse(self, user_input: str) -> ResearchQuestion:
        """
        解析用户输入，提取结构化研究问题

        Args:
            user_input: 用户原始输入，如"我想研究大语言模型在医疗诊断中的应用"

        Returns:
            结构化的研究问题
        """
        user_input = user_input.strip()

        # 提取主题
        topic = self._extract_topic(user_input)

        # 提取范围
        scope = self._extract_scope(user_input)

        # 提取关键词
        keywords = self._extract_keywords(user_input)

        # 提取约束条件
        constraints = self._extract_constraints(user_input)

        return ResearchQuestion(
            id="rq_001",
            raw_input=user_input,
            topic=topic,
            scope=scope,
            keywords=keywords,
            constraints=constraints,
        )

    def _extract_topic(self, text: str) -> str:
        """提取研究主题"""
        # 移除常见前缀
        text = re.sub(r"^(我想研究?|I want to research|我想做)?", "", text)

        # 移除后缀
        text = re.sub(r"的?(应用|研究|分析|探索)$", "", text)

        return text.strip()

    def _extract_scope(self, text: str) -> str:
        """提取研究范围/领域"""
        scope = ""

        if "诊断" in text or "diagnosis" in text.lower():
            scope = "medical diagnosis"
        elif "影像" in text or "imaging" in text.lower():
            scope = "medical imaging"
        elif "药物" in text or "drug" in text.lower():
            scope = "drug discovery"
        elif "对话" in text or "conversation" in text.lower():
            scope = "patient communication"

        return scope

    def _extract_keywords(self, text: str) -> list[str]:
        """提取关键词"""
        keywords = []

        # 大语言模型相关
        llm_terms = ["LLM", "大语言模型", "GPT", "language model", "transformer"]
        for term in llm_terms:
            if term.lower() in text.lower():
                keywords.append(term)

        # 医疗AI相关
        medical_terms = ["医疗", "medical", "healthcare", "clinical"]
        for term in medical_terms:
            if term.lower() in text.lower():
                keywords.append(term)

        # 技术方法
        tech_terms = ["RAG", "fine-tuning", "prompt", "multi-modal"]
        for term in tech_terms:
            if term.lower() in text.lower():
                keywords.append(term)

        return list(set(keywords))

    def _extract_constraints(self, text: str) -> list[str]:
        """提取约束条件"""
        constraints = []

        constraint_patterns = {
            r"需要.*隐私": "privacy",
            r"privacy": "privacy",
            r"中文": "Chinese language",
            r"英文": "English language",
            r"低成本": "low cost",
            r"快速": "fast",
        }

        for pattern, constraint in constraint_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                constraints.append(constraint)

        return constraints
