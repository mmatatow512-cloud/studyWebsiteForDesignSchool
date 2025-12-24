from app import app, db, Course, Unit
import os

# 详细调试单元创建过程
if __name__ == '__main__':
    with app.app_context():
        try:
            # 检查数据库连接
            print(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
            
            # 检查T002课程
            t002_course = Course.query.filter_by(course_code='T002').first()
            if t002_course:
                print(f'Found T002 course: ID={t002_course.id}, Title={t002_course.title}')
                
                # 检查是否已有单元
                existing_units = Unit.query.filter_by(course_id=t002_course.id).all()
                print(f'Existing units for T002: {len(existing_units)}')
                for unit in existing_units:
                    print(f'  Unit: ID={unit.id}, Title={unit.unit_title}, File Path={unit.file_path}')
                
                # 创建一个新单元
                new_unit = Unit(
                    course_id=t002_course.id,
                    unit_title='Debug Unit 1',
                    file_path='T002/unit_1_34521220812-1-192.mp4',
                    order_index=1
                )
                
                print(f'Creating new unit: {new_unit}')
                db.session.add(new_unit)
                print(f'Added to session')
                
                # 检查会话中的变更
                print(f'Session dirty: {db.session.dirty}')
                print(f'Session new: {db.session.new}')
                
                # 提交变更
                db.session.commit()
                print(f'Committed to database')
                
                # 验证创建
                created_unit = Unit.query.filter_by(id=new_unit.id).first()
                if created_unit:
                    print(f'Successfully created unit: ID={created_unit.id}, File Path={created_unit.file_path}')
                else:
                    print(f'Failed to create unit')
                    
                # 再次检查所有单元
                all_units = Unit.query.filter_by(course_id=t002_course.id).all()
                print(f'All units for T002 after creation: {len(all_units)}')
            else:
                print('T002 course not found')
                
        except Exception as e:
            print(f'Error: {str(e)}')
            import traceback
            traceback.print_exc()
            db.session.rollback()