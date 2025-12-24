import requests
import json

# 测试AI导师聊天API
def test_ai_tutor_chat():
    url = 'http://127.0.0.1:5001/api/ai-tutor/chat'
    
    # 测试1: GET请求方式
    print("测试1: GET请求方式")
    try:
        params = {'question': '你好，测试一下AI导师聊天功能'}
        response = requests.get(url, params=params, stream=True)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        # 读取响应内容
        print("响应内容:")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(chunk.decode('utf-8', errors='replace'), end='')
        print()
    except Exception as e:
        print(f"错误: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试2: POST请求方式
    print("测试2: POST请求方式")
    try:
        data = {'question': '你好，测试一下AI导师聊天功能（POST）'}
        response = requests.post(url, json=data, stream=True)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        # 读取响应内容
        print("响应内容:")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                print(chunk.decode('utf-8', errors='replace'), end='')
        print()
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    test_ai_tutor_chat()
