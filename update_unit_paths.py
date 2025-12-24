from app import app, db, Unit
import os

# 获取应用上下文
with app.app_context():
    # 查询所有单元
    units = Unit.query.all()
    print(f"找到 {len(units)} 个单元")
    
    # 统计需要更新的单元数量
    updated_count = 0
    
    for unit in units:
        if '\\' in unit.file_path:
            print(f"\n单元ID: {unit.id}")
            print(f"旧路径: {unit.file_path}")
            
            # 将反斜杠替换为正斜杠
            new_path = unit.file_path.replace('\\', '/')
            unit.file_path = new_path
            
            print(f"新路径: {new_path}")
            updated_count += 1
    
    # 提交更改
    if updated_count > 0:
        db.session.commit()
        print(f"\n已更新 {updated_count} 个单元的文件路径")
    else:
        print("\n没有需要更新的单元路径")
        db.session.rollback()