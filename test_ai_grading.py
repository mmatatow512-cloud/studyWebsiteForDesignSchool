#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AI批改功能测试脚本
用于验证修复后的AI批改功能输出是否具有差异性
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from AI_analysis.ai_grading import grade_report


def test_grading_diversity():
    """测试不同报告内容的评分和建议是否具有差异性"""
    print("=== AI批改功能差异性测试 ===")
    print()
    
    # 测试用例：不同类型的报告
    test_cases = [
        {
            "name": "技术报告",
            "content": """
随着人工智能技术的快速发展，机器学习算法在各个领域得到了广泛应用。
本报告主要介绍了深度学习中的神经网络原理及其在图像识别中的应用。
首先，我们讨论了卷积神经网络(CNN)的基本结构，包括卷积层、池化层和全连接层。
然后，分析了不同网络架构(如LeNet、AlexNet、ResNet)的优缺点。
最后，通过实验验证了ResNet在CIFAR-10数据集上的识别准确率达到了95%以上。
            """,
            "topic": "深度学习在图像识别中的应用"
        },
        {
            "name": "商业分析报告",
            "content": """
本报告对2023年中国电子商务市场进行了全面分析。
根据市场调研数据，2023年中国电商市场交易额达到了13.4万亿元，同比增长8.3%。
从用户结构来看，移动用户占比达到了92.1%，三线及以下城市用户增长迅速。
在竞争格局方面，阿里巴巴、京东和拼多多依然占据市场主导地位，但新兴平台如抖音电商发展势头强劲。
报告预测，未来电商市场将更加注重用户体验和供应链效率的提升。
            """,
            "topic": "2023年中国电子商务市场分析"
        },
        {
            "name": "学术研究报告",
            "content": """
本研究旨在探讨气候变化对全球农业生产的影响。
通过对1980-2020年间全球气温变化数据和主要农作物产量数据的相关性分析，
我们发现平均气温每升高1℃，小麦产量将下降约3.5%，水稻产量下降约2.3%。
此外，极端气候事件(如干旱、洪涝)的频率增加也对农业生产造成了显著影响。
本研究结果为制定应对气候变化的农业政策提供了科学依据。
            """,
            "topic": "气候变化对全球农业生产的影响研究"
        },
        {
            "name": "短报告",
            "content": """
今天天气很好，适合户外活动。我们去了公园，看到了很多花。
            """,
            "topic": "日常活动记录"
        }
    ]
    
    results = []
    
    # 对每个测试用例进行评分
    for i, case in enumerate(test_cases):
        print(f"处理测试用例 {i+1}/{len(test_cases)}: {case['name']}")
        print(f"主题: {case['topic']}")
        
        try:
            result = grade_report(case['content'], case['topic'])
            results.append((case['name'], result))
            
            print(f"总分: {result['total_score']}")
            print("各维度评分:")
            for dim in result['dimension_scores']:
                print(f"  - {dim['name']}: {dim['score']} (权重: {dim['weight']:.4f})")
            
            print("主要建议:")
            for j, sug in enumerate(result['suggestions'][:3]):  # 只显示前3条建议
                print(f"  {j+1}. {sug[:100]}...")
            
            print(f"生成方式: {result.get('generated_by', 'unknown')}")
            print(f"API状态: {result.get('api_status', 'unknown')}")
            print()
            
        except Exception as e:
            print(f"测试失败: {str(e)}")
            print()
    
    # 分析结果差异
    print("=== 结果差异分析 ===")
    
    # 比较总分差异
    total_scores = [r[1]['total_score'] for r in results]
    print(f"总分范围: {min(total_scores):.2f} - {max(total_scores):.2f}")
    print(f"总分差异度: {max(total_scores) - min(total_scores):.2f}")
    print()
    
    # 比较建议数量差异
    suggestion_counts = [len(r[1]['suggestions']) for r in results]
    print(f"建议数量范围: {min(suggestion_counts)} - {max(suggestion_counts)}")
    
    # 比较权重差异
    print("\n各维度权重变化:")
    dimensions = ['主题相关性', '逻辑结构完整性', '知识点覆盖率', '语言规范性']
    for dim in dimensions:
        weights = []
        for r in results:
            for d in r[1]['dimension_scores']:
                if d['name'] == dim:
                    weights.append(d['weight'])
        if weights:
            print(f"  - {dim}: {min(weights):.4f} - {max(weights):.4f}")
    
    print()
    print("=== 测试总结 ===")
    if max(total_scores) - min(total_scores) > 10:  # 如果总分差异超过10分，认为有显著差异
        print("✅ 测试通过：不同报告的评分结果具有明显差异性")
    else:
        print("⚠️  注意：不同报告的评分结果差异较小，可能需要进一步优化")
    
    if max(suggestion_counts) - min(suggestion_counts) > 2:
        print("✅ 测试通过：不同报告的建议数量具有明显差异性")
    else:
        print("⚠️  注意：不同报告的建议数量差异较小")


if __name__ == "__main__":
    test_grading_diversity()
