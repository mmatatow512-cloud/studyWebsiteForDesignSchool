# 测试grade_report函数调用阿里云百炼API的功能
import sys
import os

# 确保可以导入app模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import grade_report
import logging
import time

# 配置日志记录到文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("grade_report_test.log"),
        logging.StreamHandler()
    ]
)

def test_grade_report_function():
    """测试grade_report函数的功能"""
    try:
        logging.info("开始测试grade_report函数 - 阿里云百炼API集成")
        
        # 测试用例1：简单的报告内容
        file_content = "这是一份关于人工智能发展的测试报告。\n\n人工智能(AI)技术在近年来取得了显著进步，特别是在机器学习、深度学习和自然语言处理等领域。\n\n研究表明，AI技术正在各行各业中得到广泛应用，从医疗健康到金融服务，从智能制造到智能交通，AI都在发挥着越来越重要的作用。\n\n然而，AI技术的快速发展也带来了一系列挑战，如数据隐私、算法偏见、就业影响等问题，需要我们认真思考和应对。\n\n总的来说，AI技术的发展既带来了机遇，也带来了挑战，我们需要在推动技术创新的同时，确保其发展符合人类的长远利益。"
        topic = "人工智能发展"
        
        logging.info(f"测试用例1：主题 = '{topic}'")
        start_time = time.time()
        result = grade_report(file_content, topic)
        end_time = time.time()
        
        logging.info(f"测试用例1结果: {result}")
        logging.info(f"API调用耗时: {end_time - start_time:.2f}秒")
        
        # 验证返回结果格式
        assert isinstance(result, dict), "返回结果应该是字典类型"
        assert "score" in result, "返回结果缺少'score'字段"
        assert "grade" in result, "返回结果缺少'grade'字段"
        assert "analysis" in result, "返回结果缺少'analysis'字段"
        assert "suggestions" in result, "返回结果缺少'suggestions'字段"
        assert isinstance(result["suggestions"], list), "suggestions应该是列表类型"
        assert len(result["suggestions"]) >= 1, "suggestions列表至少应该有一个元素"
        
        # 打印结果的关键信息
        print("\n=== 测试用例1结果摘要 ===")
        print(f"评分: {result['score']}")
        print(f"等级: {result['grade']}")
        print(f"分析摘要: {result['analysis'][:100]}..." if len(result['analysis']) > 100 else f"分析: {result['analysis']}")
        print(f"建议数量: {len(result['suggestions'])}")
        for i, suggestion in enumerate(result['suggestions'], 1):
            print(f"建议{i}: {suggestion}")
        print("=============================\n")
        
        # 测试用例2：更具体的学术内容
        academic_content = "论数据驱动的城市规划方法创新\n\n摘要：随着城市化进程的加速和大数据技术的发展，传统的城市规划方法面临着前所未有的挑战与机遇。本文探讨了数据驱动的城市规划方法的理论基础、技术框架和实践应用，旨在为现代城市规划提供新的思路和方法。\n\n一、引言\n城市规划作为一门古老而又年轻的学科，在不同历史时期有着不同的理论基础和方法体系。进入21世纪，随着信息技术的飞速发展，特别是大数据、云计算、人工智能等技术的兴起，为城市规划提供了新的技术手段和方法支持。\n\n二、数据驱动城市规划的理论基础\n数据驱动的城市规划方法基于复杂系统理论、城市科学和数据科学等多学科理论，强调通过数据分析和挖掘来揭示城市系统的内在规律和运行机制。\n\n三、技术框架与方法\n本文提出了一个集成多源数据采集、数据处理与分析、模型构建与模拟、决策支持与可视化的技术框架，并详细阐述了各个环节的关键技术和方法。\n\n四、案例研究\n以某沿海城市的交通规划为例，展示了数据驱动方法在实际规划中的应用过程和效果，验证了该方法的可行性和有效性。\n\n五、结论与展望\n数据驱动的城市规划方法为城市规划提供了新的范式，但也面临着数据质量、隐私保护、技术整合等挑战。未来，需要进一步加强跨学科研究和实践探索，推动城市规划方法的不断创新和完善。"
        
        logging.info("测试用例2：学术报告内容")
        start_time = time.time()
        result2 = grade_report(academic_content, "数据驱动城市规划")
        end_time = time.time()
        
        logging.info(f"测试用例2结果: {result2}")
        logging.info(f"API调用耗时: {end_time - start_time:.2f}秒")
        
        # 打印结果的关键信息
        print("\n=== 测试用例2结果摘要 ===")
        print(f"评分: {result2['score']}")
        print(f"等级: {result2['grade']}")
        print(f"分析摘要: {result2['analysis'][:100]}..." if len(result2['analysis']) > 100 else f"分析: {result2['analysis']}")
        print(f"建议数量: {len(result2['suggestions'])}")
        for i, suggestion in enumerate(result2['suggestions'], 1):
            print(f"建议{i}: {suggestion}")
        print("=============================\n")
        
        logging.info("所有测试用例执行完成")
        print("\n测试完成！请查看grade_report_test.log日志了解详细情况。")
        print("系统现已成功集成阿里云百炼API进行报告分析。")
        
    except Exception as e:
        logging.error(f"测试过程中发生错误: {str(e)}")
        print(f"\n测试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_grade_report_function()
