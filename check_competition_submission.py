import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join('instance', 'user_management.db')

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("检查competition_submission表结构：")
# 查询表结构
cursor.execute("PRAGMA table_info(competition_submission)")
columns = cursor.fetchall()

print("列名列表：")
for column in columns:
    print(f"- {column[1]} (类型: {column[2]})")

# 查询表中的数据（如果有）
print("\n表中的数据示例：")
cursor.execute("SELECT * FROM competition_submission LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭连接
conn.close()