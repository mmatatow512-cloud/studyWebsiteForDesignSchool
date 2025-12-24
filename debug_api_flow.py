#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API调用流程诊断脚本
用于追踪从上传报告到AI评分的完整流程，识别为什么API结果未显示
"""

import sys
import os
import json
import time
import traceback
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置详细的日志记录
def setup_debug_logger():
    """设置详细的调试日志记录器"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"api_flow_debug_{timestamp}.log"
    
    class DebugLogger:
        def __init__(self, log_file):
            self.log_file = log_file
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"========== 调试日志开始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==========\n")
        
        def log(self, level, message, phase=None):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            phase_str = f"[{phase}] " if phase else ""
            log_entry = f"[{timestamp}] {phase_str}[{level}] {message}"
            print(log_entry)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
        
        def info(self, message, phase=None):
            self.log('INFO', message, phase)
        
        def debug(self, message, phase=None):
            self.log('DEBUG', message, phase)
        
        def error(self, message, phase=None):
            self.log('ERROR', message, phase)
        
        def warning(self, message, phase=None):
            self.log('WARNING', message, phase)
    
    return DebugLogger(log_file)

# 模拟upload_report路由中的处理逻辑
def simulate_upload_report_process():
    """模拟上传报告处理流程"""
    logger = setup_debug_logger()
    logger.info("开始模拟upload_report路由处理流程")
    
    try:
        # 1. 模拟上传的报告内容
        test_content = """
Python数据分析学习报告

Python在数据分析领域有着广泛的应用，主要使用的库包括NumPy、Pandas和Matplotlib等。
NumPy提供了高效的数值计算功能，支持多维数组操作。
Pandas基于NumPy构建，提供了数据结构如DataFrame，方便数据处理和分析。
Matplotlib用于创建各种可视化图表，帮助理解数据趋势。
数据清洗是数据分析的重要步骤，包括处理缺失值、异常值等。
数据可视化能够直观展示数据特征和分析结果。
        """
        
        test_topic = "Python数据分析"
        logger.info(f"测试报告主题: '{test_topic}'，内容长度: {len(test_content)}字符")
        
        # 2. 导入并检查ai_grading模块
        logger.info("导入ai_grading模块...", "模块导入")
        from AI_analysis import ai_grading
        logger.info(f"成功导入ai_grading模块，版本信息: {getattr(ai_grading, '__version__', 'unknown')}")
        
        # 3. 检查grade_report函数的实现
        logger.info("检查grade_report函数...", "函数检查")
        if hasattr(ai_grading, 'grade_report'):
            logger.info(f"grade_report函数已找到: {ai_grading.grade_report}")
        else:
            logger.error("未找到grade_report函数!")
            return False
        
        # 4. 检查是否有修改后的关键逻辑
        source_code = inspect.getsource(ai_grading.grade_report)
        if "优先使用API返回的结果" in source_code:
            logger.info("✅ 确认修复逻辑已包含在函数中")
        else:
            logger.warning("❓ 未在函数源码中找到预期的修复逻辑")
            logger.debug(f"函数源码片段: {source_code[:500]}...")
        
        # 5. 执行实际的评分过程
        logger.info("开始执行grade_report函数...", "评分执行")
        start_time = time.time()
        result = ai_grading.grade_report(test_content, test_topic)
        execution_time = time.time() - start_time
        logger.info(f"grade_report函数执行完成，耗时: {execution_time:.2f}秒", "评分执行")
        
        # 6. 详细分析结果
        logger.info("分析评分结果...", "结果分析")
        logger.info(f"总分: {result.get('total_score', 'N/A')}")
        logger.info(f"API状态: {result.get('api_status', 'N/A')}")
        logger.info(f"API错误: {result.get('api_error', 'N/A')}")
        logger.info(f"建议来源: {result.get('suggestions_source', 'N/A')}")
        
        # 分析建议内容
        suggestions = result.get('suggestions', [])
        logger.info(f"建议数量: {len(suggestions)}")
        for i, suggestion in enumerate(suggestions[:3], 1):
            logger.info(f"建议{i}: {suggestion}")
        
        # 7. 检查API调用是否真正成功
        if result.get('api_status') == 'success' and result.get('api_error') is None:
            logger.info("✅ API调用被标记为成功")
            
            # 检查API返回的建议是否真正被使用
            if result.get('suggestions_source') in ['original_api', 'enhanced_api']:
                logger.info("✅ 确认优先使用了API返回的结果")
            else:
                logger.warning(f"❌ 即使API调用成功，仍然使用了{suggestions_source}而不是API结果")
                
                # 深入检查可能的问题
                if 'suggestions' not in result:
                    logger.error("API没有返回suggestions字段")
                elif not result['suggestions']:
                    logger.warning("API返回了空的suggestions列表")
                else:
                    logger.debug(f"API返回的建议类型: {type(result['suggestions'])}")
                    logger.debug(f"API返回的建议前2个: {result['suggestions'][:2]}")
        else:
            logger.warning(f"⚠️ API调用可能未真正成功: status={result.get('api_status')}, error={result.get('api_error')}")
        
        # 8. 保存完整的诊断结果
        diagnostic_file = f"api_diagnostic_{timestamp}.json"
        with open(diagnostic_file, 'w', encoding='utf-8') as f:
            diagnostic_data = {
                'timestamp': datetime.now().isoformat(),
                'test_params': {
                    'content_length': len(test_content),
                    'topic': test_topic
                },
                'execution_info': {
                    'duration': execution_time,
                    'python_version': sys.version
                },
                'result_analysis': {
                    'api_status': result.get('api_status'),
                    'suggestions_source': result.get('suggestions_source'),
                    'suggestions_count': len(suggestions)
                },
                'full_result': result
            }
            json.dump(diagnostic_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"完整诊断结果已保存到: {diagnostic_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"诊断过程中发生错误: {str(e)}")
        logger.error(f"错误栈: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    # 需要导入inspect模块
    import inspect
    
    print("\n===== API调用流程诊断工具 =====\n")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 创建一个简单的HTML诊断报告模板
    html_report = f"""
<!DOCTYPE html>
<html>
<head>
    <title>API调用流程诊断报告 - {timestamp}</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 10px; border-radius: 5px; }}
        .section {{ margin: 20px 0; }}
        .success {{ color: green; }}
        .warning {{ color: orange; }}
        .error {{ color: red; }}
        pre {{ background: #f8f8f8; padding: 10px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>API调用流程诊断报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="section">
        <h2>诊断说明</h2>
        <p>此工具用于诊断为什么API调用后仍然显示本地生成的内容。运行后将生成详细的日志和JSON诊断文件。</p>
    </div>
    
    <div class="section">
        <h2>执行诊断</h2>
        <p>请在终端中查看诊断过程输出。诊断完成后，将在当前目录生成以下文件:</p>
        <ul>
            <li><code>api_flow_debug_{{timestamp}}.log</code> - 详细日志文件</li>
            <li><code>api_diagnostic_{{timestamp}}.json</code> - 诊断结果数据</li>
        </ul>
    </div>
</body>
</html>
"""
    
    # 保存HTML报告
    with open(f"api_diagnostic_report_{timestamp}.html", 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print("HTML诊断报告已生成: api_diagnostic_report_{timestamp}.html")
    print("\n开始执行诊断流程...\n")
    
    # 执行诊断
    success = simulate_upload_report_process()
    
    if success:
        print("\n✅ 诊断流程完成，请查看生成的日志文件获取详细信息")
    else:
        print("\n❌ 诊断流程失败")
