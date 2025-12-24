from typing import List, Optional

class CourseUnit:
    def __init__(self, unit_id: str, unit_name: str, sort: int):
        self.unit_id = unit_id
        self.unit_name = unit_name
        self.sort = sort
    
    def dict(self):
        return {
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "sort": self.sort
        }

class Course:
    def __init__(self, course_id: str, course_name: str, units: List[CourseUnit]):
        self.course_id = course_id
        self.course_name = course_name
        self.units = units
    
    def dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "units": [unit.dict() for unit in self.units]
        }

class KGNode:
    def __init__(self, node_id: str, node_name: str, node_type: str):
        self.node_id = node_id
        self.node_name = node_name
        self.node_type = node_type
    
    def dict(self):
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "node_type": self.node_type
        }

class KGRelation:
    def __init__(self, relation_id: str, source_node_id: str, target_node_id: str, relation_type: str, description: str):
        self.relation_id = relation_id
        self.source_node_id = source_node_id
        self.target_node_id = target_node_id
        self.relation_type = relation_type
        self.description = description
    
    def dict(self):
        return {
            "relation_id": self.relation_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "relation_type": self.relation_type,
            "description": self.description
        }