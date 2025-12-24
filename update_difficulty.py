from app import app, db, Question, QuizQuestion

# 在应用上下文中运行
def update_difficulty():
    with app.app_context():
        # 先删除引用简单难度题目的QuizQuestion记录
        simple_question_ids = [q.id for q in Question.query.filter_by(difficulty='简单').all()]
        if simple_question_ids:
            deleted_quiz_questions = QuizQuestion.query.filter(QuizQuestion.question_id.in_(simple_question_ids)).delete()
            print(f"删除了 {deleted_quiz_questions} 条测验题目关联记录")

        # 删除所有简单难度的题目
        simple_questions = Question.query.filter_by(difficulty='简单').all()
        for question in simple_questions:
            db.session.delete(question)

        db.session.commit()
        print(f"删除了 {len(simple_questions)} 条简单难度的题目")

        # 查看剩余题目难度分布
        remaining_questions = Question.query.all()
        difficulty_count = {}
        for question in remaining_questions:
            difficulty_count[question.difficulty] = difficulty_count.get(question.difficulty, 0) + 1

        print("剩余题目难度分布：")
        for difficulty, count in difficulty_count.items():
            print(f"{difficulty}: {count} 题")

if __name__ == "__main__":
    update_difficulty()