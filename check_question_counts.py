from app import app, db, Question

with app.app_context():
    print('当前题库难度分布：')
    print('简单难度题目数量:', Question.query.filter_by(difficulty='简单').count())
    print('中等难度题目数量:', Question.query.filter_by(difficulty='中等').count())
    print('困难难度题目数量:', Question.query.filter_by(difficulty='困难').count())
    print('总题目数量:', Question.query.count())

    # 查看测验生成时的难度处理逻辑
    print('\n测验生成时的难度处理：')
    print('当选择"简单"难度时，系统会自动使用"中等"难度的题目')
