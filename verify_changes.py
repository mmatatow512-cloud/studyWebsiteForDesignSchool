#!/usr/bin/env python3
# 验证所有修改的HTML文件中是否包含简单难度选项和返回主页按钮

import os

def check_file(file_path, checks):
    """检查文件是否包含指定内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results = {}
        for check_name, check_pattern in checks.items():
            results[check_name] = check_pattern in content
        
        return results
    except Exception as e:
        print(f"读取文件失败 {file_path}: {e}")
        return {check_name: False for check_name in checks}

def main():
    # 定义要检查的文件和内容
    files_to_check = [
        # 教师端AI测验相关页面
        {
            "path": "templates/teacher_html/teacher_create_quiz.html",
            "name": "教师端创建测验页面"
        },
        {
            "path": "templates/teacher_html/teacher_ai_test_management.html",
            "name": "教师端AI测验管理页面"
        },
        {
            "path": "templates/teacher_html/teacher_view_quiz.html",
            "name": "教师端查看测验页面"
        },
        # 学生端AI测验相关页面
        {
            "path": "templates/students_html/student_self_quiz.html",
            "name": "学生端自主测验页面"
        },
        {
            "path": "templates/students_html/student_ai_quizzes.html",
            "name": "学生端AI测验列表页面"
        },
        {
            "path": "templates/students_html/student_start_quiz.html",
            "name": "学生端开始测验页面"
        },
        {
            "path": "templates/students_html/student_quiz_result.html",
            "name": "学生端测验结果页面"
        },
        {
            "path": "templates/students_html/ai_test.html",
            "name": "学生端AI测验结果页面"
        }
    ]
    
    # 定义要检查的内容
    checks = {
        "简单难度选项": 'value="简单">简单<',
        "返回主页按钮": 'href="{{ url_for(\'dashboard\') }}"'
    }
    
    print("=== 验证修改结果 ===\n")
    
    for file_info in files_to_check:
        file_path = file_info["path"]
        file_name = file_info["name"]
        
        if not os.path.exists(file_path):
            print(f"❌ {file_name}: 文件不存在")
            continue
            
        results = check_file(file_path, checks)
        
        print(f"📄 {file_name}:")
        for check_name, found in results.items():
            status = "✅" if found else "❌"
            print(f"  {status} {check_name}")
        print()
    
    print("=== 验证完成 ===")

if __name__ == "__main__":
    main()
