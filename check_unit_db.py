import sqlite3
import os

# 直接检查数据库中的unit表
if __name__ == '__main__':
    # 获取数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')
    
    try:
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询unit表中的所有记录
        cursor.execute("SELECT * FROM unit")
        units = cursor.fetchall()
        
        print("Unit records in database:")
        if units:
            # 获取列名
            cursor.execute("PRAGMA table_info(unit)")
            columns = [column[1] for column in cursor.fetchall()]
            print(f"Columns: {columns}")
            
            for unit in units:
                print(f"Unit: {dict(zip(columns, unit))}")
        else:
            print("No unit records found")
            
        # 关闭连接
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()