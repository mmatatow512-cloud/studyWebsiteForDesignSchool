import requests
import json

def test_api_with_invalid_content_type():
    """测试不设置Content-Type头部的情况"""
    url = "http://localhost:5001/api/evaluation/report"
    
    # 准备JSON数据
    data = {
        "file_path": "test_report_1_result.txt"
    }
    
    # 发送请求但不设置Content-Type
    try:
        response = requests.post(url, data=data)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except requests.exceptions.ConnectionError:
        print("错误: 无法连接到服务器，请确保服务器正在运行")

def test_api_with_correct_content_type():
    """测试设置正确的Content-Type头部的情况"""
    url = "http://localhost:5001/api/evaluation/report"
    
    # 准备JSON数据
    data = {
        "file_path": "test_report_1_result.txt"
    }
    
    # 设置正确的Content-Type
    headers = {
        "Content-Type": "application/json"
    }
    
    # 发送请求
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"\n使用正确Content-Type的响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except requests.exceptions.ConnectionError:
        print("\n错误: 无法连接到服务器，请确保服务器正在运行")

if __name__ == "__main__":
    print("===== API Content-Type测试 =====")
    test_api_with_invalid_content_type()
    test_api_with_correct_content_type()
    print("\n测试完成")
