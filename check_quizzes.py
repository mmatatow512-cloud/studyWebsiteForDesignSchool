from app import app, db, Quiz, QuizQuestion

# 查看当前所有测验的情况
def check_quizzes():
    with app.app_context():
        print("=== 当前所有测验情况 ===")
        
        # 获取所有测验
        all_quizzes = Quiz.query.all()
        print(f"总测验数：{len(all_quizzes)}")
        
        if all_quizzes:
            for i, quiz in enumerate(all_quizzes):
                # 检查测验是否关联了题目
                quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
                
                print(f"\n测验 {i+1}：")
                print(f"  ID: {quiz.id}")
                print(f"  标题: {quiz.title}")
                print(f"  教师ID: {quiz.teacher_id}")
                print(f"  课程ID: {quiz.course_id}")
                print(f"  知识点: {quiz.knowledge_points}")
                print(f"  创建时间: {quiz.created_at}")
                print(f"  关联题目数: {len(quiz_questions)}")
                
                if quiz_questions:
                    print("  关联题目ID:", [qq.question_id for qq in quiz_questions])
        else:
            print("数据库中没有测验")

if __name__ == '__main__':
    check_quizzes()