from app import db, Unit

try:
    units = Unit.query.all()
    print("Units found:")
    for unit in units:
        print(f"Unit ID: {unit.id}, Course ID: {unit.course_id}, File Path: {unit.file_path}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
