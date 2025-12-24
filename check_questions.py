from app import app, db, Question

with app.app_context():
    questions = Question.query.all()
    print(f"数据库中共有 {len(questions)} 个题目")
    
    # 统计不同知识点的题目数量
    knowledge_points_count = {}
    
    for question in questions:
        kp = question.knowledge_point
        if kp not in knowledge_points_count:
            knowledge_points_count[kp] = 0
        knowledge_points_count[kp] += 1
    
    print("\n知识点分布：")
    for kp, count in knowledge_points_count.items():
        print(f"{kp}: {count} 道题")
    
    # 打印前10道题的详细信息
    print("\n前10道题的详细信息：")
    for i, question in enumerate(questions[:10]):
        print(f"\n题目{i+1}:")
        print(f"  知识点: {question.knowledge_point}")
        print(f"  难度: {question.difficulty}")
        print(f"  题型: {question.qtype}")
        print(f"  内容: {question.content[:50]}...")