from app import app, db, Unit, Course
import os

# 获取应用上下文
with app.app_context():
    # 检查特定课程的单元信息
    course_codes = ['B001', 'P001']
    
    for course_code in course_codes:
        print(f"\n=== 检查课程 {course_code} ===")
        
        # 查询课程
        course = Course.query.filter_by(course_code=course_code).first()
        if not course:
            print(f"未找到课程 {course_code}")
            continue
        
        print(f"课程ID: {course.id}, 标题: {course.title}")
        
        # 查询课程的所有单元
        units = Unit.query.filter_by(course_id=course.id).all()
        print(f"共有 {len(units)} 个单元")
        
        # 检查每个单元的文件路径
        for unit in units:
            print(f"\n单元ID: {unit.id}, 标题: {unit.unit_title}")
            print(f"数据库中存储的file_path: {unit.file_path}")
            
            # 检查文件是否存在
            file_path = os.path.join('course_files', unit.file_path)
            print(f"实际文件路径: {os.path.abspath(file_path)}")
            print(f"文件是否存在: {os.path.exists(file_path)}")
            
            # 如果文件不存在，检查目录结构
            if not os.path.exists(file_path):
                directory = os.path.dirname(file_path)
                if os.path.exists(directory):
                    print(f"目录存在，但文件不存在。目录内容:")
                    for f in os.listdir(directory):
                        print(f"  - {f}")
                else:
                    print(f"目录不存在: {directory}")
                    if os.path.exists('course_files'):
                        print(f"course_files目录存在，内容:")
                        for f in os.listdir('course_files'):
                            print(f"  - {f}")