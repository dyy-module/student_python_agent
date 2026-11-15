# ===== day16 跟练任务说明 v3(extra/extra_animal.py,实现由你本人盲写) =====
# 文件:extra_animal.py | ≤60 行 | 禁:第三方库、try/except(归day19)、私有属性(超前)、多继承(本周不教)
#
# 【需求】Animal 基类给 speak() 的默认叫声,Dog/Cat 各重写为自己的叫声;遍历一个装了多种动物的列表统一调 speak() 打印,体会"调用方只管调用,不管细节"
#   追加(本日重点):列表里混入一个不是 Animal 子类的对象(任何已学类型都行),遍历到它时先做判定再决定是否调用,并把判定结果 print 出来——让 issubclass()/isinstance() 真的用于拦截,而不是只演示一次返回 True
#   自证:python extra_animal.py 需看到 ≥3 种不同叫声的输出 + 1 条"被拦下"的说明输出,程序不崩
# 【可用知识点】class、__init__、实例属性、继承、方法重写、super()、isinstance()、issubclass()、for、print、f-string
# 【越界需留痕】私有属性 __xxx(10.2,归day17);@property/@classmethod/@staticmethod(归day17);多继承(本周不教)
#   留痕格式:【超前】知识点 | 出处 | 归 dayXX | 影响哪个行为
# 【教材·只读】同 employee.py 壳的三处。本题题面与廖雪峰10.3 同源,但该页练习只给起点代码、正文不给答案(已实测)——写完先合上教材答下面一问
# 【闭卷一问(写进 index.md,不写代码)】子类自己不写 speak() 时,调用会发生什么?属性在哪一层被找到、按什么顺序往下找(出处:官方 classes.html 9.5 对方法解析的叙述)
# 【交检】跑通无报错、每步 print;行为并入 index.md 的自证表即可,不必单列一表
# ================= 以下开始盲写(壳不得改动下方实现行) =================

class Animal(object):
    '''基类Animal，定义有叫声方法'''
    def speak(self):
        print('啊啊啊')
        
class Dog(Animal):
    '''小狗类'''
    def speak(self):
        print('汪汪')

class Cat(Animal):
    '''这是一只猫'''
    def speak(self):
        print('喵喵')

class Bear(Animal):
    '''这是一头熊'''
    def speak(self):
        print('嗷嗷嗷')
        
class Hamster(Animal):
    '''这是一只仓鼠，不知道怎么叫'''
    pass

weird_stuff ={}

def animal_speak():
    '''动物叫'''
    animals=[Animal(),Dog(),Cat(),Bear(),Hamster(),weird_stuff]
    for cls in animals:
        is_animal = isinstance(cls, Animal)
        print(f"是否是动物：{'YES' if is_animal else 'NO'}")
        if is_animal:
            cls.speak()
        else:
            print('这是个奇怪的东西不是动物。')
            
if __name__ == '__main__':
    animal_speak()