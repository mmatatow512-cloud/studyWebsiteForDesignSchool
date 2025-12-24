import sqlite3
import os
import sys

# 检查数据库文件路径
print('Python version:', sys.version)
print('Current directory:', os.getcwd())
print('Script path:', os.path.abspath(__file__))

# 使用绝对路径检查数据库
base_dir = os.path.dirname(os.path.abspath(__file__))
print('Base directory:', base_dir)

print('Database files:')
for db_file in ['user_management.db', 'instance/user_management.db']:
    full_path = os.path.join(base_dir, db_file)
    if os.path.exists(full_path):
        print(f'  {full_path}: {os.path.getsize(full_path)} bytes')
    else:
        print(f'  {full_path}: NOT FOUND')

# 连接到instance目录下的数据库
db_path = os.path.join(base_dir, 'instance/user_management.db')
print('\nTrying to connect to:', db_path)
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查数据库中所有表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print('\nDatabase tables:')
        for table in tables:
            print(f'  {table[0]}')
        
        # 检查unit表结构
        try:
            cursor.execute("PRAGMA table_info(unit)")
            print('\nUnit table structure:')
            columns = cursor.fetchall()
            if columns:
                for column in columns:
                    print(f'  {column[1]} ({column[2]})')
            else:
                print('  Unit table has no columns or does not exist')
        except Exception as e:
            print(f'  Error checking unit table structure: {e}')
        
        # 查询unit记录
        try:
            cursor.execute("SELECT id, file_path, unit_title FROM unit")
            units = cursor.fetchall()
            
            print('\nUnit records:')
            print('ID, File Path, Unit Title')
            if units:
                for unit in units:
                    print(f'{unit[0]}, {unit[1]}, {unit[2]}')
                    # 检查文件是否存在
                    file_path = unit[1]
                    full_path = os.path.join('course_files', file_path)
                    print(f'    File exists: {os.path.exists(full_path)}, Path: {full_path}')
            else:
                print('  No unit records found')
        except Exception as e:
            print(f'  Error querying unit records: {e}')
        
        conn.close()
    except Exception as e:
        print(f'Error connecting to database: {e}')
else:
    print(f'\nDatabase not found: {db_path}')
    print('Full path:', os.path.abspath(db_path))
