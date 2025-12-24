#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
模块路径验证工具 - 检查实际运行环境中使用的ai_grading模块路径
"""

import os
import sys
import time
from datetime import datetime

def main():
    """验证模块导入路径"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    print(f"===== 模块路径验证工具 ==== {timestamp}")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径: {sys.path}")
    
    print("\n[测试1] 尝试直接导入ai_grading...")
    try:
        import ai_grading
        print(f"✅ 成功导入ai_grading模块")
        print(f"模块路径: {ai_grading.__file__}")
        print(f"模块属性: {dir(ai_grading)}")
        if hasattr(ai_grading, 'grade_report'):
            print("✅ grade_report函数存在")
        else:
            print("❌ grade_report函数不存在")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    
    print("\n[测试2] 尝试导入AI_analysis.ai_grading...")
    try:
        from AI_analysis import ai_grading as ai_grading_module
        print(f"✅ 成功导入AI_analysis.ai_grading模块")
        print(f"模块路径: {ai_grading_module.__file__}")
        print(f"模块属性: {dir(ai_grading_module)}")
        if hasattr(ai_grading_module, 'grade_report'):
            print("✅ grade_report函数存在")
        else:
            print("❌ grade_report函数不存在")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
    
    print("\n[测试3] 检查app.py中的导入语句...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            app_content = f.read()
            import_lines = [line for line in app_content.split('\n') if 'import' in line and 'ai_grading' in line]
            print(f"找到的导入语句: {import_lines}")
    except Exception as e:
        print(f"❌ 读取app.py失败: {e}")
    
    print("\n[测试4] 检查__init__.py文件...")
    try:
        if os.path.exists('AI_analysis/__init__.py'):
            with open('AI_analysis/__init__.py', 'r', encoding='utf-8') as f:
                init_content = f.read()
                print(f"__init__.py内容:\n{init_content}")
        else:
            print("❌ AI_analysis/__init__.py不存在")
    except Exception as e:
        print(f"❌ 读取__init__.py失败: {e}")
    
    print("\n===== 验证完成 =====")


if __name__ == "__main__":
    main()
