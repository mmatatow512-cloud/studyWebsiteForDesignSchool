from app import app, db, User

with app.app_context():
    # 检查所有教师用户
    teachers = User.query.filter_by(role='teacher').all()
    print(f"共有 {len(teachers)} 个教师用户")
    for teacher in teachers:
        print(f"教师 {teacher.id}: {teacher.username}")