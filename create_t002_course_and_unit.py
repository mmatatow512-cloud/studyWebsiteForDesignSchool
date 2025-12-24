from app import app, db, User, Course, Unit
import os

# 创建T002课程和相关单元
if __name__ == '__main__':
    with app.app_context():
        try:
            # 获取第一个教师用户
            teacher = User.query.filter_by(role='teacher').first()
            if not teacher:
                print("No teacher user found. Creating a test teacher...")
                teacher = User(
                    username='testteacher',
                    email='testteacher@example.com',
                    password='password123',  # 实际应用中应该哈希密码
                    role='teacher'
                )
                db.session.add(teacher)
                db.session.commit()
            
            print(f'Using teacher: ID={teacher.id}, Username={teacher.username}')
            
            # 检查T002课程是否存在
            t002_course = Course.query.filter_by(course_code='T002').first()
            if not t002_course:
                print("Creating T002 course...")
                t002_course = Course(
                    course_code='T002',
                    title='ps基础',
                    description='Photoshop基础教程',
                    teacher_id=teacher.id,
                    credit=2.0
                )
                db.session.add(t002_course)
                db.session.commit()
                print(f'Successfully created T002 course: ID={t002_course.id}')
            else:
                print(f'Found T002 course: ID={t002_course.id}, Title={t002_course.title}')
            
            # 检查是否已有单元
            existing_units = Unit.query.filter_by(course_id=t002_course.id).all()
            print(f'Existing units for T002: {len(existing_units)}')
            
            # 如果没有单元，创建一个
            if len(existing_units) == 0:
                video_file = 'unit_1_34521220812-1-192.mp4'
                file_path = f'T002/{video_file}'
                
                # 检查文件是否存在
                full_path = os.path.join('course_files', file_path)
                if os.path.exists(full_path):
                    print(f'Found video file: {full_path}')
                    
                    # 创建新单元
                    new_unit = Unit(
                        course_id=t002_course.id,
                        unit_title='第一单元',
                        file_path=file_path,
                        order_index=1
                    )
                    
                    db.session.add(new_unit)
                    db.session.commit()
                    print(f'Successfully created unit with file path: {file_path}')
                else:
                    print(f'Video file not found: {full_path}')
            else:
                for unit in existing_units:
                    print(f'  Unit: ID={unit.id}, Title={unit.unit_title}, File Path={unit.file_path}')
                    
        except Exception as e:
            print(f'Error: {str(e)}')
            import traceback
            traceback.print_exc()
            db.session.rollback()