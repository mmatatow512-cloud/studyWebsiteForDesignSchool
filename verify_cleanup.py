from app import app, db, Quiz, QuizQuestion, StudentQuiz

with app.app_context():
    print("=== 验证清理结果 ===")
    
    # 检查测验数量
    quiz_count = Quiz.query.count()
    print(f"1. 测验总数: {quiz_count}")
    
    # 检查测验题目关系数量
    quiz_question_count = QuizQuestion.query.count()
    print(f"2. 测验题目关系总数: {quiz_question_count}")
    
    # 检查学生测验记录数量
    student_quiz_count = StudentQuiz.query.count()
    print(f"3. 学生测验记录总数: {student_quiz_count}")
    
    # 检查是否还有标题包含"测试测验"的测验
    test_quiz_count = Quiz.query.filter(Quiz.title.like('测试测验%')).count()
    print(f"4. 测试测验数量: {test_quiz_count}")
    
    if quiz_count == 0 and quiz_question_count == 0 and test_quiz_count == 0:
        print("\n✅ 清理成功！数据库已清理干净")
    else:
        print("\n⚠️  清理不彻底，仍有残留数据")
    
    print("\n=== 验证结束 ===")