import requests
import json

# 示例1：使用requests库发送带有正确Content-Type的POST请求
def test_with_correct_content_type():
    print("示例1：使用requests库设置Content-Type")
    
    # API端点URL（请根据实际情况修改）
    url = "http://localhost:5000/api/evaluation_report"
    
    # 请求数据
    payload = {
        "file_path": "test_report_1_result.txt"
    }
    
    # 设置headers，明确指定Content-Type为application/json
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # 发送POST请求，使用json参数自动设置Content-Type
        response = requests.post(url, json=payload)
        
        # 或者使用以下方式手动设置headers
        # response = requests.post(url, data=json.dumps(payload), headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

# 示例2：使用curl命令行工具设置Content-Type（仅供参考）
def curl_example():
    print("\n示例2：使用curl命令行设置Content-Type")
    curl_command = '''
curl -X POST "http://localhost:5000/api/evaluation_report" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "test_report_1_result.txt"}'
'''
    print(curl_command)

# 示例3：使用JavaScript fetch API设置Content-Type（前端代码示例）
def javascript_example():
    print("\n示例3：使用JavaScript fetch API设置Content-Type")
    js_code = '''
// JavaScript代码示例
fetch('http://localhost:5000/api/evaluation_report', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ file_path: 'test_report_1_result.txt' })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
'''
    print(js_code)

if __name__ == "__main__":
    print("Content-Type设置示例")
    print("="*50)
    test_with_correct_content_type()
    curl_example()
    javascript_example()
    print("\n注意：运行示例1前，请确保Flask服务器正在运行")