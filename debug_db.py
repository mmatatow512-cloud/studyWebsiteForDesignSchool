from app import app, db, Message
from sqlalchemy import text
import datetime

with app.app_context():
    print("=== 数据库调试脚本 ===")
    
    # 1. 检查数据库连接
    print("\n1. 检查数据库连接")
    try:
        db.session.execute(text("SELECT 1"))
        print("✅ 数据库连接正常")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        exit(1)
    
    # 2. 直接保存消息
    print("\n2. 直接保存测试消息")
    try:
        # 保存问题
        question_msg = Message(
            sender_id=1,
            receiver_id=None,
            content="调试问题",
            session_id="debug-session-001",
            message_type="question",
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(question_msg)
        print("✅ 添加问题消息到会话")
        
        # 保存回答
        answer_msg = Message(
            sender_id=1,
            receiver_id=1,
            content="调试回答",
            session_id="debug-session-001",
            message_type="answer",
            created_at=datetime.datetime.utcnow()
        )
        db.session.add(answer_msg)
        print("✅ 添加回答消息到会话")
        
        # 提交到数据库
        db.session.commit()
        print("✅ 提交到数据库成功")
        
    except Exception as e:
        print(f"❌ 保存消息失败: {e}")
        db.session.rollback()
    
    # 3. 查询所有消息
    print("\n3. 查询所有消息")
    try:
        messages = Message.query.all()
        print(f"找到 {len(messages)} 条消息:")
        for msg in messages:
            print(f"  - id={msg.id}, sender_id={msg.sender_id}, type={msg.message_type}, session_id={msg.session_id}, content={msg.content}")
    except Exception as e:
        print(f"❌ 查询消息失败: {e}")
    
    print("\n=== 调试结束 ===")