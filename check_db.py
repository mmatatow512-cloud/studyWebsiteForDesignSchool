import sqlite3

conn = sqlite3.connect('user_management.db')
cursor = conn.cursor()

try:
    # 获取所有表
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cursor.fetchall()
    print('数据库中的表:', [table[0] for table in tables])
    
    # 检查student_quiz表
    if 'student_quiz' in [table[0] for table in tables]:
        print('\nstudent_quiz表的列:')
        cursor.execute('PRAGMA table_info(student_quiz)')
        columns = cursor.fetchall()
        for column in columns:
            print(f'  {column[1]} ({column[2]})')
    else:
        print('\nstudent_quiz表不存在')
        
    # 检查quiz表
    if 'quiz' in [table[0] for table in tables]:
        print('\nquiz表的列:')
        cursor.execute('PRAGMA table_info(quiz)')
        columns = cursor.fetchall()
        for column in columns:
            print(f'  {column[1]} ({column[2]})')
finally:
    conn.close()