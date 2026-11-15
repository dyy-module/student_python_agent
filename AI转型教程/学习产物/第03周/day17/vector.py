# ===== day17 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:vector.py | ≤120 行 | 禁:第三方库(Day22前)、try/except(归day19)、私有属性/@property(超前,本周不深入)
#
# 【需求】让自定义的二维向量像内置类型一样"活"起来:能 print 出可读内容、能 == 比较、能 + 相加、能 len()、能按模长排序。机制核心=定义指定名字的 dunder 方法,Python 遇对应操作自动触发
#   1 Vector 带 x、y;__str__ 给人看的写法,__repr__ 给调试看的写法(两者可同实现)
#   2 __add__ 让 v1+v2 返回新向量;__eq__ 让 v1==v2 按分量判等;__len__ 让 len(v) 给出分量个数
#   3 __lt__ 让 v1<v2 成立,按"模长"比较;模长如何由 x、y 算出由你自定并写进 index.md(闭卷会问);对一组向量 sorted() 后打印,验证排序走的就是 __lt__
#   4 主流程逐个 print,每步注明验证的是哪个 dunder
#   自证:python vector.py 一次跑通;print(v)、v1+v2、v1==v2、len(v)、sorted 五处各有可见输出
# 【可用知识点】class、__init__、self、__str__、__repr__、__eq__、__add__、__len__、__lt__、sorted()(第02周高阶函数已学)、print、f-string
# 【越界需留痕(用了不删,标一行)】私有属性 __xxx(廖10.2,归day17随@property但本周不深入);@property/@classmethod/@staticmethod(归day17/本周不教);try/except(归day19)
#   留痕格式:【超前】知识点 | 出处 | 归 dayXX | 影响哪个行为
# 【教材·只读,读完即停】
#   liaoxuefeng.com/books/python/oop-adv/special-method/index.html(11.4 定制类:真讲到 __str__/__repr__,用 Student 例;__len__ 仅一句提及不示范)
#   ⚠ __add__/__eq__/__lt__ 运算符重载 11.4 整页不讲——正式出处=官方 datamodel 特殊方法名表 docs.python.org/zh-cn/3/reference/datamodel.html(给出 == →__eq__、< →__lt__、+ →__add__、len →__len__ 的映射)
#   ⚠ 菜鸟 runoob 面向对象页"运算符重载"一节示例恰是 class Vector 的 __add__,与本产物同构=题面答案,只作语法速查、严禁照抄实现;11.4 同页 __iter__/__getitem__/__getattr__/__call__ 本日产物不用,读到即停
# 【交检】跑通无报错、每步 print;index.md 末做行为-知识点自证表(行=产物里一个行为,3列)+ 表外一行差集;不誊写教材章节
# 【加分可选】把 __repr__ 写成"能重建对象"的形式;观察多个等模长向量 sorted() 的先后(写进 index.md,不强制实现)
# ================= 以下开始盲写(壳不得改动下方实现行) =================

import math


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    __repr__ = __str__

    def __add__(self, other):
        return Vector(self.x + other.x, self.y+other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __len__(self):
        return 2

    def magnitude(self):
        '''模长 = sqrt(x^2 + y^2)，即二维向量到原点的欧氏距离'''
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __lt__(self, other):
        return self.magnitude() < other.magnitude()


if __name__ == '__main__':
    v1 = Vector(1, 2)
    v2 = Vector(2, 3)
    v3 = Vector(1, 2)

    print(v1)
    print(v1+v2)
    print(v1 == v2)
    print(v1 == v3)
    print(len(v1))
    print(v1 < v2)
    print(sorted([v1, v2, v3]))  # 排序 触发 __lt__
