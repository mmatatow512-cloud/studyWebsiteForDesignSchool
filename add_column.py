import sqlite3

conn = sqlite3.connect('user_management.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE student_quiz ADD COLUMN submit_time DATETIME")
    conn.commit()
    print("成功添加submit_time列")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("submit_time列已存在")
    else:
        print(f"发生错误: {e}")
finally:
    conn.close()