from app import app, db, Quiz, QuizQuestion

with app.app_context():
    # 获取所有测验
    quizzes = Quiz.query.all()
    print(f"清理前数据库中共有 {len(quizzes)} 个测验记录")
    
    # 遍历所有测验，删除无效测验
    for quiz in quizzes:
        # 检查测验关联的题目数量
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
        
        # 删除条件：1. 没有关联题目 2. 非教师ID 1创建的测验（根据实际情况调整）
        if len(quiz_questions) == 0 or quiz.teacher_id != 1:
            print(f"\n删除测验ID: {quiz.id}")
            print(f"  原因: {'没有关联题目' if len(quiz_questions) == 0 else '非当前教师创建'}")
            print(f"  标题: {quiz.title}, 教师ID: {quiz.teacher_id}, 课程ID: {quiz.course_id}")
            
            # 删除测验关联的题目（如果有的话）
            for qq in quiz_questions:
                db.session.delete(qq)
            
            # 删除测验
            db.session.delete(quiz)
    
    # 提交更改
    db.session.commit()
    
    # 检查清理后的测验数量
    quizzes_after = Quiz.query.all()
    print(f"\n清理后数据库中共有 {len(quizzes_after)} 个测验记录")
    
    # 显示清理后的测验详细信息
    print("\n清理后的测验详细信息：")
    for quiz in quizzes_after:
        print(f"\n测验ID: {quiz.id}, 测验唯一标识: {quiz.quiz_id}")
        print(f"标题: {quiz.title}, 教师ID: {quiz.teacher_id}, 课程ID: {quiz.course_id}")
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
        print(f"关联题目数量: {len(quiz_questions)}")
