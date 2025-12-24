import requests
import time

# 测试SSE API
def test_sse_api():
    url = "http://127.0.0.1:5001/api/ai-tutor/chat?question=设计基础"
    
    try:
        print(f"发送请求到: {url}")
        response = requests.get(url, stream=True)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应头: {response.headers}")
        
        # 检查是否是SSE响应
        if response.headers.get('Content-Type') != 'text/event-stream':
            print("错误: 响应不是SSE格式")
            print(f"响应内容: {response.text}")
            return
            
        print("开始接收SSE事件...")
        
        # 处理流式响应
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                chunk_str = chunk.decode('utf-8')
                print(f"收到块: {chunk_str}")
                
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
    except Exception as e:
        print(f"其他错误: {e}")

if __name__ == "__main__":
    test_sse_api()
