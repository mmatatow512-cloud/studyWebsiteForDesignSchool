import sqlite3
import os

# 添加缺少的order_index列到unit表
if __name__ == '__main__':
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')
    
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查unit表是否有order_index列
        cursor.execute("PRAGMA table_info(unit)")
        columns = [column[1] for column in cursor.fetchall()]
        
        print(f"Current columns in unit table: {columns}")
        
        # 如果没有order_index列，添加它
        if 'order_index' not in columns:
            cursor.execute("ALTER TABLE unit ADD COLUMN order_index INTEGER DEFAULT 1")
            conn.commit()
            print("Successfully added order_index column to unit table")
        else:
            print("order_index column already exists in unit table")
            
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()