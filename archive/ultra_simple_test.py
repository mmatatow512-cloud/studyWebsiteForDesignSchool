# 超简单测试脚本
import os
import sys

# 添加项目目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'project'))

import ppt2video

# 测试PPT路径
test_ppt = "project/test_ppt.pptx"
# 输出路径
output_path = "test_output.mp4"

print("=== 超简单测试 ===")
print(f"测试PPT: {test_ppt}")
print(f"是否存在: {os.path.exists(test_ppt)}")

# 执行测试
print("\n开始测试...")
try:
    # 调用函数
    result = ppt2video.convert_presentation_to_video(test_ppt, output_path)
    print(f"函数返回: {result}")
    
    # 检查输出文件
    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"输出文件大小: {size} 字节")
        
        # 清理
        os.remove(output_path)
        print("已清理输出文件")
        
        # 判断是否是测试视频
        if size < 10240:  # 小于10KB
            print("❌ 测试失败: 生成了测试视频")
        else:
            print("✅ 测试成功: 生成了正常视频")
    else:
        print("✅ 测试成功: 没有生成文件（可能抛出了异常）")
        
except Exception as e:
    print(f"异常: {e}")
    print("✅ 测试成功: 抛出异常而不是生成测试视频")
    
    # 清理
    if os.path.exists(output_path):
        os.remove(output_path)
        print("已清理输出文件")