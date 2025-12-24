from app import app, db, Quiz, QuizQuestion, StudentQuiz, StudentAnswer

# 删除没有题目的测验
def delete_empty_quizzes():
    with app.app_context():
        print("=== 检查并删除没有题目的测验 ===")
        
        # 获取所有测验
        all_quizzes = Quiz.query.all()
        print(f"总测验数：{len(all_quizzes)}")
        
        # 统计并删除没有题目的测验
        empty_quizzes = []
        for quiz in all_quizzes:
            # 检查测验是否关联了题目
            quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz.id).all()
            if not quiz_questions:
                empty_quizzes.append(quiz)
        
        print(f"没有题目的测验数：{len(empty_quizzes)}")
        
        if empty_quizzes:
            # 删除这些没有题目的测验
            for quiz in empty_quizzes:
                print(f"正在删除测验：{quiz.title} (ID: {quiz.id})")
                
                # 按照正确顺序删除：
                # 1. 删除学生答题记录
                student_quizzes = StudentQuiz.query.filter_by(quiz_id=quiz.id).all()
                for sq in student_quizzes:
                    StudentAnswer.query.filter_by(student_quiz_id=sq.id).delete()
                    db.session.delete(sq)
                
                # 2. 删除测验题目关联（虽然已经没有了，但为了安全还是执行）
                QuizQuestion.query.filter_by(quiz_id=quiz.id).delete()
                
                # 3. 删除测验本身
                db.session.delete(quiz)
            
            # 提交事务
            db.session.commit()
            print(f"成功删除了 {len(empty_quizzes)} 个没有题目的测验")
        else:
            print("没有发现没有题目的测验")
        
        print("=== 操作完成 ===")

if __name__ == '__main__':
    delete_empty_quizzes()