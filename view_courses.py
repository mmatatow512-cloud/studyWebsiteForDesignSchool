from app import app, db, Course, Unit

with app.app_context():
    # 获取所有课程
    courses = Course.query.all()
    
    print('课程列表:')
    print('-' * 50)
    
    for course in courses:
        print(f'ID: {course.id}')
        print(f'课程代码: {course.course_code}')
        print(f'标题: {course.title}')
        print(f'教师ID: {course.teacher_id}')
        
        # 获取该课程的所有单元
        units = Unit.query.filter_by(course_id=course.id).order_by(Unit.order_index).all()
        print(f'单元数量: {len(units)}')
        
        if units:
            print('单元列表:')
            for unit in units:
                print(f'  - 单元ID: {unit.id}, 标题: {unit.unit_title}, 顺序: {unit.order_index}, 文件路径: {unit.file_path}')
        else:
            print('该课程暂无教学单元')
        
        print('-' * 50)
