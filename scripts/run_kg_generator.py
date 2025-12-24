from typing import List
from core.course.course_schema import Course, CourseUnit
from core.kg.kg_generator import KGGenerator
from core.kg.kg_storage import KGStorage
import json

def load_course_data(file_path: str = "project/data/course_data.json") -> List[Course]:
    """加载课程数据（极简版）"""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
    courses = []
    for item in raw_data:
        # 创建units列表，替换原始数据中的units
        item_copy = item.copy()
        item_copy["units"] = [CourseUnit(**u) for u in item["units"]]
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