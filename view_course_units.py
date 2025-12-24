import sqlite3
import os

# 连接到数据库
db_path = os.path.join('instance', 'user_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('=== 查看课程表结构 ===')
cursor.execute("PRAGMA table_info(course)")
course_columns = cursor.fetchall()
for column in course_columns:
    print(f'  {column[1]} ({column[2]})')

print('\n=== 查看单元表结构 ===')
cursor.execute("PRAGMA table_info(unit)")
unit_columns = cursor.fetchall()
for column in unit_columns:
    print(f'  {column[1]} ({column[2]})')

print('\n=== 查看所有课程 ===')
cursor.execute("SELECT id, course_code, title FROM course")
courses = cursor.fetchall()
for course in courses:
    course_id, course_code, title = course
    print(f'\n课程ID: {course_id}, 代码: {course_code}, 标题: {title}')
    
    print('  课程单元:')
    cursor.execute("SELECT id, unit_title, file_path, order_index FROM unit WHERE course_id = ? ORDER BY order_index", (course_id,))
    units = cursor.fetchall()
    
    if not units:
        print('    本课程暂无教学单元')
    else:
        for unit in units:
            unit_id, unit_title, file_path, order_index = unit
            print(f'    单元ID: {unit_id}, 标题: {unit_title}, 文件: {file_path}, 顺序: {order_index}')

# 关闭连接
conn.close()
