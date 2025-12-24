from app import app, db, Quiz, QuizQuestion, Question, StudentQuiz, User

with app.app_context():
    # 检查所有测验
    quizzes = Quiz.query.all()
    print(f"共有 {len(quizzes)} 个测验")
    for quiz in quizzes:
        print(f"测验 {quiz.id}: {quiz.title}, 课程ID: {quiz.course_id}")
        # 检查每个测验的题目
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
        print(f"  关联题目数: {len(quiz_questions)}")
        for qq in quiz_questions:
            question = Question.query.get(qq.question_id)
            if question:
                print(f"    题目 {qq.question_id}: {question.content[:20]}...")
            else:
                print(f"    题目 {qq.question_id}: 不存在")
    
    # 检查所有题目
    questions = Question.query.all()
    print(f"\n共有 {len(questions)} 个题目")
    print(f"题目来源分布: {[(q.source, len([q for q in questions if q.source == q.source])) for q in questions]}")
    
    # 检查学生
    students = User.query.filter_by(role='student').all()
    print(f"\n共有 {len(students)} 个学生")
    for student in students:
        print(f"学生 {student.id}: {student.username}")
        # 检查学生已参与的测验
        student_quizzes = StudentQuiz.query.filter_by(student_id=student.id).all()
        print(f"  已参与测验数: {len(student_quizzes)}")
        for sq in student_quizzes:
            print(f"    测验 {sq.quiz_id}, 状态: {sq.status}")