from app import app, db, Course, User, Unit
import os

# 创建一个与T002相关的课程记录
if __name__ == '__main__':
    with app.app_context():
        try:
            # 获取第一个教师用户
            teacher = User.query.filter_by(role='teacher').first()
            if not teacher:
                print('没有教师用户，请先创建教师账户')
                exit()
        
            # 检查是否已存在T002课程
            existing_course = Course.query.filter_by(course_code='T002').first()
            if existing_course:
                print('T002课程已存在')
                # 创建单元记录
                unit = Unit(
                    course_id=existing_course.id,
                    unit_title='测试单元1',
                    file_path='T002/unit_1_34521220812-1-192.mp4',
                    order_index=1
                )
                db.session.add(unit)
                db.session.commit()
                print('测试单元1已创建')
            else:
                # 创建新的T002课程
                new_course = Course(
                    course_code='T002',
                    title='测试课程T002',
                    description='这是一个测试课程，用于解决视频加载问题',
                    teacher_id=teacher.id,
                    credit=2.0
                )
            
                # 添加到数据库
                db.session.add(new_course)
                db.session.commit()
                print('T002课程创建成功')
            
                # 创建单元记录
                unit = Unit(
                    course_id=new_course.id,
                    unit_title='测试单元1',
                    file_path='T002/unit_1_34521220812-1-192.mp4',
                    order_index=1
                )
                db.session.add(unit)
                db.session.commit()
                print('测试单元1已创建')
        except Exception as e:
            print(f'创建过程中发生错误: {str(e)}')
            db.session.rollback()