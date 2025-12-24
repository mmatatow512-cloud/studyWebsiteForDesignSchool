#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
报告对比功能综合测试脚本

此脚本测试/api/evaluation/compare端点的所有功能：
1. JSON请求处理（文件存在情况）
2. JSON请求处理（文件不存在情况）
3. 错误情况处理

所有测试完成后会自动清理创建的测试文件。
"""

import os
import json
import requests
from datetime import datetime

def get_timestamp():
    """获取当前时间戳，用于生成唯一文件名"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def create_test_file(file_path, content="测试内容"):
    """创建测试文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, file_path
    except Exception as e:
        print(f"创建测试文件失败: {e}")
        return False, None

def cleanup_test_files(file_paths):
    """清理测试文件"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"已删除测试文件: {file_path}")
        except Exception as e:
            print(f"删除测试文件失败 {file_path}: {e}")

# 配置
BASE_URL = "http://localhost:5001"
API_URL = f"{BASE_URL}/api/evaluation/compare"
UPLOADS_DIR = os.path.join(os.getcwd(), 'uploads')

def test_json_with_existing_files():
    """测试1: JSON请求 - 文件存在情况"""
    print("\n===== 测试1: JSON请求 - 文件存在情况 =====")
    
    # 生成测试文件名
    timestamp = get_timestamp()
    file1_name = f"test_json_exist1_{timestamp}.txt"
    file2_name = f"test_json_exist2_{timestamp}.txt"
    
    # 创建测试文件
    file1_path = os.path.join(UPLOADS_DIR, file1_name)
    file2_path = os.path.join(UPLOADS_DIR, file2_name)
    
    create_test_file(file1_path, "这是第一个测试文件的内容")
    create_test_file(file2_path, "这是第二个测试文件的内容")
    
    try:
        # 发送JSON请求
        data = {
            "file_path_1": file1_name,
            "file_path_2": file2_name,
            "student_id": "test_student",
            "course_id": "test_course"
        }
        
        print(f"发送请求数据: {json.dumps(data)}")
        response = requests.post(API_URL, json=data, timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        # 检查响应
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ 测试通过! 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"❌ 响应不是有效的JSON: {response.text}")
                return False
        else:
            print(f"❌ 测试失败! 状态码: {response.status_code}, 响应: {response.text}")
            return False
    finally:
        # 清理文件
        cleanup_test_files([file1_path, file2_path])

def test_json_with_nonexistent_files():
    """测试2: JSON请求 - 文件不存在情况"""
    print("\n===== 测试2: JSON请求 - 文件不存在情况 =====")
    
    # 生成不存在的文件名
    timestamp = get_timestamp()
    nonexistent_file1 = f"nonexistent_file1_{timestamp}.txt"
    nonexistent_file2 = f"nonexistent_file2_{timestamp}.txt"
    
    # 确保文件不存在
    file1_path = os.path.join(UPLOADS_DIR, nonexistent_file1)
    file2_path = os.path.join(UPLOADS_DIR, nonexistent_file2)
    if os.path.exists(file1_path):
        os.remove(file1_path)
    if os.path.exists(file2_path):
        os.remove(file2_path)
    
    # 发送JSON请求
    data = {
        "file_path_1": nonexistent_file1,
        "file_path_2": nonexistent_file2,
        "student_id": "test_student",
        "course_id": "test_course"
    }
    
    print(f"发送请求数据: {json.dumps(data)}")
    response = requests.post(API_URL, json=data, timeout=10)
    
    print(f"状态码: {response.status_code}")
    
    # 检查响应 - 应该返回404错误
    if response.status_code == 404:
        print(f"✅ 测试通过! 正确返回了404错误")
        return True
    else:
        print(f"❌ 测试失败! 期望状态码404，实际: {response.status_code}")
        return False

def test_json_with_missing_parameters():
    """测试3: JSON请求 - 缺少必要参数"""
    print("\n===== 测试3: JSON请求 - 缺少必要参数 =====")
    
    # 发送缺少参数的JSON请求
    data = {
        # 缺少 file_path_1 和 file_path_2
        "student_id": "test_student",
        "course_id": "test_course"
    }
    
    print(f"发送请求数据: {json.dumps(data)}")
    response = requests.post(API_URL, json=data, timeout=10)
    
    print(f"状态码: {response.status_code}")
    
    # 检查响应 - 应该返回400错误
    if response.status_code == 400:
        print(f"✅ 测试通过! 正确返回了400错误")
        return True
    else:
        print(f"❌ 测试失败! 期望状态码400，实际: {response.status_code}")
        return False

def test_formdata_via_json():
    """测试4: FormData模拟 - 使用JSON发送文件路径"""
    print("\n===== 测试4: FormData模拟 - 使用JSON发送文件路径 =====")
    
    # 生成测试文件名
    timestamp = get_timestamp()
    file1_name = f"test_form1_{timestamp}.txt"
    file2_name = f"test_form2_{timestamp}.txt"
    
    # 创建测试文件
    file1_path = os.path.join(UPLOADS_DIR, file1_name)
    file2_path = os.path.join(UPLOADS_DIR, file2_name)
    
    create_test_file(file1_path, "这是FormData测试文件1的内容")
    create_test_file(file2_path, "这是FormData测试文件2的内容")
    
    try:
        # 发送JSON请求，模拟FormData行为
        data = {
            "file_path_1": file1_name,
            "file_path_2": file2_name,
            "student_id": "form_student",
            "course_id": "form_course"
        }
        
        print(f"发送模拟FormData请求: {json.dumps(data)}")
        response = requests.post(API_URL, json=data, timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        # 检查响应
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"✅ 测试通过! 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
                return True
            except json.JSONDecodeError:
                print(f"❌ 响应不是有效的JSON: {response.text}")
                return False
        else:
            print(f"❌ 测试失败! 状态码: {response.status_code}, 响应: {response.text}")
            return False
    finally:
        # 清理文件
        cleanup_test_files([file1_path, file2_path])

def run_all_tests():
    """运行所有测试"""
    print("\n======= 报告对比API综合测试 =======")
    print(f"测试API: {API_URL}")
    print(f"上传目录: {UPLOADS_DIR}")
    
    # 确保uploads目录存在
    os.makedirs(UPLOADS_DIR, exist_ok=True)
    
    # 运行测试
    tests = [
        ("JSON请求 - 文件存在", test_json_with_existing_files),
        ("JSON请求 - 文件不存在", test_json_with_nonexistent_files),
        ("JSON请求 - 缺少参数", test_json_with_missing_parameters),
        ("FormData模拟 - JSON方式", test_formdata_via_json)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🔄 执行测试: {name}")
        if test_func():
            passed += 1
    
    # 显示总结
    print("\n======= 测试结果总结 =======")
    print(f"通过测试: {passed}/{total}")
    print(f"成功率: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 所有测试都通过了！")
    else:
        print("\n❌ 有测试未通过，请检查问题。")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n测试已中断")
    except Exception as e:
        print(f"测试执行错误: {e}")
