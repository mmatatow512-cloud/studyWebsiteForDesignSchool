#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试音频与幻灯片的同步问题
确保幻灯片时长与音频时长保持一致
"""

import os
import sys
import logging
import tempfile
from ppt2video import PPTtoVideoConverter

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_audio_slide_sync():
    """
    测试音频与幻灯片的同步
    """
    try:
        # 确保有PPT文件可测试
        if len(sys.argv) < 2:
            logger.error("用法: python test_audio_sync.py <PPT文件路径>")
            return False
        
        ppt_path = sys.argv[1]
        if not os.path.exists(ppt_path):
            logger.error(f"PPT文件不存在: {ppt_path}")
            return False
            
        # 创建临时目录用于输出
        temp_dir = tempfile.mkdtemp()
        output_video = os.path.join(temp_dir, "test_sync_video.mp4")
        
        logger.info(f"测试开始: {ppt_path} -> {output_video}")
        logger.info(f"临时目录: {temp_dir}")
        
        # 直接调用转换函数
        from ppt2video import convert_presentation_to_video
        success = convert_presentation_to_video(ppt_path, output_video)
        
        if success:
            logger.info(f"转换成功！视频路径: {output_video}")
            logger.info(f"视频大小: {os.path.getsize(output_video)/1024/1024:.2f} MB")
            
            # 使用ffprobe检查视频信息
            try:
                import subprocess
                logger.info("\n使用ffprobe检查视频详细信息:")
                # 检查视频总时长
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', output_video],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    total_duration = float(result.stdout.strip())
                    logger.info(f"视频总时长: {total_duration:.2f} 秒")
                
                # 检查音频是否存在
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=duration', '-of', 'csv=p=0', output_video],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0 and result.stdout.strip():
                    audio_duration = float(result.stdout.strip())
                    logger.info(f"音频总时长: {audio_duration:.2f} 秒")
                    
                    if abs(total_duration - audio_duration) < 0.5:
                        logger.info("✓ 视频总时长与音频总时长基本一致")
                    else:
                        logger.warning(f"⚠ 视频总时长与音频总时长不一致: 视频 {total_duration:.2f} 秒, 音频 {audio_duration:.2f} 秒")
                
            except Exception as e:
                logger.error(f"检查视频信息失败: {e}")
                
        else:
            logger.error("转换失败！")
            return False
            
        return success
        
    except Exception as e:
        logger.error(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # 清理临时文件（可选，用户可以手动删除）
        logger.info("\n测试完成！")

if __name__ == "__main__":
    test_audio_slide_sync()