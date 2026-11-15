# ===== day17 跟练任务说明 v3(extra/extra_money.py,实现由你本人盲写) =====
# 文件:extra_money.py | ≤60 行 | 禁:第三方库、try/except(归day19)、私有属性/@property(超前)
#
# 【需求】Money(金额+币种):能 print 可读、能 + 相加(仅同币种)、能 == 判等。跨币种相加时 print 提示并拒绝——本周未学异常,用 print + 一个你能自圆其说的返回值处理,不 raise
#   1 Money 带 amount、currency;__str__ 给出"金额+币种"的可读写法
#   2 __add__ 同币种返回新 Money;不同币种 print 说明并拒绝(返回口径写进 index.md)
#   3 __eq__ 金额与币种都相同才相等
#   4 主流程 print 演示:一次同币种相加成功、一次异币种被拦、一次 == 判等
#   自证:python extra_money.py 跑通,三条分支各有可见输出,程序不崩
# 【可用知识点】class、__init__、self、实例属性、__str__、__add__、__eq__、if、print、f-string
# 【越界需留痕】私有属性 __xxx(10.2,归day17);@property/@classmethod/@staticmethod(归day17);try/except(归day19)
# 【教材·只读】同 vector.py 壳的出处;__add__/__eq__ 运算符重载查官方 datamodel 特殊方法名表(11.4 不讲运算符重载);runoob 运算符重载 Vector 例严禁照抄
# 【交检】跑通无报错、每步 print;行为并入 index.md 自证表即可,不必单列一表
# ================= 以下开始盲写(壳不得改动下方实现行) =================

class Money:
    def __init__(self,amt,currency):
        self.amt =amt
        self.currency = currency
    
    def __str__(self):
        return f'{self.amt} {self.currency}'
    
    def __add__(self, other):
        if(other.currency == self.currency):
            return Money(self.amt + other.amt, self.currency)
        else:
            return '币种不同，无法相加'
    
    def __eq__(self,other):
        return self.amt == other.amt and self.currency == other.currency
    

if __name__ =='__main__':
    m1 = Money(12,'$')
    m2 = Money(14,'$')
    m3 = Money(12,'￥')
    m4 = Money(12,'$')
    
    print(m1)
    print(m1==m2)
    print(m1==m3)
    print(m1==m4)
    print(m1 +m2)
    print(m1+m3)
    