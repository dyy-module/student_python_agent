# 第03周 · Day17 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言。末尾须做行为-知识点自证表(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
class 特殊方法
__str__ 定义class 实例  字符串读取功能
__eq__ 定义class 实例 == 对比功能
__add__ 定义class 实例 + 功能
__len__ 定义class 实例  len(X) 读取功能

dunder 函数 触发的时机

## 知识点小结
class 有很多 特殊的 dunder 方法，可以帮助我们定制类，一般称为 魔术方法

这些方法一般不手动触发，由运行过程中python解释器自行触发

```python

class Order:
    def __init__(self, amt, sku, id):  # 触发时机，在 Order 实例化的时候直接触发
        self.amt = amt
        self.sku = sku
        self.id = id

    def __str__(self):  # 在print/str 访问类的时候触发
        return f'{self.sku} {self.amt}'

    def __eq__(self, other):  # 在两个实例 == 对比的时候触发
        return self.id == other.id

    def __add__(self, other):  # 在 两个实例 + 相加时触发
        return self.amt + other.amt

    def __len__(self):  # len(实例) 获取长度时触发
        return 1


o1 = Order(12, '苹果', '123')
o2 = Order(14, '香蕉', '222')

print(o1)
print(o1 == o2)
print(o1 + o2)
print(len(o1))

```

1. 生命周期
   
```python
class Demo:
    def __new__(cls, *args, **kwargs):   # 第一步：真正创建对象（返回实例）
        print('__new__')
        return super().__new__(cls)
    def __init__(self):                  # 第二步：初始化已创建的对象
        print('__init__')
    def __del__(self):                   # 引用计数归零时（时机不保证）
        print('__del__')

```
2. __str__ vs __repr__(超前)
__str__： 触发 print()、str()
__repr__ ：交互式回显、repr()、打印容器里的元素

3. 属性访问(超前)
__getattr__ 是兜底：实例字典里找得到就不会触发它
__getattribute__ 拦截一切，内部任何 self.xxx 都会再次触发它自己，必须用 super() 委托
__setattr__ 内部赋值同理，要么 super().__setattr__()，要么直接操作 self.__dict__
```python
class A:
    def __getattr__(self, name):          # 兜底：常规查找【失败】才调用
        print(f'__getattr__: {name}')
    def __getattribute__(self, name):     # 拦截【一切】属性访问
        print(f'__getattribute__: {name}')
        return super().__getattribute__(name)   # 必须 super()，否则递归
    def __setattr__(self, name, value):   # self.x = v
        super().__setattr__(name, value)  # 内部直接 self.x=... 会无限递归
```
4. 可调用 __call__
    被当方法调用时
    ```python
        class Counter:
            def __init__(self):
                self.n = 0
            def __call__(self):
                self.n += 1
                return self.n
        c = Counter()
        c(); c(); c()          # 3
    ```


## JS→Python 对照
js 没有这些

## 卡点与解决(非必填)
暂无

## 行为-知识点自证表(vector.py)

| 行为 | 用到的知识点 | 其中我说不出出处的 |
|---|---|---|
| `__str__` 打印对象 | 类、print/str/f-string、魔法方法触发 | —— |
| `__eq__` 实例判等 | 类、== 运算符、魔法方法 | —— |
| `__len__` 取长度 | len() 运算、魔法方法 | —— |
| `magnitude()` 求模长 | math.sqrt、** 平方 | 二维向量到原点的欧氏距离公式(查的,这块理解不深) |
| `__lt__` + sorted 排序 | < 、sorted()、魔法方法 | —— |

> 表外一行(当日学了但没落进任何行为的知识点,待你确认补全):如 `__repr__ = __str__` 别名写法、dunder 由解释器自动触发的时机。

## 特殊说明
    模长 = sqrt(x^2 + y^2)，即二维向量到原点的欧氏距离