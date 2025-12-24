import sqlite3

# 使用与app.py相同的数据库路径
db_path = r'd:\zkh\Desktop\demo1.4\demo 3.0 - 副本\demo 1.6\project\user_management.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE unit ADD COLUMN order_index INTEGER DEFAULT 1")
    conn.commit()
    print("成功添加order_index列到unit表")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("order_index列已存在")
    else:
        print(f"发生错误: {e}")
finally:
    conn.close()
