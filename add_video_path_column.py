from app import app, db
import sqlite3
import os

# 添加缺少的video_path列到course表
if __name__ == '__main__':
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')
    
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查course表是否有video_path列
        cursor.execute("PRAGMA table_info(course)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Current columns in course table: {columns}")
        
        # 如果没有video_path列，添加它
        if 'video_path' not in columns:
            cursor.execute("ALTER TABLE course ADD COLUMN video_path TEXT")
            conn.commit()
            print("Successfully added video_path column to course table")
        else:
            print("video_path column already exists in course table")
            
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()