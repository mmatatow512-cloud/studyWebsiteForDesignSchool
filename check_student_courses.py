from app import app, db, StudentCourse, User

with app.app_context():
    # 获取学生用户
    student = User.query.filter_by(role='student', id=2).first()
    if student:
        print(f"学生 {student.id}: {student.username}")
        
        # 检查学生已选课程
        student_courses = StudentCourse.query.filter_by(student_id=student.id).all()
        print(f"已选课程数: {len(student_courses)}")
        for sc in student_courses:
            print(f"课程ID: {sc.course_id}")
    else:
        print("未找到学生用户")