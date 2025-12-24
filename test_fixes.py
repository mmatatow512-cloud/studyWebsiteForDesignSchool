#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的功能：
1. 视频文件访问
2. StudentQuiz对象的quiz属性
"""

import requests
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试视频文件访问
def test_video_access():
    print("\n=== 测试视频文件访问 ===")
    # 测试DES002课程的视频文件
    video_url = "http://127.0.0.1:5001/course_files/DES002/unit_1_2ff1b400ce557d715052ab3286d37716.mp4"
    
    try:
        response = requests.get(video_url, stream=True)
        print(f"状态码: {response.status_code}")
        print(f"内容类型: {response.headers.get('Content-Type')}")
        print(f"内容长度: {response.headers.get('Content-Length')}")
        print(f"Accept-Ranges: {response.headers.get('Accept-Ranges')}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        # 验证Content-Type是否正确设置为video/mp4
        if response.headers.get('Content-Type') == 'video/mp4':
            print("✓ Content-Type正确设置为video/mp4")
        else:
            print("✗ Content-Type设置不正确")
        
        if response.status_code == 200:
            print("✓ 视频文件访问成功")
        else:
            print("✗ 视频文件访问失败")
    except Exception as e:
        print(f"✗ 视频文件访问异常: {str(e)}")

# 测试AI导师聊天API
def test_ai_tutor_chat_api():
    print("\n=== 测试AI导师聊天API ===")
    api_url = "http://127.0.0.1:5001/api/ai-tutor/chat?question=测试问题"
    
    try:
        response = requests.get(api_url, stream=True)
        print(f"状态码: {response.status_code}")
        print(f"内容类型: {response.headers.get('Content-Type')}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
        
        # 验证Content-Type是否正确设置为text/event-stream
        if response.headers.get('Content-Type') == 'text/event-stream':
            print("✓ Content-Type正确设置为text/event-stream")
        else:
            print("✗ Content-Type设置不正确")
        
        # 验证是否设置了CORS头
        if response.headers.get('Access-Control-Allow-Origin') == '*':
            print("✓ 正确设置了Access-Control-Allow-Origin头")
        else:
            print("✗ 未正确设置CORS头")
        
        if response.status_code == 200:
            print("✓ AI导师聊天API访问成功")
        else:
            print("✗ AI导师聊天API访问失败")
    except Exception as e:
        print(f"✗ AI导师聊天API访问异常: {str(e)}")

# 测试StudentQuiz对象的quiz属性
def test_student_quiz_quiz_attribute():
    print("\n=== 测试StudentQuiz对象的quiz属性 ===")
    
    try:
        # 导入必要的模块
        from app import db, StudentQuiz, Quiz
        from sqlalchemy import create_engine
        import tempfile
        import os
        
        # 创建一个临时数据库进行测试
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
            temp_db_path = temp_db.name
        
        # 创建数据库引擎
        engine = create_engine(f'sqlite:///{temp_db_path}')
        
        # 创建表结构
        db.metadata.create_all(engine)
        
        # 创建会话
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # 创建一个测试Quiz对象
        quiz = Quiz(
            title="测试测验",
            knowledge_points="数学",
            difficulty="简单",
            time_limit=30,
            anti_cheat=False
        )
        session.add(quiz)
        session.commit()
        
        # 创建一个测试StudentQuiz对象
        from datetime import datetime
        student_quiz = StudentQuiz(
            student_id=1,
            quiz_id=quiz.id,
            start_time=datetime.utcnow(),
            status="in_progress"
        )
        session.add(student_quiz)
        session.commit()
        
        # 测试quiz属性是否存在
        if hasattr(student_quiz, 'quiz'):
            print("✓ StudentQuiz对象有quiz属性")
            # 测试quiz属性是否能正常访问
            if student_quiz.quiz.id == quiz.id:
                print("✓ StudentQuiz.quiz能正常访问并返回正确的Quiz对象")
            else:
                print("✗ StudentQuiz.quiz返回的Quiz对象不正确")
        else:
            print("✗ StudentQuiz对象没有quiz属性")
        
        # 清理
        session.close()
        os.unlink(temp_db_path)
        
    except Exception as e:
        print(f"✗ 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("开始测试修复后的功能...")
    test_video_access()
    test_ai_tutor_chat_api()
    test_student_quiz_quiz_attribute()
    print("\n测试完成！")
