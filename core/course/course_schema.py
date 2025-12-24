from pydantic import BaseModel
from typing import List, Optional, Literal

# 原有课程知识点结构（保留，不修改）
class CourseKnowledgePoint(BaseModel):
    point_id: str
    point_name: str
    content: str
    unit_id: str
    course_id: str
    page_num: Optional[int] = None
    video_timestamp: Optional[str] = None

# 课程单元结构（仅保留核心字段：ID、名称、所属课程、排序、知识点）
class CourseUnit(BaseModel):
    unit_id: str
    unit_name: str
    course_id: str
    sort: int  # 单元排序，用于生成递进关系（如1、2、3）
    knowledge_points: List[CourseKnowledgePoint] = []

# 课程整体结构
class Course(BaseModel):
    course_id: str
    course_name: str
    units: List[CourseUnit]

# 知识图谱核心结构（节点+关系）
class KGNode(BaseModel):
    node_id: str  # 格式：课程ID-类型-序号（如design_ps_001-course-01、design_ps_001-unit-01）
    node_name: str  # 课程名/单元名
    node_type: Literal["course", "unit"]  # 仅课程、单元两种节点类型
    course_id: str

class KGRelation(BaseModel):
    relation_id: str  # 格式：课程ID-类型-序号（如design_ps_001-contain-01）
    source_node_id: str  # 源节点ID
    target_node_id: str  # 目标节点ID
    relation_type: Literal["contain", "progress"]  # 仅包含、递进两种关系
    description: str  # 关系描述（如"设计PS课程包含PS基础操作单元"）