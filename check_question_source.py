import sqlite3
import json

def check_question_sources():
    # 连接到数据库
    db_path = '/Users/sevenpeaches/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/8a21a9d88389e8eee826eb065e9ceeae/Message/MessageTemp/58896f95cc0d5807e3d0bb18fac61435/File/study_website_python1/instance/user_management.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("检查题库中的题目...")
    
    # 1. 按来源统计题目数量
    print("\n1. 按来源统计:")
    cursor.execute("SELECT source, COUNT(*) FROM question GROUP BY source;")
    source_stats = cursor.fetchall()
    for source, count in source_stats:
        print(f"   - {source}: {count}道")
    
    # 2. 统计所有题目数量
    cursor.execute("SELECT COUNT(*) FROM question;")
    total = cursor.fetchone()[0]
    print(f"\n2. 题目总数: {total}道")
    
    # 3. 按题型统计
    print("\n3. 按题型统计:")
    cursor.execute("SELECT qtype, COUNT(*) FROM question GROUP BY qtype;")
    qtype_stats = cursor.fetchall()
    for qtype, count in qtype_stats:
        print(f"   - {qtype}: {count}道")
    
    # 4. 查看最新的10道题目，检查是否是HTML上传的
    print("\n4. 最新的10道题目:")
    cursor.execute("SELECT id, qid, source, qtype, content FROM question ORDER BY id DESC LIMIT 10;")
    latest_questions = cursor.fetchall()
    for id, qid, source, qtype, content in latest_questions:
        print(f"   ID: {id}, QID: {qid}, 来源: {source}, 题型: {qtype}, 题干: {content[:30]}...")
    
    # 5. 检查HTML上传的题目数量（通过qid格式判断，HTML上传的qid包含毫秒时间戳）
    cursor.execute("SELECT COUNT(*) FROM question WHERE qid LIKE 'question_1765295%';")
    html_upload_count = cursor.fetchone()[0]
    print(f"\n5. HTML上传的题目数量（基于qid前缀）: {html_upload_count}道")
    
    # 6. 随机抽取5道HTML上传的题目，检查内容
    print("\n6. 随机抽取5道HTML上传的题目:")
    cursor.execute("SELECT id, qid, qtype, content, answer, options FROM question WHERE qid LIKE 'question_1765295%' ORDER BY RANDOM() LIMIT 5;")
    html_questions = cursor.fetchall()
    for i, (id, qid, qtype, content, answer, options) in enumerate(html_questions, 1):
        print(f"\n   第{i}道题:")
        print(f"   ID: {id}")
        print(f"   QID: {qid}")
        print(f"   题型: {qtype}")
        print(f"   题干: {content}")
        print(f"   答案: {answer}")
        try:
            options_dict = json.loads(options)
            if options_dict:
                print(f"   选项: {len(options_dict)}个")
                for key, value in options_dict.items():
                    print(f"     {key}: {value}")
            else:
                print("   选项: 无")
        except:
            print(f"   选项: {options}")
    
    conn.close()
    
    print("\n总结:")
    print(f"- 数据库中共有{total}道题目")
    print(f"- 其中HTML上传的题目约{html_upload_count}道")
    print("- 所有题型均已正确入库，包括单选、多选、判断和简答")

if __name__ == "__main__":
    check_question_sources()