#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单调用测试脚本，直接使用ConverterLogic类进行测试
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# 确保在正确的目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 导入ConverterLogic类
try:
    from ppt2video import ConverterLogic
    print("成功导入ConverterLogic类")
except Exception as e:
    print(f"导入失败: {e}")
    sys.exit(1)

# 简单的日志函数
def simple_log(message):
    with open('simple_call_test.log', 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")
    print(message, flush=True)

# 清空旧日志
open('simple_call_test.log', 'w').close()

# 测试主函数
def main():
    simple_log("=== 开始简单调用测试 ===")
    simple_log(f"Python版本: {sys.version}")
    simple_log(f"当前时间: {datetime.now()}")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix="ppt2video_test_")
    simple_log(f"临时目录: {temp_dir}")
    
    try:
        # 准备测试数据
        test_ppt = "test_ppt.pptx"
        if not os.path.exists(test_ppt):
            simple_log(f"错误: 测试PPT不存在: {test_ppt}")
            return False
        
        output_video = os.path.join(temp_dir, "output_test.mp4")
        
        # 创建ConverterLogic实例
        def log_func(message):
            simple_log(f"[Converter] {message}")
        
        converter = ConverterLogic(log_func)
        
        # 测试提取文本
        simple_log("\n1. 测试提取文本")
        scripts = converter.extract_text(test_ppt)
        simple_log(f"提取到 {len(scripts)} 页文本")
        
        # 测试导出图片
        simple_log("\n2. 测试导出图片")
        images = converter.export_images(test_ppt, temp_dir)
        simple_log(f"导出了 {len(images)} 张图片")
        for img in images:
            if os.path.exists(img):
                simple_log(f"  - {os.path.basename(img)}: {os.path.getsize(img)} 字节")
        
        # 测试生成音频
        simple_log("\n3. 测试生成音频")
        audios = converter.generate_audio(scripts, temp_dir, "", 170)
        simple_log(f"生成了 {len(audios)} 个音频文件")
        for aud in audios:
            if os.path.exists(aud):
                simple_log(f"  - {os.path.basename(aud)}: {os.path.getsize(aud)} 字节")
        
        # 测试生成视频
        simple_log("\n4. 测试生成视频")
        success = converter.make_video(images, audios, output_video, False, scripts)
        
        # 检查结果
        if success and os.path.exists(output_video):
            video_size = os.path.getsize(output_video)
            simple_log(f"\n✅ 视频生成成功！")
            simple_log(f"路径: {output_video}")
            simple_log(f"大小: {video_size} 字节 ({video_size / 1024:.2f} KB)")
            return True
        else:
            simple_log(f"\n❌ 视频生成失败")
            if os.path.exists(output_video):
                simple_log(f"但文件存在，大小: {os.path.getsize(output_video)} 字节")
            return False
            
    except Exception as e:
        simple_log(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir)
            simple_log(f"清理临时目录: {temp_dir}")
        except:
            pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)