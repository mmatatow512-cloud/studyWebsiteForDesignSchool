#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
import os

# 检查当前应用目录下的数据库文件
current_dir = os.path.dirname(__file__)
db_files = [f for f in os.listdir(current_dir) if f.endswith('.db')]
print(f"当前目录下的数据库文件: {db_files}")

# 使用当前应用的数据库（应该是user_management.db）
db_path = os.path.join(current_dir, 'user_management.db')

# 连接到数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n验证当前应用的数据库：")
print("=" * 50)

# 1. 查询所有表名
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("1. 数据库中的所有表：")
for table in tables:
    print(f"   - {table[0]}")

# 2. 如果有question或questions表，查询其记录数
if any('question' in table[0].lower() for table in tables):
    # 尝试两种表名形式
    for table_name in ['question', 'questions']:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"\n2. {table_name}表的记录数：{count}")
            
            # 查询题型分布
            cursor.execute(f"SELECT qtype, COUNT(*) FROM {table_name} GROUP BY qtype;")
            qtype_stats = cursor.fetchall()
            print(f"3. {table_name}表的题型分布：")
            for qtype, qcount in qtype_stats:
                print(f"   - {qtype}: {qcount}条")
            
            # 随机抽取几道题检查选项JSON格式
            print(f"\n4. 随机检查5道题的选项格式：")
            cursor.execute(f"SELECT qid, content, qtype, options FROM {table_name} ORDER BY RANDOM() LIMIT 5;")
            sample_questions = cursor.fetchall()
            
            for qid, content, qtype, options in sample_questions:
                print(f"\n   题目ID: {qid}")
                print(f"   题型: {qtype}")
                print(f"   题干: {content[:50]}..." if len(content) > 50 else f"   题干: {content}")
                
                if qtype in ['single', 'multiple', 'judge']:
                    try:
                        options_dict = json.loads(options)
                        print(f"   选项: {json.dumps(options_dict, ensure_ascii=False)}")
                        print("   ✓ 选项JSON格式正确")
                    except json.JSONDecodeError as e:
                        print(f"   ✗ 选项JSON格式错误: {e}")
                        print(f"   原始选项内容: {options}")
                else:
                    print(f"   题型为{qtype}，无选项")
            
            break
        except sqlite3.OperationalError:
            continue
else:
    print("\n2. 数据库中没有找到question相关的表")

# 关闭数据库连接
conn.close()

print("\n" + "=" * 50)
print("验证完成！")
