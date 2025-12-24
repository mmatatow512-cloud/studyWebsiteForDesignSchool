from core.course.course_schema import Course
from core.kg.kg_node_generator import KGNodeGenerator
from core.kg.kg_relation_generator import KGRelationGenerator

class KGGenerator:
    """整合节点和关系生成的极简工具类"""
    def generate_kg(self, course: Course):
        # 生成节点
        node_gen = KGNodeGenerator()
        nodes = node_gen.generate_nodes(course)
        node_gen.validate_nodes(course, nodes)

        # 生成关系
        relation_gen = KGRelationGenerator()
        relations = relation_gen.generate_relations(course, nodes)
        relation_gen.validate_relations(relations)

        return nodes, relations