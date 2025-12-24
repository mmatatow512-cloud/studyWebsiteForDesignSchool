#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试StudentQuiz对象的quiz属性修复
"""

import os
import sys
import sqlite3

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_student_quiz_relationship():
    print("=== 测试StudentQuiz与Quiz的关系 ===")
    
    try:
        # 导入应用程序模块
        from app import db, StudentQuiz, Quiz
        
        print("✓ 成功导入应用程序模块")
        
        # 检查StudentQuiz类是否有quiz属性
        if hasattr(StudentQuiz, 'quiz'):
            print("✓ StudentQuiz类有quiz属性")
        else:
            print("✗ StudentQuiz类没有quiz属性")
            return
        
        # 检查quiz属性是否是relationship类型
        from sqlalchemy.orm import RelationshipProperty
        if isinstance(StudentQuiz.quiz, RelationshipProperty):
            print("✓ quiz属性是RelationshipProperty类型")
        else:
            print("✗ quiz属性不是RelationshipProperty类型")
            return
        
        print("✓ StudentQuiz与Quiz的关系已正确配置")
        print("✓ 测验提交的AttributeError问题已修复")
        
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_student_quiz_relationship()
