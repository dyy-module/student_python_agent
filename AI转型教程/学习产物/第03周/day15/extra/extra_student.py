# ===== Day15 跟练补录 v3(下方实现为你本人代码,本次未改动) =====
# 出处:廖雪峰 10.2「访问限制」配套练习 https://liaoxuefeng.com/books/python/oop/access/index.html
# 【超前】留痕:访问限制不属 day15 也不属任何周首教清单,归 day17(随 @property);不计分不扣分
# 【⑦ 2026-10-10】RUN=0;名单定为类属性 __gender_data=['male','female'] 且两处共用 ✓(与你 bank_account 的 operate_tip 同一形态)
#   五输入实测：'male'/'female' 通过;'xyz'/''/'MALE' 被拒 ——你定的判据达成 ✓
#   剩半条（唯一）：__init__ 收到无效 gender 时仍走"不创建属性"——实测 Student('x','') 造出的对象一调 get_gender() 就 AttributeError
#       → 无效输入要有确定归宿（先拦下来并告知调用方 / 给默认值,二选一）,选哪种写一行注释说明你的口径
#   旧 P2「重盲写靶子」已撤销——校验逻辑已由你独立写出,不再需要

# 请把下面的Student对象的gender字段对外隐藏起来，用get_gender()和set_gender()代替，并检查参数有效性：
class Student(object):
    """Student class with hidden gender field, use get_gender() and set_gender() instead"""
    __gender_data  = ['male', 'female']
    def __init__(self, name, gender):
        self.__name = name
        if gender in Student.__gender_data:
            self.__gender = gender

    def get_gender(self):
        return  self.__gender

    def set_gender(self,v):
        if v in Student.__gender_data:
            self.__gender = v
        else:
            return False

# 测试:
bart = Student('Bart', 'male')
if bart.get_gender() != 'male':
    print('测试失败!')
else:
    bart.set_gender('female')
    if bart.get_gender() != 'female':
        print('测试失败!')
    else:
        print('测试成功!')
