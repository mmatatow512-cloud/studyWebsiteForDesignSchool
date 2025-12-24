import http.client

# 测试用户报告的问题视频文件
video_files = [
    "/course_files/B001/unit_1_2ff1b400ce557d715052ab3286d37716.mp4",
    "/course_files/P001/unit_1_729605751-1-208.mp4",
    "/course_files/P001/unit_2_5af2f06321637469ff1b56dabf7f2d05.mp4"
]

for i, video_path in enumerate(video_files, 1):
    print(f"\nTesting video {i}: {video_path}")
    conn = http.client.HTTPConnection("127.0.0.1", 5001)
    conn.request("HEAD", video_path)
    response = conn.getresponse()
    print(f"Status: {response.status} {response.reason}")
    print(f"Content-Type: {response.getheader('Content-Type')}")
    print(f"Content-Length: {response.getheader('Content-Length')}")
    conn.close()