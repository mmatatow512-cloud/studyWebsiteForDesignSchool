#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Content-Type修复验证脚本

此脚本用于测试/api/evaluation/report端点的Content-Type处理逻辑，
分别使用正确和错误的Content-Type头进行请求，并显示结果对比。
"""

import requests
import json
import sys
import time

# API端点URL
API_URL = "http://localhost:5001/api/evaluation/report"

# 测试数据
test_data = {
    "file_path": "d:\\9\\demo\\project\\examples\\测试文档.docx",
    "topic": "这是一个测试主题",
    "analysis_type": "standard"
}


def print_separator(title):
    """打印分隔符和标题"""
    print("\n" + "=" * 60)
    print(f"{title}")
    print("=" * 60)


def test_without_content_type():
    """测试不设置Content-Type头的情况（应该失败）"""
    print_separator("测试1: 不设置Content-Type头")
    
    try:
        # 不设置Content-Type头
        response = requests.post(
            API_URL,
            data=json.dumps(test_data)  # 只序列化数据，但不设置Content-Type
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        try:
            json_response = response.json()
            print(f"响应内容: {json.dumps(json_response, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"无法解析JSON响应: {str(e)}")
            print(f"原始响应: {response.text}")
            
        return response.status_code == 415  # 415表示Unsupported Media Type
        
    except Exception as e:
        print(f"请求发送失败: {str(e)}")
        return False


def test_with_incorrect_content_type():
    """测试设置错误的Content-Type头的情况（应该失败）"""
    print_separator("测试2: 设置错误的Content-Type头")
    
    try:
        # 设置错误的Content-Type头
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=json.dumps(test_data)
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        try:
            json_response = response.json()
            print(f"响应内容: {json.dumps(json_response, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"无法解析JSON响应: {str(e)}")
            print(f"原始响应: {response.text}")
            
        return response.status_code == 415
        
    except Exception as e:
        print(f"请求发送失败: {str(e)}")
        return False


def test_with_correct_content_type():
    """测试设置正确的Content-Type头的情况（应该成功）"""
    print_separator("测试3: 设置正确的Content-Type头")
    
    try:
        # 设置正确的Content-Type头
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},  # 正确设置Content-Type
            json=test_data  # 使用requests的json参数自动序列化并设置Content-Type
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        try:
            json_response = response.json()
            print(f"响应内容: {json.dumps(json_response, ensure_ascii=False, indent=2)}")
            return response.status_code == 200 or response.status_code == 201
        except Exception as e:
            print(f"无法解析JSON响应: {str(e)}")
            print(f"原始响应: {response.text}")
            # 即使返回其他状态码（如404文件不存在），只要不是415，也算Content-Type检查通过
            return response.status_code != 415
            
    except Exception as e:
        print(f"请求发送失败: {str(e)}")
        return False


def test_with_requests_json_param():
    """测试使用requests的json参数（自动设置Content-Type）"""
    print_separator("测试4: 使用requests库的json参数（自动设置Content-Type）")
    
    try:
        # 使用json参数（requests库会自动设置Content-Type为application/json）
        response = requests.post(
            API_URL,
            json=test_data  # 关键点：使用json参数而非data参数
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        try:
            json_response = response.json()
            print(f"响应内容: {json.dumps(json_response, ensure_ascii=False, indent=2)}")
        except Exception as e:
            print(f"无法解析JSON响应: {str(e)}")
            print(f"原始响应: {response.text}")
            
        # 只要不是415错误，就表示Content-Type设置成功
        return response.status_code != 415
        
    except Exception as e:
        print(f"请求发送失败: {str(e)}")
        return False


def main():
    """主测试函数"""
    print("\n" + "*" * 60)
    print("Content-Type修复验证工具")
    print("*" * 60)
    print("本工具将测试/api/evaluation/report端点的Content-Type处理逻辑")
    
    # 检查服务器是否运行
    try:
        response = requests.get("http://localhost:5001")
        print(f"\n服务器状态: 运行中")
    except Exception as e:
        print(f"\n错误: 无法连接到服务器 (http://localhost:5001)")
        print(f"请先启动Flask服务器，然后再运行此测试脚本。")
        print(f"启动命令: python app.py")
        return False
    
    # 运行所有测试
    tests = [
        ("不设置Content-Type", test_without_content_type),
        ("设置错误Content-Type", test_with_incorrect_content_type),
        ("设置正确Content-Type", test_with_correct_content_type),
        ("使用requests.json参数", test_with_requests_json_param)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(1)  # 添加小延迟，避免请求过于频繁
    
    # 显示总结
    print_separator("测试总结")
    
    all_passed = True
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！Content-Type修复验证成功。")
        print("\n结论：")
        print("1. 当不设置Content-Type时，服务器正确返回415错误")
        print("2. 当设置错误的Content-Type时，服务器正确返回415错误")
        print("3. 当设置正确的Content-Type时，服务器接受请求")
    else:
        print("❌ 部分测试未通过，可能需要进一步检查修复。")
        
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
