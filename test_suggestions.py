import sys
import os

# 添加项目目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_analysis.ai_grading import generate_formatted_classified_suggestions

# 测试用的示例内容
content = "这是一篇关于人工智能的简单报告。人工智能是计算机科学的一个分支。它涉及创造能够模拟人类智能的机器。"
topic = "人工智能应用"

print("\n===== 测试 generate_formatted_classified_suggestions 函数 =====\n")

# 生成三次建议，检查多样性
for i in range(3):
    print(f"\n--- 第 {i+1} 次生成的建议 ---")
    suggestions = generate_formatted_classified_suggestions(content, topic)
    print(suggestions)
    print("\n" + "-"*50)

print("\n测试完成！")
