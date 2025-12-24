from app import app, db, Course

# 获取应用上下文
with app.app_context():
    print("=== 更新课程视频路径格式 ===")
    
    # 查询所有课程
    courses = Course.query.all()
    print(f"找到 {len(courses)} 个课程")
    
    # 统计需要更新的课程数量
    updated_count = 0
    
    for course in courses:
        if course.video_path and '\\' in course.video_path:
            print(f"\n课程ID: {course.id}, 课程代码: {course.course_code}")
            print(f"旧路径: {course.video_path}")
            
            # 将反斜杠替换为正斜杠
            new_path = course.video_path.replace('\\', '/')
            course.video_path = new_path
            
            print(f"新路径: {new_path}")
            updated_count += 1
    
    # 提交更改
    if updated_count > 0:
        db.session.commit()
        print(f"\n已更新 {updated_count} 个课程的视频路径")
    else:
        print("\n没有需要更新的课程视频路径")
        db.session.rollback()