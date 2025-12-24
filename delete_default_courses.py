from app import app, db, User, Course

with app.app_context():
    # 查找default_teacher用户
    default_teacher = User.query.filter_by(username='default_teacher').first()
    
    if default_teacher:
        print(f"找到default_teacher用户，ID: {default_teacher.id}")
        
        # 查找该用户创建的所有课程
        courses = Course.query.filter_by(teacher_id=default_teacher.id).all()
        
        if courses:
            print(f"找到{len(courses)}门预设课程，准备删除：")
            for course in courses:
                print(f"- {course.course_code}: {course.title}")
                db.session.delete(course)
            
            # 提交更改
            db.session.commit()
            print("所有预设课程已成功删除！")
        else:
            print("没有找到default_teacher创建的课程")
    else:
        print("没有找到default_teacher用户")
