from app import app, db, User
from werkzeug.security import generate_password_hash

# 在应用上下文中运行
with app.app_context():
    # 查找用户001
    user = User.query.filter_by(username='001').first()
    
    if user:
        # 为用户设置正确的哈希密码
        user.password = generate_password_hash('123456', method='pbkdf2:sha256')
        db.session.commit()
        print(f"已成功修复用户 {user.username} 的密码")
        print(f"新的密码哈希: {user.password}")
    else:
        print("未找到用户001")
