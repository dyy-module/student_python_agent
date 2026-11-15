# 第03周 · Day15 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言(见 00_验证规则与里程碑.md 日级第5条)。

## 今日主题

类和实例
梳理属性和类属性
type isinstance dir

## 知识点小结

```python
class Test(): #约定首字符大写类名
    bank_name='中国工商' # 所有实例共享变量
    def __init__(self,public_a,private_a): #特殊方法__init__前后分别有两个下划线！！！第一个参数永远是self，表示创建的实例本身
        # self.X 实例独享
        self.public_a = public_a # 实例完，可以直接外部修改
        self.__private_a = private_a # 实例完，外部无法修改，私有属性（并非完全不能修改，python只是给变量修改了名字，不推荐修改，容易出错）
  
    def get_private_a(self): # 可以通过内置方法获取和修改私有变量，self 必传
        return self.__private_a

# 超前，还没有具体看继承
# type 只认精确类型，isinstance 认继承链
class Test2(Test):pass

test1 = Test(1,2)
test2 = Test2(1,2)
print(type(123) == int)
print(type(test1) is Test) # True
print(type(test2) is Test) # False

print(isinstance(123, int))
print(isinstance(test1, Test)) # True
print(isinstance(test2, Test)) # True
```

```javascript
class Test{
    static bank_name='中国工商' // 静态属性，共享
    constructor(public_a,private_a){
        this.public_a = public_a  // 实例属性,没有私有共有区分，可以用下划线区分，但是不能阻止修改和访问
        this._private_a = private_a
    }

    get_private_a(){
        return this._private_a
    }

    static hello() {              // 静态方法
        return "hi";
    }
}

const test1 = new Test(1,2)

typeof test1 === 'object' // 返回类型字符串
test1 instanceof  Test // 检查原型链
test1 instanceof  Object

```

需求	用法
判断"是不是某类型或其子类"	isinstance(obj, T) ✅ 首选
精确判断"就是某类型"	type(obj) is T
同时判断多种类型	isinstance(obj, (A, B, C))
判断两个对象类型是否相同	type(a) is type(b)

继承部分超前----
class Animal: pass
class Dog(Animal): pass

d = Dog()

print(type(d))                    # <class '__main__.Dog'>
print(type(d) is Dog)             # True
print(type(d) is Animal)          # False
print(isinstance(d, Dog))         # True
print(isinstance(d, Animal))      # True
print(isinstance(d, (Dog, Cat)))  # True（假设有 Cat）

print(type(True) is int)          # False
print(isinstance(True, int))      # True

print(isinstance(123, (int, str)))  # True
print(type(123) is type(456))       # True

## JS→Python 对照

创建：py class A(): -> js class A {}
构造器：py __init__ 方法，第一个参数self指向自身，实例属性都挂在self上 -> js constructor，不需要第一个参数，实例属性都挂在this 上
私有变量 py __a,双下划线，外部无法直接访问。
实例化： JS new X() → Python X()(无new)
static字段 → Python 类体内直接赋值(类属性)
JS obj instanceof X → Python isinstance(obj, X);JS typeof obj → Python type(obj)

、Python vs JS 对照
用途	Python	JavaScript
判断基本类型	type(x) is int	typeof x === "number"
判断是否某类（含继承）	isinstance(x, T)	x instanceof T
精确判断类型	type(x) is T	没有直接对应，用 constructor
判断 None/null	x is None	x === null

## 卡点与解决

暂无

## 行为-知识点自证表(2026-10-10 取代旧 4 列核对表)

> 本表由助教代填一次,仅作格式范例;day16 起须你自己闭卷填。代填范围不包含任何未写代码的实现思路——它只回顾你已写下的东西。（内容对齐复验③时的代码）

行=产物里的一个行为;列2=这个行为用到的知识点(往期已学的也写,标明往期);列3=其中你说不出出处、或清单外的写法。**教材章节不在此表里**(那部分参考页由教程与产物壳给,单一出处)。

| 行为(bank_account.py 里的哪个方法在干什么)       | 用到的知识点                                                               | 其中我说不出出处 / 清单外的                                                                                 |
| ------------------------------------------------ | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `__init__` 开户:存姓名、初始余额、写第一条记录 | class、`__init__`、self、实例属性、dict/list(往期第01周)                 | 私有属性 `__xxx`;`datetime.now`(往期只学过 `datetime.date`)                            |
| `deposit` 存钱:>0 才生效,记一笔并返回成败包    | 实例方法、self、if、实例属性读写、dict/list(往期)、`**result` 组装返回包 | 私有属性;`datetime.now`;`**` 解包——归属待确认                                          |
| `withdraw` 取钱:`<=0` 或超余额则拒           | 实例方法、if、比较运算、f-string                                           | 私有属性;`datetime.now`                                                                    |
| `show_history` 逐条打印历史                    | 推导式(往期)、字符串 `join`(往期)、f-string、类属性经类名读取            | `strftime` 格式化(时间已改用本地 `now()`,原 UTC 差 8 小时的问题已消)                                                      |
| `print_result` 按返回包播报成败                | if/else、f-string、实例方法、dict 取值                                     | `**rest` 形参收集 + `**dict` 解包传参——第02周写的是"参数全体系",未展开到具体语法,**归属待确认** |
| `show_user_info` 一行打印谁的/多少钱           | print、f-string、实例方法、类属性经类名读取                             | 无越界(收口时已在主程序两处调用)                                                                            |
| 主程序里创建两个账户                             | class 定义与实例化(无 new)                                                 | 无                                                                                                          |
| 主程序用 `type()` 与 `isinstance()` 各判一次 | `type()`、`isinstance()`                                               | 无                                                                                                          |
| 主程序改类属性后两账户同值                       | 类属性共享                                                                 | 无                                                                                                          |

**学了但没落进任何行为的**:本日五个知识点全部已用 ✓;未落地的是 **`isinstance()` 认子类** 这一半能力——本日无继承结构,产物无法验证它,day16 做继承时才能落地。

**越界留痕(不删代码,按周头口径逐条一行)**:

- 【超前】访问限制(私有属性 `__xxx`) | 出处 廖雪峰 10.2 | 正式归 day17(随 @property 出现) | 影响 `__name`/`__amount`/`__history` 及全部方法;与 day18/20/21 文件持久化有已知冲突
- 【超前】`datetime.now`/`strftime` | 出处 往期仅 day12 学过 `datetime.date` | 正式归待确认(17 周清单未列) | 影响开户/存/取三处时间字段与历史打印时间(现为本地时间;timezone 已移除)
- 【归属待确认】`**` 解包与 `**rest` 形参收集(含两处:组装返回包、主程序调用 `print_result`) | 出处 第02周"参数全体系"未展开清单 | 待确认 | 影响 `print_result` 的定义与主程序四处调用——此项属教程侧欠账,不计你越界
