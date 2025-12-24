from app import app, db, User
from werkzeug.security import generate_password_hash, check_password_hash

with app.app_context():
    # 查询所有用户
    users = User.query.all()
    print("所有用户:")
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 密码: {user.password}, 角色: {user.role}")
    
    # 检查admin用户
    admin_user = User.query.filter_by(username='admin').first()
    if admin_user:
        print(f"\n找到admin用户: {admin_user.username}")
        print(f"密码哈希: {admin_user.password}")
        # 验证密码是否为admin
        password_match = check_password_hash(admin_user.password, 'admin')
        print(f"密码 'admin' 验证结果: {password_match}")
        
        if not password_match:
            # 如果密码不正确，更新密码
            print("更新admin用户密码为 'admin'")
            admin_user.password = generate_password_hash('admin')
            db.session.commit()
            print("密码更新成功")
    else:
        print("\n未找到admin用户，创建一个新的")
        new_admin = User(
            username='admin',
            password=generate_password_hash('admin'),
            role='admin',
            student_id='admin001'
        )
        db.session.add(new_admin)
        db.session.commit()
        print("admin用户创建成功")