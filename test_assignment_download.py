import os
import sys
import sqlite3

# 设置项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, StudentAssignment

with app.app_context():
    # 查询submission_id为1的记录
    submission = StudentAssignment.query.get(1)
    if not submission:
        print("未找到submission_id为1的作业提交记录")
        sys.exit(1)
    
    print("作业提交记录信息：")
    print(f"submission_id: {submission.id}")
    print(f"student_id: {submission.student_id}")
    print(f"assignment_id: {submission.assignment_id}")
    print(f"file_path: {submission.file_path}")
    print(f"file_type: {submission.file_type}")
    print(f"status: {submission.status}")
    
    # 构建文件路径
    if os.path.isabs(submission.file_path):
        file_path = submission.file_path
    else:
        upload_dir = os.path.join(app.root_path, 'uploads', 'assignments')
        file_path = os.path.join(upload_dir, submission.file_path)
    
    print(f"\n构建的完整文件路径：{file_path}")
    print(f"文件存在：{os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        print(f"文件大小：{os.path.getsize(file_path)} bytes")
    else:
        # 检查上传目录是否存在
        upload_dir = os.path.join(app.root_path, 'uploads', 'assignments')
        print(f"\n上传目录存在：{os.path.exists(upload_dir)}")
        if os.path.exists(upload_dir):
            print("上传目录内容：")
            for item in os.listdir(upload_dir):
                item_path = os.path.join(upload_dir, item)
                print(f"  {item} {'(目录)' if os.path.isdir(item_path) else ''}")
