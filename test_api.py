import json
import os
import sys

# 添加当前目录到系统路径，确保能导入grade_report函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 尝试导入grade_report函数，如果不存在则创建模拟函数
try:
    from app import grade_report
except ImportError:
    # 创建一个模拟的grade_report函数
    def grade_report(content, topic=''):
        print(f"模拟调用grade_report，内容长度: {len(content)}, 主题: {topic}")
        return {
            'total_score': 85.5,
            'level': {'level': '良好'},
            'dimension_scores': [
                {'name': '内容完整性', 'score': 90},
                {'name': '逻辑性', 'score': 85},
                {'name': '创新性', 'score': 80},
                {'name': '表达清晰度', 'score': 88}
            ],
            'suggestions': [
                '【内容完整性】报告内容较为全面，但可以补充更多具体案例',
                '【逻辑性】整体结构清晰，但部分段落过渡可以更自然',
                '【创新性】有一定创新点，但可以进一步挖掘'
            ],
            'api_status': 'success'
        }

# 模拟API处理函数
def mock_api_evaluation_report(file_path, topic='', analysis_type='standard'):
    print(f"开始处理文件: {file_path}")
    
    # 确保文件路径是绝对路径或相对于当前目录的路径
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)
    
    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return {"error": f"文件不存在: {file_path}"}, False
    
    # 读取文件内容
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_content = f.read()
    except Exception as e:
        return {"error": f"读取文件失败: {str(e)}"}, False
    
    # 确保有文件内容
    if not file_content:
        return {"error": "文件内容为空"}, False
    
    print(f"文件读取成功，内容长度: {len(file_content)}")
    
    # 调用grade_report函数
    try:
        api_result = grade_report(file_content, topic)
        
        # 构建响应数据
        response_data = {
            "status": "success",
            "message": "文件已成功处理",
            "file_path": file_path,
            "analysis_type": analysis_type,
            "report_data": api_result
        }
        
        return response_data, True
    except Exception as e:
        return {"error": str(e)}, False

# 测试函数
def run_test():
    print("===== 开始测试API功能 =====")
    
    # 测试文件路径
    test_files = [
        "test_report_1_result.txt",
        "test_report_2_result.txt", 
        "test_report_3_result.txt"
    ]
    
    # 检查测试文件是否存在
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"测试文件存在: {test_file}")
            # 调用模拟API处理函数
            result, success = mock_api_evaluation_report(test_file)
            
            # 打印结果
            print(f"\n处理结果: {'成功' if success else '失败'}")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            break
    else:
        print("没有找到测试文件")
    
    print("\n===== 测试完成 =====")

# 执行测试
if __name__ == "__main__":
    run_test()
