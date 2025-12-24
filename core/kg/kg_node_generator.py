from typing import List
from core.course.course_schema import Course, KGNode

class KGNodeGenerator:
    """生成图谱节点的工具类"""
    def generate_nodes(self, course: Course) -> List[KGNode]:
        """
        生成节点：
        1. 课程节点：1个
        2. 单元节点：每个单元1个
        """
        nodes = []
        
        # 1. 生成课程节点
        course_node = KGNode(
            node_id=f"course-{course.course_id}",
            node_name=course.course_name,
            node_type="course"
        )
        nodes.append(course_node)
        
        # 2. 生成单元节点
        for unit in course.units:
            unit_node = KGNode(
                node_id=f"unit-{unit.unit_id}",
                node_name=unit.unit_name,
                node_type="unit"
            )
            nodes.append(unit_node)
        
        return nodes
    
    def validate_nodes(self, course: Course, nodes: List[KGNode]):
        """验证节点生成是否正确"""
        # 检查课程节点数量
        course_nodes = [n for n in nodes if n.node_type == "course"]
        if len(course_nodes) != 1:
            raise ValueError(f"课程节点数量应为1，实际为{len(course_nodes)}")
        
        # 检查单元节点数量
        unit_nodes = [n for n in nodes if n.node_type == "unit"]
        if len(unit_nodes) != len(course.units):
            raise ValueError(f"单元节点数量应为{len(course.units)}，实际为{len(unit_nodes)}")
        
        return True