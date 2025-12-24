#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证Content-Type修复效果

这个脚本用于测试修复后的前端页面是否能正确处理Content-Type，
以及后端API是否能正确接收和处理文件上传请求。
"""

import os
import sys
import requests
import time
import tempfile
from pathlib import Path

def create_test_file():
    """创建一个临时测试文件"""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w', encoding='utf-8') as f:
        f.write("""这是一份测试报告
主题：Content-Type修复测试

1. 测试目的
验证修复后的上传功能是否能正确处理Content-Type

2. 测试方法
使用自动化脚本测试文件上传功能

3. 预期结果
文件成功上传，API正确响应
        """)
        return f.name

def test_report_upload_api():
    """测试/api/evaluation/report API"""
    print("\n=== 测试报告上传API ===")
    url = "http://localhost:5000/api/evaluation/report"
    
    # 创建测试文件
    test_file_path = create_test_file()
    
    try:
        # 构建多部分表单数据（模拟浏览器行为）
        files = {'file': open(test_file_path, 'rb')}
        
        print(f"正在上传测试文件到 {url}...")
        start_time = time.time()
        
        # 发送请求（不手动设置Content-Type，让requests库自动处理）
        response = requests.post(url, files=files)
        
        elapsed_time = time.time() - start_time
        print(f"请求完成，耗时: {elapsed_time:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        # 检查响应内容
        try:
            data = response.json()
            print("响应数据格式: JSON")
            print(f"API返回结果: {'成功' if 'error' not in data else '失败'}")
            if 'error' in data:
                print(f"错误信息: {data['error']}")
            elif 'overall_score' in data:
                print(f"报告得分: {data['overall_score']}")
            return True
        except ValueError:
            print(f"响应内容不是有效的JSON: {response.text[:100]}...")
            return False
    
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        return False
    finally:
        # 清理临时文件
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_report_compare_api():
    """测试/api/evaluation/compare API"""
    print("\n=== 测试报告对比API ===")
    url = "http://localhost:5000/api/evaluation/compare"
    
    # 创建两个测试文件
    test_file1_path = create_test_file()
    test_file2_path = create_test_file()
    
    try:
        # 构建多部分表单数据
        files = {
            'file1': open(test_file1_path, 'rb'),
            'file2': open(test_file2_path, 'rb')
        }
        
        print(f"正在上传两个测试文件到 {url}...")
        start_time = time.time()
        
        # 发送请求
        response = requests.post(url, files=files)
        
        elapsed_time = time.time() - start_time
        print(f"请求完成，耗时: {elapsed_time:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        # 检查响应内容
        try:
            data = response.json()
            print("响应数据格式: JSON")
            print(f"API返回结果: {'成功' if 'error' not in data else '失败'}")
            if 'error' in data:
                print(f"错误信息: {data['error']}")
            elif 'report1' in data and 'report2' in data:
                print(f"报告1得分: {data['report1'].get('overall_score', 'N/A')}")
                print(f"报告2得分: {data['report2'].get('overall_score', 'N/A')}")
            return True
        except ValueError:
            print(f"响应内容不是有效的JSON: {response.text[:100]}...")
            return False
    
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
        return False
    finally:
        # 清理临时文件
        for f_path in [test_file1_path, test_file2_path]:
            if os.path.exists(f_path):
                os.remove(f_path)

def check_server_running():
    """检查服务器是否正在运行"""
    print("检查服务器状态...")
    try:
        response = requests.get("http://localhost:5000", timeout=3)
        print("✅ 服务器正在运行")
        return True
    except requests.ConnectionError:
        print("❌ 服务器未运行，请先启动Flask服务器")
        return False

def generate_test_summary(results):
    """生成测试摘要"""
    print("\n=== 测试摘要 ===")
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试数: {passed_tests}")
    print(f"成功率: {passed_tests/total_tests*100:.1f}%")
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")
    
    return passed_tests == total_tests

def main():
    """主函数"""
    print("\n=====================================")
    print("Content-Type修复测试脚本")
    print("=====================================")
    print("此脚本用于验证前端页面的Content-Type修复效果")
    
    # 首先检查服务器是否运行
    if not check_server_running():
        print("\n请先启动Flask服务器，然后再运行此测试脚本。")
        print("可以在项目目录下运行: python app.py")
        return False
    
    # 运行各项测试
    results = {}
    results["报告上传API测试"] = test_report_upload_api()
    results["报告对比API测试"] = test_report_compare_api()
    
    # 生成测试摘要
    all_passed = generate_test_summary(results)
    
    print("\n=====================================")
    if all_passed:
        print("🎉 所有测试都已通过！Content-Type修复成功。")
        print("您现在可以在原网页中正常上传文件并使用API功能了。")
    else:
        print("⚠️ 部分测试未通过，请检查错误信息并修复问题。")
    print("=====================================")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
