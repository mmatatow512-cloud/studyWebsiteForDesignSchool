#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试AI评分模块修复是否生效
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入AI评分模块
from AI_analysis.ai_grading import (
    generate_local_enhanced_result,
    generate_basic_result,
    generate_formatted_classified_suggestions
)

# 测试报告内容
content1 = "这是一个测试报告，关于Python编程的基础内容。Python是一种广泛使用的解释型、高级和通用的编程语言。它支持多种编程范式，包括结构化、函数式和面向对象编程。Python被设计为易于阅读和编写，具有简洁的语法。"

content2 = "数据分析是指用适当的统计分析方法对收集来的大量数据进行分析，提取有用信息和形成结论而对数据加以详细研究和概括总结的过程。这一过程也是质量管理体系的支持过程。在实用中，数据分析可帮助人们作出判断，以便采取适当行动。"

topic1 = "Python编程基础"
topic2 = "数据分析技术"

print("\n" + "="*50)
print("测试修复后的AI评分模块")
print("="*50 + "\n")

# 测试1: 相同内容多次生成建议，检查多样性
print("\n" + "-"*40)
print("测试1: 相同内容多次生成建议，检查多样性")
print("-"*40 + "\n")

for i in range(3):
    print(f"\n测试1.{i+1}: 生成建议 #{i+1}")
    suggestions = generate_formatted_classified_suggestions(content1, topic1)
    print("\n" + suggestions)
    print("\n" + "="*30)

# 测试2: 不同内容生成建议，检查针对性
print("\n" + "-"*40)
print("测试2: 不同内容生成建议，检查针对性")
print("-"*40 + "\n")

print("\n测试2.1: 关于Python编程的报告")
suggestions1 = generate_formatted_classified_suggestions(content1, topic1)
print("\n" + suggestions1)
print("\n" + "="*30)

print("\n测试2.2: 关于数据分析的报告")
suggestions2 = generate_formatted_classified_suggestions(content2, topic2)
print("\n" + suggestions2)
print("\n" + "="*30)

# 测试3: 测试增强本地结果生成
print("\n" + "-"*40)
print("测试3: 测试增强本地结果生成")
print("-"*40 + "\n")

result = generate_local_enhanced_result(content1, topic1)
print(f"\n总分: {result['total_score']}")
print(f"等级: {result['level']}")
print(f"生成方式: {result['generated_by']}")
print("\n建议列表:")
for i, suggestion in enumerate(result['suggestions'], 1):
    print(f"\n{i}. {suggestion}")
    print("-" * 20)

print("\n" + "="*50)
print("测试完成！")
print("="*50)
