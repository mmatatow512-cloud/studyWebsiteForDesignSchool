#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单元视频更新功能
"""

import requests
import os
import sys
import tempfile

# 服务器地址
BASE_URL = 'http://127.0.0.1:5001'

# 登录测试
login_data = {
    'username': 'testteacher',
    'password': 'password123'
}

# 创建一个会话
session = requests.Session()

# 登录
def login():
    response = session.post(f'{BASE_URL}/login', data=login_data)
    if response.status_code == 200:
        print("登录成功")
        return True
    else:
        print(f"登录失败: {response.status_code}")
        return False

# 获取课程列表
def get_courses():
    response = session.get(f'{BASE_URL}/teacher_edit_course')
    if response.status_code == 200:
        print("获取课程列表成功")
        return response.text
    else:
        print(f"获取课程列表失败: {response.status_code}")
        return None

# 测试单元视频更新
def test_unit_video_update(course_id, unit_id):
    # 创建一个临时视频文件
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
        temp_file.write(b'\x00\x01\x02\x03')  # 简单的视频文件头
        temp_file_path = temp_file.name
    
    try:
        # 准备表单数据
        data = {
            f'unit_title_{unit_id}': '测试单元',
            f'unit_order_{unit_id}': '1'
        }
        
        # 准备文件
        files = {
            f'unit_file_{unit_id}': open(temp_file_path, 'rb')
        }
        
        # 发送更新请求
        response = session.post(f'{BASE_URL}/teacher_edit_course/{course_id}', data=data, files=files)
        
        if response.status_code == 200:
            print("单元视频更新成功")
            return True
        else:
            print(f"单元视频更新失败: {response.status_code}")
            print(f"响应内容: {response.text[:500]}...")  # 只显示前500个字符
            return False
    finally:
        # 清理临时文件
        os.unlink(temp_file_path)

if __name__ == '__main__':
    if login():
        courses = get_courses()
        if courses:
            print("请从课程列表中选择要测试的课程ID和单元ID")
            print("例如: python test_unit_update.py 1 1")
            
            if len(sys.argv) == 3:
                course_id = sys.argv[1]
                unit_id = sys.argv[2]
                test_unit_video_update(course_id, unit_id)
            else:
                print("请提供课程ID和单元ID作为命令行参数")
