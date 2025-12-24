import os
import sys
import webbrowser

# 设置项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, CompetitionSubmission

with app.app_context():
    # 查询submission_id为1的记录
    submission = CompetitionSubmission.query.get(1)
    if not submission:
        print("未找到submission_id为1的竞赛投递记录")
        sys.exit(1)
    
    print("竞赛投递记录信息：")
    print(f"submission_id: {submission.id}")
    print(f"file_path: {submission.pdf_path}")
    
    # 构建下载URL
    download_url = f"http://127.0.0.1:5001/download_competition_file/1"
    
    print(f"\n下载URL: {download_url}")
    print("正在打开浏览器测试下载功能...")
    
    # 打开浏览器访问下载URL
    webbrowser.open(download_url)
    
    print("请在浏览器中检查下载是否成功。")
    print("注意：您可能需要先登录系统。")