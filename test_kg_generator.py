from core.course.course_schema import Course, Unit
from core.kg.kg_generator import KGGenerator

# 创建测试数据
course = Course(
    course_id="c001",
    course_name="设计基础课程",
    units=[
        Unit(unit_id="u001", unit_name="设计概论", sort=1),
        Unit(unit_id="u002", unit_name="色彩理论", sort=2),
        Unit(unit_id="u003", unit_name="构图技巧", sort=3),
        Unit(unit_id="u004", unit_name="实践项目", sort=4)
    ]
)

# 生成知识图谱
kg_generator = KGGenerator()
nodes, relations = kg_generator.generate_kg(course)

# 验证结果
print("=== 测试结果 ===")
print(f"节点数量: {len(nodes)}")
print(f"关系数量: {len(relations)}")
print()

# 检查关系类型
print("关系类型检查:")
relation_types = {r.relation_type for r in relations}
print(f"关系类型: {relation_types}")
if relation_types == {"contain", "progress"}:
    print("✅ 关系类型合法性: 100%")
else:
    print("❌ 关系类型合法性: 失败")
print()

# 检查包含关系
print("包含关系检查:")
contain_relations = [r for r in relations if r.relation_type == "contain"]
expected_contain = len(course.units)
actual_contain = len(contain_relations)
print(f"预期包含关系数: {expected_contain}, 实际包含关系数: {actual_contain}")
if actual_contain == expected_contain:
    print("✅ 包含关系覆盖率: 100%")
else:
    print("❌ 包含关系覆盖率: 失败")
print()

# 检查递进关系
print("递进关系检查:")
progress_relations = [r for r in relations if r.relation_type == "progress"]
expected_progress = len(course.units) - 1
actual_progress = len(progress_relations)
print(f"预期递进关系数: {expected_progress}, 实际递进关系数: {actual_progress}")
if actual_progress == expected_progress:
    print("✅ 递进关系覆盖率: 100%")
else:
    print("❌ 递进关系覆盖率: 失败")
print()

# 检查关系描述
print("关系描述检查:")
all_desc_correct = True
for r in relations:
    if r.relation_type == "contain":
        if not "包含" in r.description:
            all_desc_correct = False
            print(f"❌ 包含关系描述错误: {r.description}")
    elif r.relation_type == "progress":
        if not "先学" in r.description or not "再学" in r.description:
            all_desc_correct = False
            print(f"❌ 递进关系描述错误: {r.description}")
if all_desc_correct:
    print("✅ 所有关系描述准确")
print()

# 打印所有关系
print("=== 所有关系详情 ===")
for i, relation in enumerate(relations, 1):
    print(f"{i}. {relation.relation_id}")
    print(f"   源节点: {relation.source_node_id}")
    print(f"   目标节点: {relation.target_node_id}")
    print(f"   类型: {relation.relation_type}")
    print(f"   描述: {relation.description}")
    print()