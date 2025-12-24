import sqlite3

def check_database_tables():
    # 连接到当前运行应用的数据库
    db_path = '/Users/sevenpeaches/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/8a21a9d88389e8eee826eb065e9ceeae/Message/MessageTemp/58896f95cc0d5807e3d0bb18fac61435/File/study_website_python1/user_management.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("检查数据库表结构...")
    
    # 查询所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("数据库中的表:")
    for table in tables:
        print(f"   - {table[0]}")
    
    # 检查是否存在question或questions表
    table_names = [table[0] for table in tables]
    if 'question' in table_names:
        print("\nquestion表存在")
        # 查询表结构
        cursor.execute("PRAGMA table_info(question);")
        columns = cursor.fetchall()
        print("question表的列:")
        for column in columns:
            print(f"   - {column[1]}: {column[2]}")
    elif 'questions' in table_names:
        print("\nquestions表存在")
        # 查询表结构
        cursor.execute("PRAGMA table_info(questions);")
        columns = cursor.fetchall()
        print("questions表的列:")
        for column in columns:
            print(f"   - {column[1]}: {column[2]}")
    else:
        print("\n数据库中不存在question或questions表")
    
    conn.close()

if __name__ == "__main__":
    check_database_tables()