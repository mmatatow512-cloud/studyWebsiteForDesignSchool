from typing import List 
from core.course.course_schema import Course, KGNode, KGRelation 

class KGRelationGenerator: 
    """生成图谱关系的工具类，仅包含+递进两种关系"""
    def generate_relations(self, course: Course, nodes: List[KGNode]) -> List[KGRelation]: 
        """
        生成关系：
        1. 包含关系：课程节点 → 所有单元节点
        2. 递进关系：按sort排序，前一个单元节点 → 后一个单元节点
        """
        relations = [] 
        seq = 1  # 关系序号 

        # 找到课程节点（仅1个）
        course_node = next(n for n in nodes if n.node_type == "course")
        # 找到单元节点并按sort排序
        unit_nodes = [n for n in nodes if n.node_type == "unit"]
        # 关联单元的sort字段（通过节点名称匹配单元）
        unit_node_with_sort = []
        for node in unit_nodes:
            unit = next(u for u in course.units if u.unit_name == node.node_name)
            unit_node_with_sort.append((node, unit.sort))
        # 按sort升序排列
        unit_node_with_sort.sort(key=lambda x: x[1])
        sorted_unit_nodes = [n for n, s in unit_node_with_sort]

        # 1. 生成包含关系：课程 → 每个单元
        for unit_node in sorted_unit_nodes:
            contain_relation = KGRelation(
                relation_id=f"{course.course_id}-contain-{seq:02d}",
                source_node_id=course_node.node_id,
                target_node_id=unit_node.node_id,
                relation_type="contain",
                description=f"{course_node.node_name}包含{unit_node.node_name}单元"
            )
            relations.append(contain_relation)
            seq += 1

        # 2. 生成递进关系：前一个单元 → 后一个单元
        for i in range(len(sorted_unit_nodes) - 1):
            current_node = sorted_unit_nodes[i]
            next_node = sorted_unit_nodes[i+1]
            progress_relation = KGRelation(
                relation_id=f"{course.course_id}-progress-{seq:02d}",
                source_node_id=current_node.node_id,
                target_node_id=next_node.node_id,
                relation_type="progress",
                description=f"先学{current_node.node_name}，再学{next_node.node_name}"
            )
            relations.append(progress_relation)
            seq += 1

        return relations 

    def validate_relations(self, relations: List[KGRelation]) -> bool: 
        """验证关系类型仅为contain/progress"""
        allowed_types = {"contain", "progress"}
        for r in relations:
            if r.relation_type not in allowed_types:
                raise ValueError(f"关系类型「{r.relation_type}」非法，仅允许{allowed_types}")
        return True