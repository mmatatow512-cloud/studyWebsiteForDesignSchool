import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.course.course_schema import Course, CourseUnit
from core.kg.kg_generator import KGGenerator
from core.kg.kg_storage import KGStorage
import json
from typing import List

def load_course_data(file_path: str = "data/course_data.json") -> List[Course]:
    """加载课程数据（极简版）"""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    courses = []
    for item in raw_data:
        # 转换units为CourseUnit对象
        item_copy = item.copy()
        item_copy["units"] = [CourseUnit(**u) for u in item_copy["units"]]
        course = Course(**item_copy)
        courses.append(course)
    return courses

if __name__ == "__main__":
    # 1. 加载课程数据
    courses = load_course_data()
    # 2. 生成+保存图谱
    generator = KGGenerator()
    storage = KGStorage()
    for course in courses:
        nodes, relations = generator.generate_kg(course)
        storage.save_kg(course, nodes, relations)