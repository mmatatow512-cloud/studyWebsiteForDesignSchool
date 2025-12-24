import sqlite3
import json

def verify_question_database():
    # 连接到当前运行应用的数据库
    db_path = '/Users/sevenpeaches/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/8a21a9d88389e8eee826eb065e9ceeae/Message/MessageTemp/58896f95cc0d5807e3d0bb18fac61435/File/study_website_python1/instance/user_management.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("验证题目数据库...")
    
    # 1. 查询question表的记录总数
    cursor.execute("SELECT COUNT(*) FROM question;")
    total_questions = cursor.fetchone()[0]
    print(f"1. 题目总数: {total_questions}")
    
    # 2. 查询题型分布
    cursor.execute("SELECT qtype, COUNT(*) FROM question GROUP BY qtype;")
    qtype_stats = cursor.fetchall()
    print("2. 题型分布:")
    for qtype, count in qtype_stats:
        print(f"   - {qtype}: {count}道")
    
    # 3. 随机抽取5道题，检查选项JSON格式和其他字段
    cursor.execute("SELECT id, qid, knowledge_point, difficulty, qtype, content, options, answer FROM question ORDER BY RANDOM() LIMIT 5;")
    sample_questions = cursor.fetchall()
    print("3. 随机抽取5道题检查格式:")
    for i, (id, qid, knowledge_point, difficulty, qtype, content, options, answer) in enumerate(sample_questions, 1):
        print(f"\n   第{i}道题:")
        print(f"   ID: {id}")
        print(f"   QID: {qid}")
        print(f"   知识点: {knowledge_point}")
        print(f"   难度: {difficulty}")
        print(f"   题型: {qtype}")
        print(f"   题干: {content[:50]}...")
        print(f"   答案: {answer}")
        
        # 检查选项JSON格式
        try:
            options_dict = json.loads(options)
            print(f"   选项: 共{len(options_dict)}个选项，格式正确")
            for key, value in options_dict.items():
                print(f"     {key}: {value[:30]}...")
        except json.JSONDecodeError as e:
            print(f"   选项JSON格式错误: {e}")
    
    # 4. 检查是否有重复的qid
    cursor.execute("SELECT qid, COUNT(*) FROM question GROUP BY qid HAVING COUNT(*) > 1;")
    duplicate_qids = cursor.fetchall()
    if duplicate_qids:
        print(f"\n4. 发现重复的QID: {len(duplicate_qids)}个")
        for qid, count in duplicate_qids:
            print(f"   - {qid}: 出现{count}次")
    else:
        print("\n4. 没有发现重复的QID")
    
    conn.close()
    
    # 总结
    print(f"\n总结:")
    if total_questions == 240:
        print("✓ 题目总数正确: 240道")
    else:
        print(f"✗ 题目总数不正确: 期望240道，实际{total_questions}道")
    
    # 检查题型是否完整
    expected_qtypes = ['single', 'multiple', 'judge', 'short_answer']
    actual_qtypes = [qtype for qtype, _ in qtype_stats]
    for qtype in expected_qtypes:
        if qtype in actual_qtypes:
            print(f"✓ 题型{qtype}存在")
        else:
            print(f"✗ 题型{qtype}缺失")

if __name__ == "__main__":
    verify_question_database()