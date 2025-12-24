import sqlite3
import os

# 连接到数据库
db_path = os.path.join('instance', 'user_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 获取所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print('数据库中的表:')
for table in tables:
    table_name = table[0]
    print(f'\n表名: {table_name}')
    
    # 获取表结构
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print('列信息:')
    for column in columns:
        print(f'  {column[1]} ({column[2]})')

# 关闭连接
conn.close()
