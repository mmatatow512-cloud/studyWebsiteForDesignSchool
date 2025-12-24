import requests
import json
import time

# 测试AI导师聊天API，特别是"什么是blender"的请求
question = "什么是blender"
# 正确构建URL，只编码参数值
url = f"http://127.0.0.1:5001/api/ai-tutor/chat?question={requests.utils.quote(question)}"

print(f"Testing API with question: {question}")
print(f"URL: {url}")
print("=" * 50)

try:
    # 发送请求，设置stream=True以接收流式响应
    response = requests.get(url, stream=True)
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("\nResponse Body:")
    
    # 逐行读取响应内容
    for line in response.iter_lines():
        if line:
            # 解码并打印行内容
            decoded_line = line.decode('utf-8')
            print(f"  {decoded_line}")
            
            # 如果是数据行，尝试解析JSON
            if decoded_line.startswith('data: '):
                data_content = decoded_line[6:]
                if data_content == '[DONE]':
                    print("  End of stream")
                    break
                try:
                    json_data = json.loads(data_content)
                    print(f"    Parsed JSON: {json.dumps(json_data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"    Invalid JSON: {data_content}")
            
        # 添加一些延迟，以便观察响应流
        time.sleep(0.1)
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()