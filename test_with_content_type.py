import requests
import json
import time

# 设置API端点URL
API_URL = "http://localhost:5000/api/evaluation_report"

# 测试文件路径
TEST_FILE_PATH = "test_report_1_result.txt"

def test_without_content_type():
    """测试不设置Content-Type的情况"""
    print("\n1. 测试不设置Content-Type:")
    payload = {"file_path": TEST_FILE_PATH}
    
    try:
        # 故意不设置Content-Type
        response = requests.post(API_URL, data=json.dumps(payload))
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        # 检查是否是415错误
        if response.status_code == 415:
            print("✅ 预期得到415 Unsupported Media Type错误")
        else:
            print("❌ 未得到预期的415错误")
            
    except Exception as e:
        print(f"请求失败: {e}")

def test_with_content_type():
    """测试设置Content-Type为application/json的情况"""
    print("\n2. 测试设置Content-Type为application/json:")
    payload = {"file_path": TEST_FILE_PATH}
    
    # 方法1：使用headers参数明确设置Content-Type
    headers = {"Content-Type": "application/json"}
    
    try:
        # 使用json参数会自动设置Content-Type为application/json
        # response = requests.post(API_URL, json=payload)
        
        # 或者手动设置headers并使用data参数
        response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        
        # 检查是否成功（状态码200）
        if response.status_code == 200:
            print("✅ 请求成功，Content-Type设置正确!")
        else:
            print("❌ 请求未成功，请检查服务器状态")
            
    except Exception as e:
        print(f"请求失败: {e}")

def main():
    print("Content-Type设置测试工具")
    print("="*50)
    print(f"目标API: {API_URL}")
    print(f"测试文件: {TEST_FILE_PATH}")
    print("\n注意：请确保Flask服务器已在运行!")
    print("提示：在另一个终端运行 'python app.py'")
    
    input("\n按Enter键开始测试...")
    
    try:
        # 先测试不设置Content-Type
        test_without_content_type()
        time.sleep(1)
        
        # 再测试设置Content-Type
        test_with_content_type()
        
    except KeyboardInterrupt:
        print("\n测试已取消")
    except Exception as e:
        print(f"\n测试过程中发生错误: {e}")
    finally:
        print("\n测试完成!")

if __name__ == "__main__":
    main()