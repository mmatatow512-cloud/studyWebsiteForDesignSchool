from app import app, db

with app.app_context():
    print("正在重新创建数据库表...")
    db.drop_all()
    db.create_all()
    print("数据库表已重新创建完成！")