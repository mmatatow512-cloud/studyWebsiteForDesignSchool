# 先测试基本导入
print('开始导入模块...')
try:
    import sys
    import os
    import shutil
    import tempfile
    import traceback
    print(f'基本模块导入成功: {sys.version}')
    
    # 导入ppt2video模块
    try:
        from ppt2video import ConverterLogic
        print('ppt2video模块导入成功')
    except Exception as e:
        print(f'导入ppt2video模块失败: {e}')
        print(traceback.format_exc())
        sys.exit(1)
except Exception as e:
    print(f'初始化导入失败: {e}')
    print(traceback.format_exc())
    import sys
    sys.exit(1)

# 测试完整转换流程
def test_full_conversion():
    # 创建转换器实例
    logic = ConverterLogic(print)
    
    # 检查测试PPT是否存在
    ppt_path = 'test_ppt.pptx'
    if not os.path.exists(ppt_path):
        print(f'[错误] 测试PPT文件不存在: {ppt_path}')
        return False
    
    # 设置输出路径
    video_path = 'final_test.mp4'
    
    # 创建临时目录
    temp_img = tempfile.mkdtemp(prefix="ppt2video_img_")
    temp_aud = tempfile.mkdtemp(prefix="ppt2video_aud_")
    
    print(f'=== 开始完整转换测试 ===')
    print(f'PPT路径: {ppt_path}')
    print(f'输出路径: {video_path}')
    print(f'临时图片目录: {temp_img}')
    print(f'临时音频目录: {temp_aud}')
    
    try:
        # 1. 导出图片
        print('\n第1步：导出幻灯片图片')
        images = logic.export_images(ppt_path, temp_img)
        if not images:
            print('[错误] 图片导出失败')
            return False
        print(f'[成功] 导出 {len(images)} 张幻灯片图片')
        
        # 2. 提取文本
        print('\n第2步：提取PPT文字内容')
        scripts = logic.extract_text(ppt_path)
        print(f'[成功] 提取 {len(scripts)} 页文字内容')
        
        # 3. 生成语音
        print('\n第3步：生成语音文件')
        # 使用MoviePy生成音频，不需要系统语音
        voice_id = None
        audios = logic.generate_audio(scripts, temp_aud, voice_id, 170)
        print(f'[成功] 生成 {len(audios)} 个音频文件')
        
        # 4. 合成视频
        print('\n第4步：合成视频文件')
        success = logic.make_video(images, audios, video_path, False, scripts)
        
        if success:
            print(f'\n=== 转换成功！ ===')
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                print(f'视频文件大小: {file_size} 字节 ({file_size / 1024:.2f} KB)')
                print(f'视频文件已保存到: {os.path.abspath(video_path)}')
                return True
            else:
                print(f'[错误] 转换返回成功，但视频文件不存在')
                return False
        else:
            print(f'\n[错误] 转换失败')
            return False
            
    except Exception as e:
        print(f'\n[错误] 转换过程中发生异常: {e}')
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时目录
        print('\n=== 清理临时文件 ===')
        try:
            if os.path.exists(temp_img):
                shutil.rmtree(temp_img)
                print(f'已清理临时图片目录: {temp_img}')
            if os.path.exists(temp_aud):
                shutil.rmtree(temp_aud)
                print(f'已清理临时音频目录: {temp_aud}')
        except Exception as e:
            print(f'清理临时文件失败: {e}')

if __name__ == '__main__':
    test_full_conversion()
