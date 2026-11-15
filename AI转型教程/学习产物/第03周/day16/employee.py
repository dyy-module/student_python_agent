# ===== day16 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:employee.py | ≤120 行 | 禁:第三方库(Day22前)、try/except(归day19)、私有属性(见越界栏)、多继承(本周不教)
#
# 【需求】员工继承体系:同一个 salary() 接口,不同工种各给各的实现——这就是多态的最小样本,第07周 LangChain 的 Chain/Tool、第13周 FastAPI 的服务层都靠这套组织方式
#   1 基类 Employee 带 name 与 base,提供 salary() 的默认口径,并提供 intro()(把姓名与薪资说给人听)
#   2 Manager 比基类多一份奖金;它要新增自己的字段,同时 name/base 仍须被正常初始化(本日 super() 的真实作用就在这儿)
#   3 Developer 带 level,salary() 在基类口径之上按 level 加成;加成幅度你自定,并把这个约定写进 index.md——闭卷会问
#   4 一个列表混装三种员工,for 遍历统一调 salary() 逐个 print:调用方不知道也不必知道每个元素的确切类型
#   5 issubclass() 与 isinstance() 各验证一次并 print——一个比"类与类",一个比"对象与类",别混用
#   自证:python employee.py 一次跑通;三类员工的 salary 结果互不相同;intro() 至少打印一次;两个类型判断各一条输出
# 【可用知识点】class、__init__、self、实例属性、类属性、继承、方法重写、super()、多态、issubclass()、isinstance()、for、print、f-string
# 【越界需留痕(用了不删,标一行)】私有属性 __xxx(廖雪峰10.2,归day17);@property/@classmethod/@staticmethod(归day17);多继承(本周不教);try/except(归day19)
#   留痕格式:【超前】知识点 | 出处 | 归 dayXX | 影响哪个行为
# 【教材·只读3处,读完即停】
#   liaoxuefeng.com/books/python/oop/extend/index.html(10.3 继承和多态:继承/重写/多态)
#   docs.python.org/zh-cn/3/library/functions.html#super(super() 的正式出处——10.3 全页没有 super 示例,已实测)
#   docs.python.org/zh-cn/3/tutorial/classes.html 只读 9.5 继承一节(issubclass/isinstance)
#   ⚠ 10.3 的下一页 10.4 已学过(day15),再往后 11.x 是 day17 的 @property/定制类;10.3 页内「鸭子类型」小节本日不验收;runoob 面向对象页的「多继承」小节不读
# 【交检】跑通无报错、每步 print;index.md 末做行为-知识点自证表(行=产物里的一个行为,3列)+ 表外一行差集;不誊写教材章节
# 【加分可选】再加一层子类,验证三级继承下的字段初始化;思考 intro() 该不该复用 salary()(写进 index.md,不强制实现)
# ================= 以下开始盲写(壳不得改动下方实现行) =================

class Employee(object):
    '''工资基础'''

    def __init__(self, name, base=2000):
        self.name = name
        self.base = base

    def salary(self):
        '''基础工资'''
        return self.base

    def intro(self):
        '''工资 和姓名'''
        return f'{self.name} 的工资为 {self.salary()}'


class Manager(Employee):
    ''' 管理者工资 '''

    def __init__(self, name, base=2000, bonus=800):
        super().__init__(name, base)
        self.bonus = bonus

    def salary(self):
        '''带奖金的工资'''
        base = super().salary()
        return base + self.bonus


class Developer(Employee):
    ''' 分级工资 '''

    def __init__(self, name, base=2000, level=1):
        super().__init__(name, base)
        self.level = level

    def salary(self):
        '''分级工资，每级+500'''
        baseSalary = super().salary()
        return baseSalary + self.level*500


if __name__ == '__main__':
    say = Employee('say')
    wy = Manager('wy', bonus=1000)
    qqa = Developer('qqa', level=3)
    employee_list = [say, wy, qqa]

    for r in employee_list:
        print(r.salary())
    print(say.intro())
    print(wy.intro())
    print(qqa.intro())
    print(type(say) is Employee)
    print(type(qqa) is Employee)
    print(isinstance(say, Employee))
    print(isinstance(qqa, Employee))
    print(issubclass(Manager, Employee))
    print(issubclass(Employee, Employee))
    print(issubclass(Developer, Manager))
