# ===== Day15 跟练 v3(实现由你本人盲写于下方) =====
# 文件:extra\extra_rectangle.py | ≤120 行 | 禁:第三方库、try/except
# 【需求】Rectangle 类:长宽为实例属性;能回答面积/周长/是否正方形三个问题并各自 print
#   自证:python extra_rectangle.py 至少一个实例 → 三步都有 print → 含正方形与非正方形两种结论
# 【可用知识点】class、__init__、self、实例属性、实例方法、if、print、f-string
# 【越界需留痕(用了不删,标一行)】私有属性 __xxx(10.2,归 day17);三目表达式(归属待确认);字典解包传参(边界待确认)
# 【教材·只读】10.1 类和实例 + 10.5 实例属性和类属性;⚠ 10.1 下一页即 10.2 访问限制,读完即停
# 【加分可选】长宽为正数校验;按比例放大后返回新尺寸
# 【复验待修】
#   P1  长宽用私有属性且未标【超前】;三目、字典解包属需留痕/需确认项
#   P2  只建 12x12 一个实例,is_square 永远只走"是"分支,"否"从未验证 → 补一个长宽不等实例
#   P1→day16 前置:get_area/get_perimeter/is_square 只 print 不 return —— 明天继承/多态要的是"同签名给出值、由子类替换行为",只打印的方法在多态里用不上;先让三个方法给出数值,调用处再负责打印
#   P2  扩展项(长宽为正校验)未做(加分,不计缺)
# ================= 以下开始盲写(本次未改动你的实现) =================

class Rectangle():
    '''创建一个矩形，计算矩形属性'''
    def __init__(self,w,h):
        self.__width = w #私有属性 超前
        self.__height = h
         
    def get_area(self):
        '''打印矩形面积'''
        return self.__width * self.__height
    
    def get_perimeter(self):
        '''打印矩形周长'''
        return (self.__width+self.__height)*2
    
    def is_square(self):
        '''判断矩形是不是正方形'''
        return self.__height == self.__width

if __name__ =='__main__':
    test_react={"w":12,"h":12}
    react_a = Rectangle(**test_react)
    print(f'矩形的面积是：{react_a.get_area()}')
    print(f'矩形的周长是：{react_a.get_perimeter()}')
    print(f'是否是正方形：{"是" if react_a.is_square() else "否"}')

    test_react2={"w":12,"h":14}
    react_b = Rectangle(**test_react2)
    print(f'矩形的面积是：{react_b.get_area()}')
    print(f'矩形的周长是：{react_b.get_perimeter()}')
    print(f'是否是正方形：{"是" if react_b.is_square() else "否"}')
