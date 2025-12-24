from app import app, db, Quiz, QuizQuestion, Question
import uuid

with app.app_context():
    # 确保有课程ID（假设课程ID为1）
    course_id = 1
    
    # 随机选择10个题目
    questions = Question.query.order_by(db.func.random()).limit(10).all()
    print(f"选择了 {len(questions)} 个题目用于创建测验")
    
    # 创建测验
    quiz = Quiz(
        quiz_id=str(uuid.uuid4()),
        title="测试测验",
        teacher_id=1,
        course_id=course_id,
        knowledge_points="测试知识点",
        difficulty="medium",
        time_limit=30,
        anti_cheat=False
    )
    db.session.add(quiz)
    db.session.commit()
    
    # 关联题目到测验
    for question in questions:
        quiz_question = QuizQuestion(
            quiz_id=quiz.id,
            question_id=question.id,
            score=10  # 每个题目10分
        )
        db.session.add(quiz_question)
    
    db.session.commit()
    print(f"成功创建测验 {quiz.id}: {quiz.title}，关联了 {len(questions)} 个题目")