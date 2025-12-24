import sqlite3
import os

# 连接数据库
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== 数据库表信息 ===")
try:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"数据库中共有 {len(tables)} 个表")
    for table in tables:
        print(f"表名: {table[0]}")
except Exception as e:
    print(f"查询表信息时出错: {e}")

print("\n=== 课程信息 ===")
try:
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    print(f"共有 {len(courses)} 门课程")
    for course in courses:
        print(f"课程ID: {course[0]}, 代码: {course[1]}, 标题: {course[2]}, 老师ID: {course[3]}")
except Exception as e:
    print(f"查询课程表时出错: {e}")

print("\n=== 学生选课信息 ===")
try:
    # 检查是否存在student_course表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='student_course';")
    if cursor.fetchone():
        cursor.execute("SELECT * FROM student_course")
        enrollments = cursor.fetchall()
        print(f"共有 {len(enrollments)} 条选课记录")
        for enrollment in enrollments:
            print(f"ID: {enrollment[0]}, 学生ID: {enrollment[1]}, 课程ID: {enrollment[2]}")
    else:
        print("student_course表不存在")
except Exception as e:
    print(f"查询选课表时出错: {e}")

# 检查用户ID为2的学生是否有选课记录
print("\n=== 学生ID为2的选课记录 ===")
try:
    cursor.execute("SELECT * FROM student_course WHERE student_id = 2")
    student2_courses = cursor.fetchall()
    print(f"学生ID为2共有 {len(student2_courses)} 条选课记录")
    for enrollment in student2_courses:
        print(f"ID: {enrollment[0]}, 学生ID: {enrollment[1]}, 课程ID: {enrollment[2]}")
except Exception as e:
    print(f"查询学生ID为2的选课记录时出错: {e}")

# 检查course表的结构
print("\n=== course表结构 ===")
try:
    cursor.execute("PRAGMA table_info(course)")
    columns = cursor.fetchall()
    print("字段名称, 数据类型, 是否主键, 默认值")
    for column in columns:
        print(f"{column[1]}, {column[2]}, {column[5] == 1}, {column[4]}")
except Exception as e:
    print(f"查询course表结构时出错: {e}")

conn.close()
