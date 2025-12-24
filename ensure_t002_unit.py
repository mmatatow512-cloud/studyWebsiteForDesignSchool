from app import app, db, Course, Unit
import os

# 确保T002课程有单元记录
if __name__ == '__main__':
    with app.app_context():
        try:
            # 检查T002课程
            t002_course = Course.query.filter_by(course_code='T002').first()
            if t002_course:
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
                        # 检查文件路径格式，确保使用正斜杠
                        if '\\' in unit.file_path:
                            unit.file_path = unit.file_path.replace('\\', '/')
                            print(f'  Updated file path to: {unit.file_path}')
                            db.session.commit()
            else:
                print('T002 course not found')
                
        except Exception as e:
            print(f'Error: {str(e)}')
            import traceback
            traceback.print_exc()
            db.session.rollback()