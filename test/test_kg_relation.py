from core.course.course_schema import Course, CourseUnit, CourseKnowledgePoint
from core.kg.kg_node_generator import KGNodeGenerator
from core.kg.kg_relation_generator import KGRelationGenerator
from core.kg.kg_generator import KGGenerator

def test_relation_generation():
    # 构造测试课程数据
    unit1 = CourseUnit(
        unit_id="u1", 
        unit_name="PS基础", 
        course_id="c1", 
        sort=1,
        knowledge_points=[]
    )
    unit2 = CourseUnit(
        unit_id="u2", 
        unit_name="PS抠图", 
        course_id="c1", 
        sort=2,
        knowledge_points=[]
    )
    unit3 = CourseUnit(
        unit_id="u3", 
        unit_name="PS合成", 
        course_id="c1", 
        sort=3,
        knowledge_points=[]
    )
    course = Course(course_id="c1", course_name="PS课程", units=[unit1, unit2, unit3])

    # 生成节点
    node_generator = KGNodeGenerator()
    nodes = node_generator.generate_nodes(course)

    # 生成关系
    relation_generator = KGRelationGenerator()
    relations = relation_generator.generate_relations(course, nodes)

    # 验证关系数量：3个单元 → 3个包含关系 + 2个递进关系 = 5个关系
    expected_contain_relations = len(course.units)
    expected_progress_relations = len(course.units) - 1
    expected_total_relations = expected_contain_relations + expected_progress_relations
    assert len(relations) == expected_total_relations, f"关系数量错误，预期{expected_total_relations}个，实际{len(relations)}个"

    # 验证关系类型：仅包含contain和progress
    relation_types = {r.relation_type for r in relations}
    assert relation_types == {"contain", "progress"}, f"关系类型错误，预期{{'contain', 'progress'}}，实际{relation_types}"

    # 验证包含关系：课程 → 每个单元
    contain_relations = [r for r in relations if r.relation_type == "contain"]
    assert len(contain_relations) == expected_contain_relations, f"包含关系数量错误，预期{expected_contain_relations}个，实际{len(contain_relations)}个"

    # 验证递进关系：按sort排序，前一个单元 → 后一个单元
    progress_relations = [r for r in relations if r.relation_type == "progress"]
    assert len(progress_relations) == expected_progress_relations, f"递进关系数量错误，预期{expected_progress_relations}个，实际{len(progress_relations)}个"

    # 验证递进关系顺序
    unit_names = ["PS基础", "PS抠图", "PS合成"]
    for i in range(len(progress_relations)):
        relation = progress_relations[i]
        # 验证源节点和目标节点的顺序
        assert unit_names[i] in relation.source_node_id, f"递进关系源节点顺序错误，第{i+1}个递进关系应该是{unit_names[i]} → {unit_names[i+1]}"
        assert unit_names[i+1] in relation.target_node_id, f"递进关系目标节点顺序错误，第{i+1}个递进关系应该是{unit_names[i]} → {unit_names[i+1]}"

    # 验证关系描述准确
    for relation in relations:
        if relation.relation_type == "contain":
            assert "包含" in relation.description, f"包含关系描述错误，预期包含'包含'，实际{relation.description}"
        else:  # progress
            assert "先学" in relation.description and "再学" in relation.description, f"递进关系描述错误，预期包含'先学'和'再学'，实际{relation.description}"

    print("关系生成测试通过")

def test_kg_generator_integration():
    # 构造测试课程数据
    unit1 = CourseUnit(
        unit_id="u1", 
        unit_name="PS基础", 
        course_id="c2", 
        sort=1,
        knowledge_points=[]
    )
    unit2 = CourseUnit(
        unit_id="u2", 
        unit_name="PS抠图", 
        course_id="c2", 
        sort=2,
        knowledge_points=[]
    )
    course = Course(course_id="c2", course_name="PS进阶课程", units=[unit1, unit2])

    # 使用整合工具生成节点和关系
    kg_generator = KGGenerator()
    nodes, relations = kg_generator.generate_kg(course)

    # 验证节点数量：1个课程节点 + 2个单元节点 = 3个节点
    assert len(nodes) == 1 + len(course.units), f"节点数量错误，预期{1 + len(course.units)}个，实际{len(nodes)}个"

    # 验证关系数量：2个单元 → 2个包含关系 + 1个递进关系 = 3个关系
    expected_contain_relations = len(course.units)
    expected_progress_relations = len(course.units) - 1
    expected_total_relations = expected_contain_relations + expected_progress_relations
    assert len(relations) == expected_total_relations, f"关系数量错误，预期{expected_total_relations}个，实际{len(relations)}个"

    print("知识图谱整合生成测试通过")

if __name__ == "__main__":
    test_relation_generation()
    test_kg_generator_integration()