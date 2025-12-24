import requests
import os
import sys

# 测试简单的下载请求
def test_simple_download():
    download_url = "http://127.0.0.1:5001/download_assignment_file/1"
    
    print(f"发送请求到: {download_url}")
    
    try:
        response = requests.get(download_url, allow_redirects=True)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应URL: {response.url}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容长度: {len(response.content)} bytes")
        
        if response.status_code == 200:
            # 检查内容类型
            content_type = response.headers.get('content-type', '')
            if 'pdf' in content_type.lower():
                # 保存PDF文件
                filename = 'test_download.pdf'
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"\n文件已保存为: {filename}")
                print(f"文件大小: {os.path.getsize(filename)} bytes")
            else:
                print(f"\n内容类型不是PDF: {content_type}")
                # 打印前100个字符
                print(f"响应内容前100个字符: {response.text[:100]}...")
        else:
            print(f"\n响应内容前200个字符: {response.text[:200]}...")
            
    except Exception as e:
        print(f"请求发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_download()
