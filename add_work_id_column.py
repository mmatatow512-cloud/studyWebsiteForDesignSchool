import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join('instance', 'user_management.db')

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    # 添加work_id列
    cursor.execute("ALTER TABLE competition_submission ADD COLUMN work_id INTEGER")
    print("成功添加work_id列")
    
    # 提交更改
    conn.commit()
    
    # 验证列是否添加成功
    cursor.execute("PRAGMA table_info(competition_submission)")
    columns = cursor.fetchall()
    print("\n更新后的表结构：")
    for column in columns:
        print(f"- {column[1]} (类型: {column[2]})")
        
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("work_id列已经存在")
    else:
        print(f"添加列时出错: {e}")
finally:
    # 关闭连接
    conn.close()