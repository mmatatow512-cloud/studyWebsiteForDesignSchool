from app import app, db
with app.app_context():
    print('数据库表:', db.metadata.tables.keys())
    print('数据库URI:', app.config['SQLALCHEMY_DATABASE_URI'])
