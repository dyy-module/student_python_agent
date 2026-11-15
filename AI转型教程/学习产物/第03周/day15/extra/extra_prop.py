# ===== Day15 跟练补录 v3(下方实现为你本人代码,本次未改动) =====
# 出处:廖雪峰 10.5 实例属性和类属性配套练习(类属性统计实例数) https://liaoxuefeng.com/books/python/oop/props/index.html
# 闭包归属:✅ 属 day15 当日范围,可计分;自发加练(当日清单只列 extra_rectangle.py),请在 index.md 记一行来源
# 【复验待修】
#   P2  文件名 "prop" 易与 @property(day17 超前项)混淆,本件与它无关 → 可改名 extra_class_attr_count.py
#   P2  测试代码嵌套 if 四层 → 可改"逐条断言 + 统一输出结论"
#   P2  重盲写的靶子(教材未给答案,只给起点 count=0 与测试脚手架 → 不算照抄):全部增量只有一行类属性自增,
#       能否说清为什么必须经类名而不能写 self.count —— 后者会在实例上创建同名属性遮蔽类属性(本页末段与 bank_account 的 self.bank_name 同一个坑)

# 为了统计学生人数，可以给Student类增加一个类属性，每创建一个实例，该属性自动增加
class Student(object):
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count+=1

# 测试:
if Student.count != 0:
    print('测试失败!')
else:
    bart = Student('Bart')
    if Student.count != 1:
        print('测试失败!')
    else:
        lisa = Student('Bart')
        if Student.count != 2:
            print('测试失败!')
        else:
            print('Students:', Student.count)
            print('测试通过!')
