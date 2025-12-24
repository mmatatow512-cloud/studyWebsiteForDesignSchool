import sqlite3
import os

# 连接到数据库
conn = sqlite3.connect('instance/user_management.db')
cursor = conn.cursor()

# 查询unit表的所有记录
cursor.execute('SELECT * FROM unit')
unit_records = cursor.fetchall()

print('Unit records:')
if unit_records:
    for record in unit_records:
        print(f'ID: {record[0]}, Course ID: {record[1]}, Title: {record[2]}, File Path: {record[3]}')
else:
    print('No unit records found')

# 关闭连接
conn.close()