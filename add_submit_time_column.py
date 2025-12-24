import sqlite3
import os

# 获取数据库路径
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')

# 连接到SQLite数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 添加缺失的submit_time列
try:
    cursor.execute("ALTER TABLE student_quiz ADD COLUMN submit_time DATETIME")
    conn.commit()
    print("Successfully added submit_time column to student_quiz table")
except sqlite3.OperationalError as e:
    print(f"Error adding column: {e}")

# 关闭连接
conn.close()
