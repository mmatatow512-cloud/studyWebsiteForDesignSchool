#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import sys
import tempfile
import shutil
import time

def test_convert_ppt():
    """
    测试PPT转视频功能
    """
    # 设置服务器URL
    base_url = 'http://127.0.0.1:5001'
    convert_url = f'{base_url}/convert_ppt_to_video'
    login_url = f'{base_url}/login'
    register_url = f'{base_url}/register'
    
    # 测试用户信息
    test_user = {
        'username': 'test_user',
        'password': 'test_password',
        'confirm_password': 'test_password',
        'role': 'student',
        'student_id': 'test123'
    }
    
    # 创建会话对象
    session = requests.Session()
    
    # 1. 注册测试用户
    print("=== 注册测试用户 ===")
    try:
        register_response = session.post(register_url, data=test_user, timeout=10)
        print(f"[信息] 注册响应状态码: {register_response.status_code}")
        print(f"[信息] 注册响应URL: {register_response.url}")
    except Exception as e:
        print(f"[错误] 注册失败: {e}")
        # 注册失败可能是因为用户已存在，继续尝试登录
    
    # 2. 登录测试用户
    print("\n=== 登录测试用户 ===")
    try:
        login_data = {
            'username': test_user['username'],
            'password': test_user['password']
        }
        login_response = session.post(login_url, data=login_data, allow_redirects=True, timeout=10)
        print(f"[信息] 登录响应状态码: {login_response.status_code}")
        print(f"[信息] 登录响应URL: {login_response.url}")
        
        # 检查是否登录成功
        if 'dashboard' in login_response.url:
            print("[成功] 登录成功")
        else:
            print("[错误] 登录失败")
            print(f"[信息] 响应内容: {login_response.text[:500]}...")
            return False
    except Exception as e:
        print(f"[错误] 登录失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 找到测试用的PPT文件
    ppt_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.lower().endswith(('.pptx', '.ppt')):
                ppt_files.append(os.path.join(root, file))
                if len(ppt_files) >= 2:  # 最多找2个文件测试
                    break
    
    if not ppt_files:
        print("[错误] 未找到测试用的PPT文件")
        return False
    
    print(f"[信息] 找到 {len(ppt_files)} 个PPT文件用于测试:")
    for i, ppt_file in enumerate(ppt_files):
        print(f"  {i+1}. {ppt_file}")
    
    # 测试每个PPT文件
    success_count = 0
    for i, ppt_file in enumerate(ppt_files):
        print(f"\n=== 测试文件 {i+1}/{len(ppt_files)}: {os.path.basename(ppt_file)} ===")
        
        try:
            # 检查文件大小
            file_size = os.path.getsize(ppt_file)
            print(f"[信息] 文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)")
            
            # 准备请求文件
            with open(ppt_file, 'rb') as f:
                files = {'ppt_file': (os.path.basename(ppt_file), f)}
                
                # 发送请求
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                print(f"[信息] 发送请求到 {convert_url}...")
                start_time = time.time()
                
                # 使用登录后的会话发送请求
                response = session.post(
                    convert_url,
                    files=files,
                    headers=headers,
                    stream=True,  # 使用流式响应
                    timeout=600  # 10分钟超时
                )
                
                end_time = time.time()
                response_time = end_time - start_time
                print(f"[信息] 请求耗时: {response_time:.2f} 秒")
                print(f"[信息] 响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    # 检查响应头
                    print(f"[信息] 响应头:")
                    for key, value in response.headers.items():
                        if key.lower() in ['content-type', 'content-disposition', 'content-length', 'access-control-allow-origin']:
                            print(f"  {key}: {value}")
                    
                    # 保存响应内容
                    content_disposition = response.headers.get('Content-Disposition', '')
                    filename = 'output.mp4'
                    if 'filename=' in content_disposition:
                        filename = content_disposition.split('filename=')[1].strip('"')
                    
                    output_path = os.path.join(tempfile.gettempdir(), filename)
                    print(f"[信息] 保存响应内容到: {output_path}")
                    
                    # 逐块保存文件
                    total_size = 0
                    with open(output_path, 'wb') as out_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                out_file.write(chunk)
                                total_size += len(chunk)
                                # 每接收1MB打印一次进度
                                if total_size % (1024 * 1024) < 8192:
                                    print(f"[信息] 已接收: {total_size / (1024 * 1024):.2f} MB")
                    
                    print(f"[信息] 文件保存完成，大小: {total_size} 字节")
                    
                    # 检查是否是JSON响应
                    if total_size < 1000 and response.headers.get('Content-Type') == 'application/json':
                        with open(output_path, 'r', encoding='utf-8') as f:
                            json_content = f.read()
                        print(f"[警告] 服务器返回JSON而不是视频文件: {json_content}")
                        print(f"[错误] PPT转视频测试失败")
                    else:
                        print(f"[成功] PPT转视频测试通过")
                        success_count += 1
                    
                    # 清理临时文件
                    os.unlink(output_path)
                    print(f"[信息] 临时文件已清理: {output_path}")
                else:
                    print(f"[错误] 请求失败，状态码: {response.status_code}")
                    print(f"[错误] 响应内容: {response.text[:500]}...")  # 只显示前500个字符
                    
        except requests.exceptions.Timeout:
            print(f"[错误] 请求超时")
        except requests.exceptions.ConnectionError as e:
            print(f"[错误] 连接错误: {e}")
            print(f"[提示] 可能的原因: 服务器超时、连接被重置或网络问题")
        except Exception as e:
            print(f"[错误] 测试失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n=== 测试总结 ===")
    print(f"总测试文件数: {len(ppt_files)}")
    print(f"成功数: {success_count}")
    print(f"失败数: {len(ppt_files) - success_count}")
    
    return success_count > 0

if __name__ == '__main__':
    success = test_convert_ppt()
    sys.exit(0 if success else 1)