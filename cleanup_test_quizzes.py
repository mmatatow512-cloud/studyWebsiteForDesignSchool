from app import app, db, Quiz, QuizQuestion, StudentQuiz

with app.app_context():
    print("=== 清理测试测验开始 ===")
    
    # 1. 查看清理前的测验数量
    before_count = Quiz.query.count()
    print(f"   清理前测验数量: {before_count}")
    
    # 2. 删除测试用的测验（标题包含"测试测验"的测验）
    test_quizzes = Quiz.query.filter(Quiz.title.like('测试测验%')).all()
    deleted_count = 0
    
    for quiz in test_quizzes:
        # 删除测验前先删除关联的学生测验记录
        StudentQuiz.query.filter_by(quiz_id=quiz.id).delete()
        # 删除测验前先删除关联的题目关系
        QuizQuestion.query.filter_by(quiz_id=quiz.id).delete()
        # 删除测验
        db.session.delete(quiz)
        deleted_count += 1
    
    db.session.commit()
    
    # 3. 查看清理后的测验数量
    after_count = Quiz.query.count()
    print(f"   清理后测验数量: {after_count}")
    print(f"   已删除测试测验: {deleted_count} 个")
    
    # 4. 验证剩余测验都有题目关联
    remaining_quizzes = Quiz.query.all()
    valid_quizzes = 0
    
    for quiz in remaining_quizzes:
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
        if len(quiz_questions) > 0:
            valid_quizzes += 1
    
    print(f"   剩余有效测验（有题目）: {valid_quizzes}")
    print(f"   剩余无效测验（无题目）: {after_count - valid_quizzes}")
    
    print("=== 清理测试测验结束 ===")