import json
from core.course.course_schema import Course, CourseUnit, CourseKnowledgePoint, KGNode, KGRelation
from core.kg.kg_generator import KGGenerator

# 测试加载课程数据
def test_load_course_data():
    with open('data/course_data.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    # 转换为Course对象
    courses = [Course(**course) for course in course_data]
    
    print(f"成功加载 {len(courses)} 门课程")
    
    for course in courses:
        print(f"\n课程ID: {course.course_id}")
        print(f"课程名称: {course.course_name}")
        print(f"课程单元数量: {len(course.units)}")
        
        # 按sort字段排序并打印单元
        sorted_units = sorted(course.units, key=lambda x: x.sort)
        for i, unit in enumerate(sorted_units):
            print(f"  单元 {i+1} (ID: {unit.unit_id}, 排序: {unit.sort}): {unit.unit_name}")
            print(f"    知识点数量: {len(unit.knowledge_points)}")
            for kp in unit.knowledge_points:
                print(f"    - 知识点: {kp.point_name}")

# 测试生成知识图谱节点和关系
def test_generate_kg():
    with open('data/course_data.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    courses = [Course(**course) for course in course_data]
    
    # 生成知识图谱节点和关系
    all_nodes = []
    all_relations = []
    
    for course in courses:
        # 课程节点
        course_node = KGNode(
            node_id=f"{course.course_id}-course-01",
            node_name=course.course_name,
            node_type="course",
            course_id=course.course_id
        )
        all_nodes.append(course_node)
        
        # 按sort排序单元
        sorted_units = sorted(course.units, key=lambda x: x.sort)
        
        # 生成单元节点和包含关系
        for i, unit in enumerate(sorted_units):
            unit_node = KGNode(
                node_id=f"{course.course_id}-unit-{str(i+1).zfill(2)}",
                node_name=unit.unit_name,
                node_type="unit",
                course_id=course.course_id
            )
            all_nodes.append(unit_node)
            
            # 包含关系
            contain_relation = KGRelation(
                relation_id=f"{course.course_id}-contain-{str(i+1).zfill(2)}",
                source_node_id=course_node.node_id,
                target_node_id=unit_node.node_id,
                relation_type="contain",
                description=f"{course.course_name}包含{unit.unit_name}单元"
            )
            all_relations.append(contain_relation)
        
        # 生成递进关系
        for i in range(len(sorted_units) - 1):
            source_unit = sorted_units[i]
            target_unit = sorted_units[i+1]
            
            progress_relation = KGRelation(
                relation_id=f"{course.course_id}-progress-{str(i+1).zfill(2)}",
                source_node_id=f"{course.course_id}-unit-{str(i+1).zfill(2)}",
                target_node_id=f"{course.course_id}-unit-{str(i+2).zfill(2)}",
                relation_type="progress",
                description=f"{source_unit.unit_name}单元递进至{target_unit.unit_name}单元"
            )
            all_relations.append(progress_relation)
    
    print(f"\n成功生成 {len(all_nodes)} 个知识图谱节点")
    print(f"成功生成 {len(all_relations)} 个知识图谱关系")
    
    # 打印部分节点和关系
    print("\n部分知识图谱节点:")
    for node in all_nodes[:3]:
        print(f"  - {node.node_name} (ID: {node.node_id}, 类型: {node.node_type})")
    
    print("\n部分知识图谱关系:")
    for relation in all_relations[:3]:
        print(f"  - {relation.description} (类型: {relation.relation_type})")

# 测试KGGenerator类

def test_kg_generator():
    with open('data/course_data.json', 'r', encoding='utf-8') as f:
        course_data = json.load(f)
    
    courses = [Course(**course) for course in course_data]
    
    # 使用KGGenerator生成知识图谱
    kg_gen = KGGenerator()
    
    for course in courses:
        print(f"\n=== 测试课程: {course.course_name} ===")
        
        # 生成节点和关系
        nodes, relations = kg_gen.generate_kg(course)
        
        print(f"生成的节点数量: {len(nodes)}")
        print(f"生成的关系数量: {len(relations)}")
        
        # 验证节点类型
        course_node_count = sum(1 for n in nodes if n.node_type == "course")
        unit_node_count = sum(1 for n in nodes if n.node_type == "unit")
        kp_node_count = sum(1 for n in nodes if n.node_type == "knowledge_point")
        
        print(f"课程节点数: {course_node_count}")
        print(f"单元节点数: {unit_node_count}")
        print(f"知识点节点数: {kp_node_count}")
        
        # 验证关系类型和数量
        contain_relations = [r for r in relations if r.relation_type == "contain"]
        progress_relations = [r for r in relations if r.relation_type == "progress"]
        
        print(f"包含关系数: {len(contain_relations)}")
        print(f"递进关系数: {len(progress_relations)}")
        
        # 验证关系数量是否符合预期
        expected_contain = unit_node_count
        expected_progress = unit_node_count - 1 if unit_node_count > 0 else 0
        
        print(f"预期包含关系数: {expected_contain}")
        print(f"预期递进关系数: {expected_progress}")
        
        assert len(contain_relations) == expected_contain, f"包含关系数量错误：{len(contain_relations)} != {expected_contain}"
        assert len(progress_relations) == expected_progress, f"递进关系数量错误：{len(progress_relations)} != {expected_progress}"
        
        print(f"\n✅ 课程 {course.course_name} 的知识图谱生成验证通过！")
        
        # 打印部分关系示例
        print("\n关系示例:")
        for i, relation in enumerate(relations[:5]):
            print(f"  {i+1}. {relation.description} (类型: {relation.relation_type})")


if __name__ == "__main__":
    print("=== 测试课程数据加载 ===")
    test_load_course_data()
    
    print("\n=== 测试知识图谱生成 ===")
    test_generate_kg()
    
    print("\n=== 测试KGGenerator类 ===")
    test_kg_generator()
    
    print("\n✅ 所有测试通过，数据结构能正常加载和使用！")
