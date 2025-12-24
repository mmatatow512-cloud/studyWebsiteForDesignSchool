from app import app, db, User

with app.app_context():
    # 检查并添加 course_count 列
    with db.engine.connect() as conn:
        # 检查 courses 列是否存在
        result = conn.execute(db.text("PRAGMA table_info(user)"))
        columns = [row[1] for row in result]
        
        if 'courses' in columns and 'course_count' not in columns:
            # 添加 course_count 列
            conn.execute(db.text("ALTER TABLE user ADD COLUMN course_count INTEGER DEFAULT 0"))
            # 将旧数据迁移到新列
            conn.execute(db.text("UPDATE user SET course_count = courses"))
            # 删除旧列
            conn.execute(db.text("""CREATE TABLE user_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(80) UNIQUE NOT NULL,
                password VARCHAR(120) NOT NULL,
                role VARCHAR(20) NOT NULL,
                student_id VARCHAR(20) UNIQUE NOT NULL,
                course_count INTEGER DEFAULT 0,
                assignments INTEGER DEFAULT 0,
                completed_assignments INTEGER DEFAULT 0,
                average_score FLOAT DEFAULT 0.0,
                student_count INTEGER DEFAULT 0,
                graded_assignments INTEGER DEFAULT 0,
                questions_answered INTEGER DEFAULT 0,
                quizzes_graded INTEGER DEFAULT 0,
                suggestions_provided INTEGER DEFAULT 0
            )"""))
            conn.execute(db.text("INSERT INTO user_new SELECT id, username, password, role, student_id, course_count, assignments, completed_assignments, average_score, student_count, graded_assignments, questions_answered, quizzes_graded, suggestions_provided FROM user"))
            conn.execute(db.text("DROP TABLE user"))
            conn.execute(db.text("ALTER TABLE user_new RENAME TO user"))
            print("数据库迁移成功：添加了 course_count 列，迁移了数据，删除了旧的 courses 列")
        elif 'course_count' in columns:
            print("course_count 列已存在，无需迁移")
        else:
            print("未找到 courses 列，无法迁移")
    
    # 确保所有表都已创建
    db.create_all()
    print("数据库表创建/验证完成")
