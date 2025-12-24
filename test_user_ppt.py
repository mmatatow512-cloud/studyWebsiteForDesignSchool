#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用户上传的PPT转视频功能
"""

import os
import sys
import tempfile
import shutil

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath('.'))

# 导入PPT转视频模块
import ppt2video

def test_user_ppt_conversion():
    """测试用户PPT转视频功能"""
    print("=" * 60)
    print("测试用户PPT转视频功能")
    print("=" * 60)
    
    # 要求用户输入PPT文件路径
    ppt_path = input("请输入您的PPT文件路径: ").strip()
    
    # 验证PPT文件是否存在
    if not os.path.exists(ppt_path):
        print(f"错误: PPT文件不存在 - {ppt_path}")
        return False
    
    # 验证文件类型
    if not ppt_path.endswith(('.pptx', '.ppt')):
        print(f"错误: 不支持的文件格式 - {ppt_path}")
        print("请确保文件是PPT或PPTX格式")
        return False
    
    print(f"\nPPT文件信息:")
    print(f"  路径: {ppt_path}")
    print(f"  大小: {os.path.getsize(ppt_path)} 字节")
    
    # 创建临时输出目录
    output_dir = tempfile.mkdtemp(prefix="ppt2video_test_")
    output_path = os.path.join(output_dir, "output_video.mp4")
    
    print(f"\n输出设置:")
    print(f"  输出目录: {output_dir}")
    print(f"  视频路径: {output_path}")
    
    try:
        # 执行PPT转视频
        print(f"\n开始PPT转视频处理...")
        success = ppt2video.convert_presentation_to_video(ppt_path, output_path)
        
        if success:
            print(f"\n✅ 转换成功！")
            print(f"视频文件路径: {output_path}")
            print(f"视频文件大小: {os.path.getsize(output_path)} 字节")
            print("\n您可以在文件资源管理器中打开视频文件查看效果。")
            return True
        else:
            print(f"\n❌ 转换失败！")
            return False
            
    except Exception as e:
        print(f"\n❌ 转换过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 询问是否保留临时文件
        keep_files = input("\n是否保留临时文件? (y/n): ").strip().lower()
        if keep_files != 'y':
            try:
                shutil.rmtree(output_dir)
                print("临时文件已清理。")
            except Exception as e:
                print(f"清理临时文件失败: {e}")

if __name__ == "__main__":
    test_user_ppt_conversion()