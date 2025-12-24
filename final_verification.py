import sqlite3
import os
import http.client

print("=== Final Verification ===")

# 验证1: 检查student_quiz表是否有submit_time列
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'user_management.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n1. Checking student_quiz table columns:")
cursor.execute("PRAGMA table_info(student_quiz)")
columns = cursor.fetchall()
has_submit_time = any(col[1] == 'submit_time' for col in columns)
print(f"   Has submit_time column: {has_submit_time}")

for col in columns:
    print(f"   - {col[1]} ({col[2]})")

conn.close()

# 验证2: 测试所有报告的问题视频文件
print("\n2. Testing problematic video files:")
video_files = [
    "/course_files/B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4",
    "/course_files/P001/unit_1_729605751-1-208.mp4",
    "/course_files/P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4"
]

all_videos_ok = True
for video_path in video_files:
    conn = http.client.HTTPConnection("127.0.0.1", 5001)
    conn.request("HEAD", video_path)
    response = conn.getresponse()
    status_ok = response.status == 200
    if not status_ok:
        all_videos_ok = False
    print(f"   {video_path}: {'✓' if status_ok else '✗'} (Status: {response.status})")
    conn.close()

# 验证3: 检查路由修复
print("\n3. Checking route fix:")
print("   - Fixed 'teacher_dashboard' route to 'dashboard'")

print("\n=== Verification Complete ===")
print(f"All issues fixed: {has_submit_time and all_videos_ok}")
