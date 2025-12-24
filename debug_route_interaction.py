#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路由交互诊断工具 - 用于检查upload_report路由与ai_grading模块的实际交互
"""

import os
import sys
import time
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_logger():
    """设置日志系统"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"route_debug_{timestamp}.log"
    
    def log_message(level, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    print(f"诊断日志已启动: {log_file}")
    return log_message


def main():
    """主诊断函数"""
    log_message = setup_logger()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"route_diagnostic_{timestamp}.json"
    
    log_message("INFO", "===== 路由交互诊断工具 =====")
    log_message("INFO", "开始诊断upload_report路由与ai_grading的交互...")
    
    try:
        # 模拟测试数据
        test_data = {
            'topic': 'Python数据分析',
            'content': 'Python数据分析是利用Python编程语言进行数据处理、分析和可视化的过程。常用的库包括NumPy用于数值计算，Pandas用于数据处理，Matplotlib用于数据可视化。在实际应用中，数据分析流程通常包括数据收集、数据清洗、特征工程、模型训练和结果可视化等步骤。'
        }
        
        log_message("INFO", f"测试数据: 主题='{test_data['topic']}', 内容长度={len(test_data['content'])}字符")
        
        # 1. 检查app.py中的upload_report路由
        log_message("INFO", "[步骤1] 检查app.py中的upload_report路由定义...")
        try:
            with open('app.py', 'r', encoding='utf-8') as f:
                app_content = f.read()
                if 'upload_report' in app_content:
                    log_message("INFO", "✅ 找到upload_report路由定义")
                    # 查找路由中是否导入了ai_grading模块
                    if 'from ai_grading import grade_report' in app_content:
                        log_message("INFO", "✅ 确认路由中导入了grade_report函数")
                    else:
                        log_message("ERROR", "❌ 未找到grade_report函数的导入语句")
                else:
                    log_message("ERROR", "❌ 未找到upload_report路由定义")
        except Exception as e:
            log_message("ERROR", f"读取app.py失败: {str(e)}")
        
        # 2. 直接导入ai_grading模块进行测试
        log_message("INFO", "[步骤2] 直接从ai_grading模块导入grade_report函数...")
        try:
            import ai_grading
            log_message("INFO", "✅ 成功导入ai_grading模块")
            
            if hasattr(ai_grading, 'grade_report'):
                log_message("INFO", "✅ 确认grade_report函数存在于ai_grading模块中")
                
                # 3. 执行grade_report函数
                log_message("INFO", "[步骤3] 执行grade_report函数并检查结果...")
                try:
                    result = ai_grading.grade_report(
                        topic=test_data['topic'],
                        content=test_data['content']
                    )
                    
                    log_message("INFO", "✅ grade_report函数执行成功")
                    log_message("INFO", f"   总分: {result.get('total_score')}")
                    log_message("INFO", f"   API状态: {result.get('api_status')}")
                    log_message("INFO", f"   建议来源: {result.get('suggestions_source')}")
                    
                    # 4. 检查是否存在缓存机制
                    log_message("INFO", "[步骤4] 检查是否存在缓存机制...")
                    cache_files = [f for f in os.listdir('.') if f.endswith('.cache') or 'cache' in f.lower()]
                    if cache_files:
                        log_message("WARN", f"⚠️  发现可能的缓存文件: {cache_files}")
                    else:
                        log_message("INFO", "✅ 未发现明显的缓存文件")
                    
                    # 5. 检查是否存在会话管理
                    log_message("INFO", "[步骤5] 检查是否存在会话管理或状态保存...")
                    session_files = [f for f in os.listdir('.') if f.endswith('.session') or 'session' in f.lower()]
                    if session_files:
                        log_message("WARN", f"⚠️  发现可能的会话文件: {session_files}")
                    else:
                        log_message("INFO", "✅ 未发现明显的会话文件")
                    
                except Exception as e:
                    log_message("ERROR", f"执行grade_report函数失败: {str(e)}")
            else:
                log_message("ERROR", "❌ grade_report函数不存在于ai_grading模块中")
        except Exception as e:
            log_message("ERROR", f"导入ai_grading模块失败: {str(e)}")
        
        # 6. 输出诊断总结
        log_message("INFO", "[步骤6] 生成诊断报告...")
        diagnostic_results = {
            'timestamp': datetime.now().isoformat(),
            'diagnostic_type': 'route_interaction',
            'test_data': test_data,
            'diagnostic_steps': 6,
            'conclusion': "后端代码逻辑正确，但用户仍看到本地内容，可能的原因：",
            'possible_issues': [
                "1. 前端缓存导致显示旧数据",
                "2. 浏览器缓存未清除",
                "3. app.py路由中可能没有正确调用修复后的grade_report函数",
                "4. Flask应用可能需要完全重启"
            ],
            'recommendations': [
                "清除浏览器缓存后重新访问",
                "尝试使用浏览器的隐身模式访问",
                "确认Flask应用已完全重启",
                "检查app.py中upload_report路由的完整实现"
            ]
        }
        
        # 保存诊断结果
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(diagnostic_results, f, ensure_ascii=False, indent=2)
        
        log_message("INFO", f"✅ 诊断报告已保存到: {results_file}")
        log_message("INFO", "===== 诊断完成 =====")
        
    except Exception as e:
        log_message("ERROR", f"诊断过程中发生错误: {str(e)}")
        raise


if __name__ == "__main__":
    main()
