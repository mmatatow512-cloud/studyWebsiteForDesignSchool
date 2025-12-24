import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.abspath('.'))

from core.course.course_schema import Course, CourseUnit
from core.kg.kg_node_generator import KGNodeGenerator

def test_node_generation():
    # 构造测试课程数据
    unit1 = CourseUnit(unit_id="u1", unit_name="PS基础", course_id="c1", sort=1)
    unit2 = CourseUnit(unit_id="u2", unit_name="PS抠图", course_id="c1", sort=2)
    course = Course(course_id="c1", course_name="PS课程", units=[unit1, unit2])

    # 生成节点
    generator = KGNodeGenerator()
    nodes = generator.generate_nodes(course)

    # 验证数量：1个课程节点 + 2个单元节点 = 3个
    assert len(nodes) == 3, "节点数量错误"
    # 验证无外部节点
    assert generator.validate_nodes(course, nodes), "包含外部节点"
    print("节点生成测试通过")

if __name__ == "__main__":
    test_node_generation()