import re

# 优秀范例库
EXCELLENT_EXAMPLES = [
    {
        'id': 1,
        'title': 'Python编程学习报告',
        'content': '''# Python编程学习报告\n\n## 一、引言\nPython是一种高级编程语言，具有简洁易读的语法特点，广泛应用于数据分析、人工智能、Web开发等领域。本文将总结Python编程学习的主要内容和心得体会。\n\n## 二、核心知识点\n\n### 2.1 变量与数据类型\nPython支持多种数据类型，包括整数、浮点数、字符串、列表、元组、字典等。变量的定义非常简单，不需要声明类型，直接赋值即可。\n\n```python\n# 变量定义示例\nname = "张三"\nage = 20\nscores = [85, 90, 95]\n```\n\n### 2.2 控制流语句\nPython提供了if-elif-else条件判断语句和for、while循环语句，用于控制程序的执行流程。\n\n### 2.3 函数与模块\n函数是一段可重复使用的代码块，通过def关键字定义。模块是Python文件，可以通过import语句导入和使用。\n\n### 2.4 面向对象编程\nPython支持面向对象编程，包括类的定义、继承、多态等特性。\n\n## 三、实践应用\n通过学习Python，我完成了以下实践项目：\n1. 学生成绩管理系统\n2. 数据分析可视化\n3. Web应用开发\n\n## 四、总结与展望\nPython是一门功能强大且易于学习的编程语言，通过系统的学习和实践，我掌握了Python的核心语法和应用技能。未来将继续深入学习Python在人工智能领域的应用。\n''',
        'keywords': ['Python', '变量', '函数', '面向对象', '实践项目']
    },
    {
        'id': 2,
        'title': '数据结构与算法学习报告',
        'content': '''# 数据结构与算法学习报告\n\n## 一、概述\n数据结构是计算机存储、组织数据的方式，算法是解决问题的步骤集合。学习数据结构与算法对于提高程序效率和解决复杂问题具有重要意义。\n\n## 二、常见数据结构\n\n### 2.1 线性结构\n- 数组：连续存储的元素集合\n- 链表：通过指针连接的节点序列\n- 栈：后进先出（LIFO）的数据结构\n- 队列：先进先出（FIFO）的数据结构\n\n### 2.2 非线性结构\n- 树：层次化的数据结构\n- 图：由节点和边组成的网络结构\n- 哈希表：通过哈希函数快速查找的数据结构\n\n## 三、常用算法\n\n### 3.1 排序算法\n- 冒泡排序\n- 插入排序\n- 快速排序\n- 归并排序\n\n### 3.2 搜索算法\n- 线性搜索\n- 二分搜索\n- 深度优先搜索\n- 广度优先搜索\n\n## 四、学习体会\n通过学习数据结构与算法，我深刻理解了"程序=数据结构+算法"的理念，提高了分析问题和解决问题的能力。\n\n## 五、总结\n数据结构与算法是计算机科学的基础，掌握好这些知识对于成为一名优秀的程序员至关重要。\n''',
        'keywords': ['数据结构', '算法', '线性结构', '非线性结构', '排序', '搜索']
    }
]

def compare_reports(student_content, example_id=None):
    """
    比较学生报告与优秀范例
    :param student_content: 学生报告内容
    :param example_id: 指定比较的范例ID（可选）
    :return: 对比分析结果
    """
    # 如果未指定范例，选择最合适的范例
    if example_id:
        example = next((e for e in EXCELLENT_EXAMPLES if e['id'] == example_id), None)
    else:
        example = find_best_matching_example(student_content)
    
    if not example:
        return {
            'success': False,
            'error': '未找到合适的优秀范例'
        }
    
    # 分析学生报告与范例的差异
    comparison_result = analyze_differences(student_content, example)
    
    return {
        'success': True,
        'example': {
            'id': example['id'],
            'title': example['title'],
            'keywords': example['keywords']
        },
        'comparison': comparison_result
    }

def find_best_matching_example(student_content):
    """
    找到与学生报告最匹配的优秀范例
    :param student_content: 学生报告内容
    :return: 最匹配的范例
    """
    student_content_lower = student_content.lower()
    
    # 计算每个范例的匹配度
    matches = []
    for example in EXCELLENT_EXAMPLES:
        match_count = 0
        for keyword in example['keywords']:
            if keyword.lower() in student_content_lower:
                match_count += 1
        
        match_score = match_count / len(example['keywords']) if example['keywords'] else 0
        matches.append((match_score, example))
    
    # 返回匹配度最高的范例
    if matches:
        return sorted(matches, key=lambda x: x[0], reverse=True)[0][1]
    return None

def analyze_differences(student_content, example):
    """
    分析学生报告与范例的差异
    :param student_content: 学生报告内容
    :param example: 优秀范例
    :return: 差异分析结果
    """
    student_paragraphs = [p.strip() for p in student_content.split('\n') if p.strip()]
    example_paragraphs = [p.strip() for p in example['content'].split('\n') if p.strip()]
    
    # 计算段落数量差异
    paragraph_diff = len(example_paragraphs) - len(student_paragraphs)
    
    # 检查结构完整性
    student_has_headings = any(re.match(r'^#{1,6}\s+', p) for p in student_paragraphs)
    example_has_headings = any(re.match(r'^#{1,6}\s+', p) for p in example_paragraphs)
    
    # 检查关键词覆盖率
    student_content_lower = student_content.lower()
    covered_keywords = [k for k in example['keywords'] if k.lower() in student_content_lower]
    keyword_coverage = len(covered_keywords) / len(example['keywords']) if example['keywords'] else 0
    
    # 生成改进建议
    suggestions = []
    
    if paragraph_diff > 0:
        suggestions.append(f"优秀范例包含{len(example_paragraphs)}个段落，建议增加{paragraph_diff}个段落，使内容更丰富")
    
    if example_has_headings and not student_has_headings:
        suggestions.append("建议参考优秀范例，使用标题和小标题来组织内容结构")
    
    if keyword_coverage < 0.5:
        suggestions.append(f"建议补充{'、'.join(example['keywords'][:3])}等关键知识点的内容")
    
    # 检查是否包含实践应用或案例
    if '实践' not in student_content_lower and '项目' not in student_content_lower and '案例' not in student_content_lower:
        if any(word in example['content'].lower() for word in ['实践', '项目', '案例']):
            suggestions.append("建议增加实践案例或项目经验的描述，增强报告的实用性")
    
    return {
        'paragraph_count': {
            'student': len(student_paragraphs),
            'example': len(example_paragraphs),
            'difference': paragraph_diff
        },
        'structure': {
            'student_has_headings': student_has_headings,
            'example_has_headings': example_has_headings
        },
        'keyword_coverage': {
            'covered_keywords': covered_keywords,
            'total_keywords': example['keywords'],
            'coverage_ratio': keyword_coverage
        },
        'suggestions': suggestions
    }
