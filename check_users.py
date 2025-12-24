import sqlite3
import os

# 数据库路径
DB_PATH = os.path.join('instance', 'user_management.db')

# 连接到数据库
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("检查用户表中的数据：")
# 查询所有用户
cursor.execute("SELECT id, username, role, student_id FROM user")
users = cursor.fetchall()

print("用户列表：")
for user in users:
    print(f"- ID: {user[0]}, 用户名: {user[1]}, 角色: {user[2]}, 学号/工号: {user[3]}")

# 关闭连接
conn.close()