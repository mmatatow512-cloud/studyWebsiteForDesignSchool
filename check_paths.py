from app import app, db, Course, Unit

with app.app_context():
    print('课程信息:')
    courses = Course.query.all()
    for course in courses:
        print(f'ID: {course.id}, 代码: {course.course_code}, 标题: {course.title}, 视频路径: {course.video_path}')
    
    print('\n单元信息:')
    units = Unit.query.all()
    for unit in units:
        print(f'ID: {unit.id}, 课程ID: {unit.course_id}, 标题: {unit.unit_title}, 文件路径: {unit.file_path}')
