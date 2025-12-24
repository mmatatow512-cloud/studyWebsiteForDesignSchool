import json
from core.course.course_schema import Course, KGNode, KGRelation
from typing import List
import os

class KGStorage:
    """极简图谱存储工具，仅保存为JSON文件"""
    def save_kg(self, course: Course, nodes: List[KGNode], relations: List[KGRelation], save_path: str = "data/kg"):
        """按课程ID命名，保存图谱数据"""
        # 构造图谱数据
        kg_data = {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "nodes": [n.dict() for n in nodes],
            "relations": [r.dict() for r in relations]
        }

        # 创建目录（不存在则创建）
        os.makedirs(save_path, exist_ok=True)
        # 保存文件
        file_path = f"{save_path}/{course.course_id}_kg.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(kg_data, f, ensure_ascii=False, indent=2)

        print(f"知识图谱已保存至：{file_path}")