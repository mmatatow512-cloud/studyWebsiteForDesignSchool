from app import app, db, Quiz, QuizQuestion

with app.app_context():
    # 检查所有测验
    quizzes = Quiz.query.all()
    print(f"数据库中共有 {len(quizzes)} 个测验记录")
    print("\n所有测验详细信息：")
    for quiz in quizzes:
        print(f"\n测验ID: {quiz.id}, 测验唯一标识: {quiz.quiz_id}")
        print(f"标题: {quiz.title}, 教师ID: {quiz.teacher_id}, 课程ID: {quiz.course_id}")
        print(f"知识点: {quiz.knowledge_points}, 难度: {quiz.difficulty}")
        
        # 检查测验关联的题目
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
        print(f"关联题目数量: {len(quiz_questions)}")
        for qq in quiz_questions:
            print(f"  题目ID: {qq.question_id}, 分数: {qq.score}")