#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
import json

def parse_html_questions(html_content):
    """
    解析HTML格式的题库文件，提取题目数据
    :param html_content: HTML文件内容
    :return: 题目数据列表
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    questions = []
    
    # 提取所有段落内容
    elements = soup.find_all(['p', 'h4'])
    
    current_section = ""
    
    # 使用索引遍历元素，方便处理后续元素
    i = 0
    while i < len(elements):
        element = elements[i]
        text = element.get_text().strip()
        if not text:
            i += 1
            continue
        
        # 检查是否是题目类型标题
        if '三、判断题' in text or '判断题' in text:
            current_section = 'judge'
            print(f"切换到判断题 section: {text}")
            i += 1
            continue
        elif '单选题' in text:
            current_section = 'single'
            print(f"切换到单选题 section: {text}")
            i += 1
            continue
        elif '多选题' in text or '二、多选题' in text:
            current_section = 'multiple'
            print(f"切换到多选题 section: {text}")
            i += 1
            continue
        elif '简答题' in text or '四、' in text:
            current_section = 'short'
            print(f"切换到简答题 section: {text}")
            i += 1
            continue
        
        # 跳过分隔线和其他非题目内容
        if '<hr' in str(element) or '---' in text or '_____' in text:
            i += 1
            continue
        
        # 匹配题目格式 - 更精确的正则
        # 处理不同格式的题目编号
        # 示例1：17. 材料与质感的研究对设计的意义在于？（ABCD）A. 直接影响产品的功能...
        # 示例2：1. 在平面构成中，点只有相对意义...（√）
        # 匹配编号格式：数字+点+空格
        if re.match(r'^\d+\.', text):
            # 提取题目编号和剩余内容
            number_part, rest_text = text.split('.', 1)
            rest_text = rest_text.strip()
            
            # 初始化变量
            question_text = ""
            answer = ""
            options = {}
            
            # 检查是否包含答案（选择题）
            # 处理不同格式的答案标记：（A）或(A)
            answer_match = re.search(r'[（(]([A-Z]+)[）)]', rest_text)
            if answer_match:
                answer = answer_match.group(1)
                # 提取题干（答案之前的部分）
                question_text = rest_text[:answer_match.start()].strip()
                # 提取所有选项文本（答案标记之后的所有内容）
                all_text_after_answer = rest_text[answer_match.end():].strip()
                
                # 合并后续元素的文本
                i += 1  # 移动到下一个元素
                while i < len(elements):
                    next_element = elements[i]
                    next_text = next_element.get_text().strip()
                    if next_text and not re.match(r'^\d+\.', next_text) and not any(keyword in next_text for keyword in ['一、', '二、', '三、', '四、', '单选题', '多选题', '判断题', '简答题']):
                        all_text_after_answer += next_text
                        i += 1
                    else:
                        break
                
                # 专门处理选项紧跟在答案后面的情况
                # 匹配选项：A.内容B.内容C.内容D.内容
                option_pattern = r'([A-Z])\.(.*?)(?=[A-Z]\.|$)'
                option_matches = re.finditer(option_pattern, all_text_after_answer)
                for match in option_matches:
                    option_key = match.group(1)
                    option_value = match.group(2).strip()
                    options[option_key] = option_value
                
                # 如果没有匹配到选项，尝试另一种格式：A. 内容 B. 内容
                if not options:
                    option_pattern = r'([A-Z])\.\s*(.*?)(?=\s*[A-Z]\.\s*|$)'
                    option_matches = re.finditer(option_pattern, all_text_after_answer)
                    for match in option_matches:
                        option_key = match.group(1)
                        option_value = match.group(2).strip()
                        options[option_key] = option_value
                
                # 根据答案长度确定题型
                if len(answer) > 1:
                    current_section = 'multiple'
                else:
                    current_section = 'single'
            
            # 检查是否是判断题（包含√或×）
            elif '（√）' in rest_text or '（×）' in rest_text or '(√)' in rest_text or '(×)' in rest_text:
                current_section = 'judge'
                if '（√）' in rest_text or '(√)' in rest_text:
                    answer = 'True'
                    question_text = rest_text.replace('（√）', '').replace('(√)', '').strip()
                else:
                    answer = 'False'
                    question_text = rest_text.replace('（×）', '').replace('(×)', '').strip()
                i += 1  # 移动到下一个元素
            
            # 其他情况（可能是没有答案的题目或简答题）
            else:
                question_text = rest_text
                i += 1  # 移动到下一个元素
            
            # 只添加有效的题目
            if question_text:
                # 创建题目数据
                question_data = {
                    'knowledge_point': '设计基础知识',  # 默认知识点
                    'difficulty': '中等',  # 默认难度
                    'qtype': current_section if current_section else 'single',  # 默认为单选题
                    'question_text': question_text,
                    'options': json.dumps(options) if options else '{}',
                    'answer': answer,
                    'analysis': '',  # 默认解析
                    'source': 'html_upload'
                }
                
                questions.append(question_data)
                print(f"解析到题目: {question_data['qtype']} - {question_data['question_text'][:50]}... 答案: {answer}")
        else:
            i += 1  # 移动到下一个元素
    
    return questions

# 测试代码
if __name__ == "__main__":
    # 读取HTML文件
    with open('题库.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 解析题目
    questions = parse_html_questions(html_content)
    
    # 打印解析结果
    print(f"共解析出 {len(questions)} 道题目")
    for i, q in enumerate(questions[:10]):  # 只打印前10道题
        print(f"\n题目 {i+1}:")
        print(f"类型: {q['qtype']}")
        print(f"题干: {q['question_text']}")
        print(f"选项: {q['options']}")
        print(f"答案: {q['answer']}")
