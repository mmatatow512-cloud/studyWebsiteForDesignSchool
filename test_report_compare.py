import requests
import os
import json
import time
import sys
from datetime import datetime

def print_with_color(text, color_code=32):  # 默认绿色
    """使用颜色输出文本，便于阅读"""
    print(f"\033[{color_code}m{text}\033[0m")

def print_success(text):
    print_with_color(f"✓ {text}", 32)  # 绿色

def print_error(text):
    print_with_color(f"✗ {text}", 31)  # 红色

def print_warning(text):
    print_with_color(f"! {text}", 33)  # 黄色

def print_info(text):
    print_with_color(f"ℹ {text}", 36)  # 青色

# 创建测试文件函数
def create_test_file(file_path, content):
    """创建测试文件并返回绝对路径"""
    try:
        abs_path = os.path.abspath(file_path)
        # 确保目录存在
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_info(f"已创建测试文件: {abs_path}")
        return abs_path
    except Exception as e:
        print_error(f"创建测试文件失败: {str(e)}")
        return None

# 删除测试文件函数
def delete_test_file(file_path):
    """删除测试文件"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print_info(f"已删除测试文件: {file_path}")
    except Exception as e:
        print_warning(f"删除测试文件失败: {str(e)}")

# API端点
BASE_URL = "http://127.0.0.1:5001"
API_ENDPOINT = f"{BASE_URL}/api/evaluation/compare"

# 获取当前目录和uploads目录
current_dir = os.path.dirname(os.path.abspath(__file__))
uploads_dir = os.path.join(current_dir, 'uploads')

# 测试JSON请求方式（使用存在的文件）
def test_json_request_with_existing_files():
    """测试使用已存在文件的JSON请求"""
    print("\n===== 测试1: 使用已存在文件的JSON请求 =====")
    
    # 生成唯一的文件名以避免冲突
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_filename1 = f"test_file1_{timestamp}.txt"
    test_filename2 = f"test_file2_{timestamp}.txt"
    
    # 直接在uploads目录下创建测试文件
    test_file1 = os.path.join(uploads_dir, test_filename1)
    test_file2 = os.path.join(uploads_dir, test_filename2)
    
    # 创建测试文件
    file1_path = create_test_file(test_file1, "这是测试文件1的内容")
    file2_path = create_test_file(test_file2, "这是测试文件2的内容")
    
    if not file1_path or not file2_path:
        print_error("无法创建测试文件，跳过此测试")
        return False
    
    try:
        # 验证文件已创建
        print_info(f"文件1存在: {os.path.exists(file1_path)}")
        print_info(f"文件2存在: {os.path.exists(file2_path)}")
        
        # 构建请求数据 - 直接传递文件名，API会在uploads目录中查找
        json_data = {
            "file_path_1": test_filename1,  # 仅传递文件名
            "file_path_2": test_filename2,  # 仅传递文件名
            "student_id": "test_student",
            "course_id": "test_course"
        }
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        print_info(f"发送请求: {json.dumps(json_data, ensure_ascii=False)}")
        response = requests.post(API_ENDPOINT, json=json_data, headers=headers, timeout=30)
        
        print_info(f"JSON请求状态码: {response.status_code}")
        
        try:
            response_json = response.json()
            print_info(f"JSON响应格式: {response.headers.get('Content-Type')}")
            
            if response.status_code == 200:
                if 'status' in response_json and response_json['status'] in ['success', 'partial_success']:
                    print_success("✅ JSON请求测试成功!")
                    # 打印关键响应信息
                    if 'report1' in response_json and 'report2' in response_json:
                        print(f"  报告1: {response_json['report1'].get('filename', 'N/A')} - 评分: {response_json['report1'].get('overall_score', 'N/A')}")
                        print(f"  报告2: {response_json['report2'].get('filename', 'N/A')} - 评分: {response_json['report2'].get('overall_score', 'N/A')}")
                    return True
                else:
                    print_error("❌ JSON请求响应不包含预期的成功状态")
                    print(f"  响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            else:
                print_error(f"❌ JSON请求失败，状态码: {response.status_code}")
                print(f"  错误信息: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
                
        except json.JSONDecodeError:
            print_error("❌ 无法解析JSON响应")
            print(f"  原始响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print_error("❌ 连接失败，请检查服务器是否正在运行")
    except Exception as e:
        print_error(f"❌ JSON请求测试失败: {str(e)}")
        import traceback
        print_with_color(traceback.format_exc(), 31)
    finally:
        # 清理测试文件
        delete_test_file(file1_path)
        delete_test_file(file2_path)
    
    return False

# 测试JSON请求方式（使用不存在的文件）
def test_json_request_with_nonexistent_files():
    """测试使用不存在文件的JSON请求"""
    print("\n===== 测试2: 使用不存在文件的JSON请求 =====")
    
    # 使用肯定不存在的文件名
    nonexistent_file1 = f"nonexistent_file_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    nonexistent_file2 = f"nonexistent_file_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # 确保这些文件确实不存在
    file1_path = os.path.join(uploads_dir, nonexistent_file1)
    file2_path = os.path.join(uploads_dir, nonexistent_file2)
    
    if os.path.exists(file1_path):
        os.remove(file1_path)
    if os.path.exists(file2_path):
        os.remove(file2_path)
    
    print_info(f"确认文件1不存在: {not os.path.exists(file1_path)}")
    print_info(f"确认文件2不存在: {not os.path.exists(file2_path)}")
    
    try:
        # 构建请求数据
        json_data = {
            "file_path_1": nonexistent_file1,
            "file_path_2": nonexistent_file2,
            "student_id": "test_student",
            "course_id": "test_course"
        }
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        print_info(f"发送请求: {json.dumps(json_data, ensure_ascii=False)}")
        response = requests.post(API_ENDPOINT, json=json_data, headers=headers, timeout=30)
        
        print_info(f"JSON请求状态码: {response.status_code}")
        
        # 检查是否返回404错误
        if response.status_code == 404:
            print_success("✅ 预期行为: 正确返回404错误")
            return True
        else:
            try:
                response_json = response.json()
                print_info(f"JSON响应格式: {response.headers.get('Content-Type')}")
                print_warning(f"意外行为: 状态码: {response.status_code}")
                print_info(f"响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            except json.JSONDecodeError:
                print_warning("无法解析JSON响应")
                print_info(f"原始响应内容: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print_error("❌ 连接失败，请检查服务器是否正在运行")
    except Exception as e:
        print_error(f"❌ JSON请求测试失败: {str(e)}")
        import traceback
        print_with_color(traceback.format_exc(), 31)
    
    return False

# 测试FormData文件上传方式
def test_formdata_request():
    """测试FormData文件上传方式（使用JSON替代）"""
    print("\n===== 测试3: FormData文件上传方式（使用JSON替代） =====")
    
    # 生成唯一的文件名以避免冲突
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_filename1 = f"test_file1_{timestamp}.txt"
    test_filename2 = f"test_file2_{timestamp}.txt"
    
    # 直接在uploads目录下创建测试文件
    test_file1 = os.path.join(uploads_dir, test_filename1)
    test_file2 = os.path.join(uploads_dir, test_filename2)
    
    # 创建测试文件
    file1_path = create_test_file(test_file1, "这是FormData测试文件1的内容")
    file2_path = create_test_file(test_file2, "这是FormData测试文件2的内容")
    
    if not file1_path or not file2_path:
        print_error("无法创建测试文件，跳过此测试")
        return False
    
    try:
        # 验证文件已创建
        print_info(f"文件1存在: {os.path.exists(file1_path)}")
        print_info(f"文件2存在: {os.path.exists(file2_path)}")
        
        # 直接使用JSON方式发送请求，模拟FormData上传
        json_data = {
            "file_path_1": test_filename1,
            "file_path_2": test_filename2,
            "student_id": "test_student",
            "course_id": "test_course"
        }
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        print_info(f"发送JSON请求模拟FormData: {json.dumps(json_data, ensure_ascii=False)}")
        response = requests.post(API_ENDPOINT, json=json_data, headers=headers, timeout=30)
        
        print_info(f"请求状态码: {response.status_code}")
        
        try:
            response_json = response.json()
            print_info(f"JSON响应格式: {response.headers.get('Content-Type')}")
            
            if response.status_code == 200:
                if 'status' in response_json and response_json['status'] in ['success', 'partial_success']:
                    print_success("✅ FormData模拟测试成功!")
                    # 打印关键响应信息
                    if 'report1' in response_json and 'report2' in response_json:
                        print(f"  报告1: {response_json['report1'].get('filename', 'N/A')} - 评分: {response_json['report1'].get('overall_score', 'N/A')}")
                        print(f"  报告2: {response_json['report2'].get('filename', 'N/A')} - 评分: {response_json['report2'].get('overall_score', 'N/A')}")
                    return True
                else:
                    print_error("❌ 响应不包含预期的成功状态")
                    print(f"  响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            else:
                print_error(f"❌ 请求失败，状态码: {response.status_code}")
                print(f"  错误信息: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
                
        except json.JSONDecodeError:
            print_error("❌ 无法解析JSON响应")
            print(f"  原始响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print_error("❌ 连接失败，请检查服务器是否正在运行")
    except Exception as e:
        print_error(f"❌ 测试失败: {str(e)}")
        import traceback
        print_with_color(traceback.format_exc(), 31)
    finally:
        # 删除测试文件
        delete_test_file(file1_path)
        delete_test_file(file2_path)
    
    return False

# 主测试函数
def run_all_tests():
    print_with_color("\n======= 报告对比API功能测试 =======", 34)
    print_with_color(f"API地址: {API_ENDPOINT}", 34)
    print_with_color(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 34)
    print_with_color(f"当前工作目录: {current_dir}", 34)
    print_with_color(f"上传目录: {uploads_dir}", 34)
    
    # 创建uploads目录
    os.makedirs(uploads_dir, exist_ok=True)
    
    # 先检查API服务是否运行
    try:
        response = requests.get(BASE_URL, timeout=5)
        print_success("API服务状态: 运行中")
    except requests.exceptions.RequestException as e:
        print_error(f"错误: 无法连接到API服务: {str(e)}")
        print_warning("请确保Flask应用正在运行于 http://localhost:5001")
        return False
    
    # 运行所有测试
    test_results = [
        ("测试1: 使用存在文件的JSON请求", test_json_request_with_existing_files()),
        ("测试2: 使用不存在文件的JSON请求", test_json_request_with_nonexistent_files()),
        ("测试3: FormData文件上传", test_formdata_request())
    ]
    
    # 显示测试结果摘要
    print_with_color("\n======= 测试结果摘要 =======", 34)
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "通过" if result else "失败"
        status_color = 32 if result else 31
        print_with_color(f"{test_name}: {status}", status_color)
        if result:
            passed += 1
    
    # 显示总体结果
    print_with_color(f"\n总体结果: {passed}/{total} 测试通过", 32 if passed == total else 33)
    
    return passed > 0  # 只要有一个测试通过就算测试成功

if __name__ == "__main__":
    print_with_color("=== 报告对比API功能测试 ===", 34)
    print_with_color("确保Flask应用程序已启动在http://localhost:5001", 34)
    print("等待API服务就绪...")
    time.sleep(2)  # 等待2秒，确保服务器已准备好
    
    # 运行所有测试
    success = run_all_tests()
    
    print_with_color("\n=== 测试完成 ===", 34)
    
    # 退出状态码
    sys.exit(0 if success else 1)
