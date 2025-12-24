import sqlite3

# 连接到数据库
db_path = '/Users/sevenpeaches/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/8a21a9d88389e8eee826eb065e9ceeae/Message/MessageTemp/58896f95cc0d5807e3d0bb18fac61435/File/study_website_python1/instance/user_management.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 先查看当前各类题目数量
print("删除前的题目分布：")
cursor.execute("SELECT source, COUNT(*) FROM question GROUP BY source;")
result = cursor.fetchall()
for source, count in result:
    print(f"  {source}: {count}道")

# 删除系统测试题（ai_generated和manual_upload），保留用户上传的html_upload
print("\n正在删除系统测试题...")

# 删除ai_generated类型的题目
delete_ai_sql = "DELETE FROM question WHERE source = 'ai_generated'"
cursor.execute(delete_ai_sql)
ai_deleted = cursor.rowcount
print(f"  删除了 {ai_deleted} 道ai_generated测试题")

# 删除manual_upload类型的题目
delete_manual_sql = "DELETE FROM question WHERE source = 'manual_upload'"
cursor.execute(delete_manual_sql)
manual_deleted = cursor.rowcount
print(f"  删除了 {manual_deleted} 道manual_upload测试题")

# 提交事务
conn.commit()

# 查看删除后的题目数量
print("\n删除后的题目分布：")
cursor.execute("SELECT source, COUNT(*) FROM question GROUP BY source;")
result = cursor.fetchall()
for source, count in result:
    print(f"  {source}: {count}道")

# 查看总数量
total_sql = "SELECT COUNT(*) FROM question"
cursor.execute(total_sql)
total = cursor.fetchone()[0]
print(f"\n总剩余题目数：{total}道")

# 关闭连接
conn.close()

print("\n系统测试题删除完成！")