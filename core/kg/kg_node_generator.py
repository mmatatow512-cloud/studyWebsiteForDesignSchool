from typing import List
from core.course.course_schema import Course, KGNode

class KGNodeGenerator:
    """仅基于课程/单元名称生成图谱节点的工具类"""
    def generate_nodes(self, course: Course) -> List[KGNode]:
        """
        生成两种节点：1个课程节点 + 每个单元对应1个单元节点
        """
        nodes = []
        seq = 1  # 节点序号

        # 1. 生成课程节点（仅1个）
        course_node = KGNode(
            node_id=f"{course.course_id}-course-{seq:02d}",  # 补零保证格式统一
            node_name=course.course_name,
            node_type="course",
            course_id=course.course_id
        )
        nodes.append(course_node)
        seq += 1

        # 2. 生成单元节点（每个单元对应1个）
        for unit in course.units:
            unit_node = KGNode(
                node_id=f"{course.course_id}-unit-{seq:02d}",
                node_name=unit.unit_name,
                node_type="unit",
                course_id=course.course_id
            )
            nodes.append(unit_node)
            seq += 1

        return nodes

    def validate_nodes(self, course: Course, nodes: List[KGNode]) -> bool:
        """验证节点名称仅为课程/单元名称，禁止外部内容"""
        allowed_names = {course.course_name} | {unit.unit_name for unit in course.units}
        for node in nodes:
            if node.node_name not in allowed_names:
                raise ValueError(f"节点「{node.node_name}」是外部内容，禁止生成")
        return True