from app import app, db, Quiz, QuizQuestion, StudentQuiz, StudentAnswer

# 删除所有测验
def delete_all_quizzes():
    with app.app_context():
        print("=== 删除所有测验 ===")
        
        # 获取所有测验
        all_quizzes = Quiz.query.all()
        print(f"总测验数：{len(all_quizzes)}")
        
        if all_quizzes:
            # 删除所有测验
            for quiz in all_quizzes:
                print(f"正在删除测验：{quiz.title} (ID: {quiz.id})")
                
                # 按照正确顺序删除：
                # 1. 删除学生答题记录
                student_quizzes = StudentQuiz.query.filter_by(quiz_id=quiz.id).all()
                for sq in student_quizzes:
                    StudentAnswer.query.filter_by(student_quiz_id=sq.id).delete()
                    db.session.delete(sq)
                
                # 2. 删除测验题目关联
                QuizQuestion.query.filter_by(quiz_id=quiz.id).delete()
                
                # 3. 删除测验本身
                db.session.delete(quiz)
            
            # 提交事务
            db.session.commit()
            print(f"成功删除了 {len(all_quizzes)} 个测验")
        else:
            print("没有发现测验")
        
        print("=== 操作完成 ===")

if __name__ == '__main__':
    delete_all_quizzes()