#!/usr/bin/env python3
"""科研选题副驾 - 选题Agent CLI入口"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.orchestrator import TopicAgentOrchestrator


def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    科研选题副驾子系统                          ║
║                    Research Topic Agent                      ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_usage():
    """打印使用说明"""
    usage = """
使用方法:
    1. 输入你的研究兴趣或初步想法
    2. 系统会引导你完成:
       - 研究问题解析
       - 相关文献检索
       - 研究方向调研
       - 候选路径比较
       - 收敛判断
    3. 每步需要你确认后才会继续
    4. 最终输出选题建议和置信度评估

示例输入:
    - "我想研究大语言模型在医疗诊断中的应用"
    - "RAG在学术文献检索中的使用"
    - "多模态模型在医学影像诊断中的现状"

退出: 输入 'quit' 或 'exit'
    """
    print(usage)


def main():
    """主函数"""
    print_banner()
    print_usage()

    orchestrator = TopicAgentOrchestrator()

    while True:
        try:
            print("\n" + "-" * 60)
            print("请输入您的研究兴趣或想法 (quit退出):")
            print("> ", end="")

            user_input = input().strip()

            if user_input.lower() in ("quit", "exit", "q"):
                print("\n感谢使用科研选题副驾系统!")
                break

            if not user_input:
                print("输入为空，请重新输入")
                continue

            # 执行选题流程
            result = orchestrator.run(user_input)

            # 打印结果摘要
            print("\n" + "=" * 60)
            print("选题流程完成!")
            print("=" * 60)

            if orchestrator.state_manager.state.user_confirmed:
                print("您已确认接受此选题建议")
            else:
                print("您尚未确认选题建议，可以调整后重试")

            # 打印状态摘要
            summary = orchestrator.state_manager.get_summary()
            print(f"\n流程摘要:")
            print(f"  - 步骤数: {summary['papers_retrieved']} 篇论文")
            print(f"  - 候选路径: {summary['paths_count']} 条")
            print(f"  - 选题建议: {'已就绪' if summary['final_topic_ready'] else '未就绪'}")

        except KeyboardInterrupt:
            print("\n\n操作已取消")
            break
        except ValueError as e:
            print(f"\n[错误] {e}")
            print("请调整输入后重试")
        except Exception as e:
            print(f"\n[系统错误] {e}")
            print("请联系开发者或重试")


if __name__ == "__main__":
    main()
