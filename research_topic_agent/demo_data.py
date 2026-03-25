"""Mock学术文献数据库"""

from .models import Paper, VenueType, ResearchPath


MOCK_PAPERS = [
    Paper(
        id="p1",
        title="Dr. GPT: Large Language Models in Medical Diagnosis",
        authors=["Smith, J.", "Johnson, A.", "Williams, B."],
        abstract="We present Dr. GPT, a large language model specifically fine-tuned for medical diagnosis. "
                 "Our model achieves 92% accuracy on benchmark medical diagnosis datasets, outperforming "
                 "traditional ML methods. We demonstrate its effectiveness in preliminary diagnosis "
                 "support for primary care physicians.",
        venue="Nature Medicine",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2024,
        citations=245,
        keywords=["large language model", "medical diagnosis", "clinical decision support"],
        domain="medical AI",
    ),
    Paper(
        id="p2",
        title="Clinical BERT: Pre-trained Language Model for Electronic Health Records",
        authors=["Chen, L.", "Park, S.", "Kim, H."],
        abstract="Clinical BERT is designed to process electronic health records (EHR) and assist in "
                 "clinical decision making. Our study shows a 15% improvement in predicting patient "
                 "outcomes compared to baseline models.",
        venue="Journal of Medical Informatics",
        venue_type=VenueType.JOURNAL,
        year=2023,
        citations=189,
        keywords=["BERT", "EHR", "clinical decision support"],
        domain="medical AI",
    ),
    Paper(
        id="p3",
        title="LLM-based Triage System for Emergency Departments",
        authors=["Brown, R.", "Davis, M.", "Miller, K."],
        abstract="We propose an LLM-based triage system that prioritizes emergency department patients "
                 "based on symptom severity. The system reduced wait times by 23% in simulation.",
        venue="AAAI 2024",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2024,
        citations=87,
        keywords=["triage", "emergency", "LLM", "healthcare"],
        domain="medical AI",
    ),
    Paper(
        id="p4",
        title="Challenges of LLM in Medical Settings: A Case Study",
        authors=["Garcia, E.", "Martinez, R."],
        abstract="This paper identifies critical challenges when deploying LLMs in real medical settings, "
                 "including hallucinations, domain shift, and regulatory compliance issues. We propose "
                 "a human-in-the-loop framework to mitigate these risks.",
        venue="CHIL 2024",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2024,
        citations=156,
        keywords=["challenges", "deployment", "safety", "human-in-the-loop"],
        domain="medical AI",
    ),
    Paper(
        id="p5",
        title="MedPrompt: Few-shot Learning for Medical Question Answering",
        authors=["Lee, S.", "Yang, Q.", "Wang, F."],
        abstract="MedPrompt uses chain-of-thought prompting to achieve state-of-the-art results on medical "
                 "QA tasks with only 5 examples. We demonstrate generalization to unseen medical "
                 "conditions.",
        venue="NeurIPS 2023",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2023,
        citations=312,
        keywords=["prompting", "few-shot", "medical QA"],
        domain="medical AI",
    ),
    Paper(
        id="p6",
        title="Patient Privacy in LLM-based Medical Systems",
        authors=["Anderson, T.", "Taylor, J."],
        abstract="We analyze privacy risks when using LLMs for medical applications and propose "
                 "differential privacy mechanisms. Our approach achieves 95% utility while "
                 "guaranteeing k-anonymity.",
        venue="IEEE S&P",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2024,
        citations=134,
        keywords=["privacy", "differential privacy", "HIPAA"],
        domain="medical AI",
    ),
    Paper(
        id="p7",
        title="Survey: Large Language Models in Healthcare",
        authors=["Zhang, Y.", "Li, W.", "Huang, J."],
        abstract="This comprehensive survey covers 200+ papers on LLM applications in healthcare, "
                 "identifying key research trends and open challenges. We provide a taxonomy of "
                 "current approaches and future directions.",
        venue="arXiv preprint",
        venue_type=VenueType.PREPRINT,
        year=2024,
        citations=78,
        keywords=["survey", "healthcare", "taxonomy"],
        domain="medical AI",
    ),
    Paper(
        id="p8",
        title="GatorTron: A Large Clinical Language Model",
        authors=["Liu, X.", "Chen, Q.", "Emergency, R."],
        abstract="GatorTron is trained on 90B tokens of clinical text from Mayo Clinic. It achieves "
                 "excellent performance on clinical NLP benchmarks and is publicly available.",
        venue="Nature Biomedical Engineering",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2023,
        citations=423,
        keywords=["clinical LLM", " Mayo Clinic", "domain-specific"],
        domain="medical AI",
    ),
    Paper(
        id="p9",
        title="Limitations of LLMs in Understanding Medical Context",
        authors=["Robinson, P.", "Clark, D."],
        abstract="We demonstrate that current LLMs struggle with nuanced medical contexts, especially "
                 "for rare diseases with limited training data. This limitation poses significant "
                 "risks for diagnostic applications.",
        venue="Lancet Digital Health",
        venue_type=VenueType.JOURNAL,
        year=2024,
        citations=201,
        keywords=["limitations", "rare diseases", "context understanding"],
        domain="medical AI",
    ),
    Paper(
        id="p10",
        title="MedAI: Blog about LLM in Healthcare",
        authors=["BlogAuthor"],
        abstract="A blog post discussing the potential of LLMs in healthcare. Contains general "
                 "observations but lacks rigorous evaluation.",
        venue="MedAI Blog",
        venue_type=VenueType.BLOG,
        year=2024,
        citations=5,
        keywords=["LLM", "healthcare", "opinion"],
        domain="medical AI",
    ),
    Paper(
        id="p11",
        title="Multi-modal LLM for Medical Imaging Diagnosis",
        authors=["Kumar, S.", "Patel, N.", "Shah, A."],
        abstract="We propose a multi-modal LLM that combines text and medical images for improved "
                 "diagnosis accuracy. Our model achieves 96% accuracy on chest X-ray interpretation.",
        venue="CVPR 2024",
        venue_type=VenueType.TOP_CONFERENCE,
        year=2024,
        citations=167,
        keywords=["multi-modal", "medical imaging", "X-ray"],
        domain="medical AI",
    ),
    Paper(
        id="p12",
        title="Evaluating LLMs on Medical Licensing Exams",
        authors=["Turner, M.", "Harris, N.", "Young, R."],
        abstract="We evaluate GPT-4 and other LLMs on USMLE and other medical licensing exams. "
                 "Results show GPT-4 passes with 85% accuracy, but performance varies significantly "
                 "by medical specialty.",
        venue="NEJM AI",
        venue_type=VenueType.JOURNAL,
        year=2024,
        citations=289,
        keywords=["evaluation", "USMLE", "GPT-4", "medical exams"],
        domain="medical AI",
    ),
]

# 候选研究路径
MOCK_RESEARCH_PATHS = [
    ResearchPath(
        id="rp1",
        name="LLM辅助诊断系统",
        hypothesis="LLM可以作为初级诊断助手，提升医生诊断效率",
        methodology="设计提示工程框架，结合RAG检索最新医学指南",
        novelty="提出诊断置信度校准机制，降低误诊风险",
        feasibility=0.8,
        risk="需解决幻觉问题和隐私合规",
        supporting_papers=["p1", "p5", "p12"],
    ),
    ResearchPath(
        id="rp2",
        name="多模态医学影像诊断",
        hypothesis="结合视觉语言模型可提升影像诊断准确率",
        methodology="微调多模态大模型，融合影像和文本报告",
        novelty="端到端诊断，减少人工干预",
        feasibility=0.7,
        risk="高质量标注数据获取困难",
        supporting_papers=["p11"],
    ),
    ResearchPath(
        id="rp3",
        name="医患对话系统",
        hypothesis="LLM可用于患者初步问诊和分诊",
        methodology="构建医疗对话数据集，RLHF对齐医学专家偏好",
        novelty="首次在中文医疗场景下系统评估RLHF效果",
        feasibility=0.6,
        risk="安全性和伦理问题需严格论证",
        supporting_papers=["p3", "p4"],
    ),
    ResearchPath(
        id="rp4",
        name="隐私保护的医学NLP",
        hypothesis="差分隐私可确保LLM不泄露患者隐私",
        methodology="在GatorTron基础上引入DP-SGD训练",
        novelty="首次在临床NLP上实现严格隐私保证",
        feasibility=0.5,
        risk="隐私预算会降低模型效用",
        supporting_papers=["p6"],
    ),
]


def get_mock_papers() -> list[Paper]:
    """获取所有Mock论文"""
    return MOCK_PAPERS.copy()


def get_mock_paths() -> list[ResearchPath]:
    """获取所有Mock研究路径"""
    return MOCK_RESEARCH_PATHS.copy()
