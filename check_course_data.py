import sqlite3
import os

# 连接到数据库
conn = sqlite3.connect('instance/user_management.db')
cursor = conn.cursor()

# 检查course表结构
cursor.execute('PRAGMA table_info(course)')
print('Course table structure:')
for col in cursor.fetchall():
    print(f'  {col[1]} ({col[2]})')

# 查询course记录
cursor.execute('SELECT id, course_code, title, description FROM course')
print('\nCourse records:')
print('ID, Course Code, Title, Description')
for course in cursor.fetchall():
    print(f'{course[0]}, {course[1]}, {course[2]}, {course[3]}')

# 关闭连接
conn.close()