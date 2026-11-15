# 第03周 · Day20 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条,2026-10-24 现行口径)。

## 今日主题
class 创建/实例，__init__ 方法/self 实例属性/魔术方法
class 继承/super方法调用链/多态/isinstance/isssubclass/type
open文件读取,with 函数兜底错误
try expect else finally 错误处理
错误类型 BaseException 类

## 知识点小结
### class
```python
    class Test(object): # 类创建，py3可以不写(object),行为和写了一致
        '''讲解Test 类定义'''
        class_public_prop ='class_public_prop' # 类公共属性，所有实例共享
        def __init__(self,name,value): # 魔术方法init,在类实例时被调用,首个参数 self
            # self 指向创建的实例本身
            self.__name = name # 定义实例私有属性，实例无法直接访问（并非完全不能访问，只是被改了名字），只能通过方法访问（超前）
            self.value = value # 实例属性，可被直接访问
        
        def get_name(self): # 方法必须self作为默认参数，可接收其他参数
            return self.__name

        def set_name(self,name):
            self.__name =name

        def __str__(self): # 魔术方法 print/str/f""触发 面向用户返回
            return '自定义'
        
        def __repr__(self):# repr(obj)/f"{obj!r}"/print([obj, obj]) 触发，主要面向开发者定位错误
            return '自定义'
        
        def __lt__(self,other):# 魔术方法，< 访问时，或者sorted 访问时，返回bool.
            return True
        # def __gt__(self,other) # >触发 sorted reverse=True 时
        # def __eq__(self,other) # = 触发，返回bool


        # __del__# 对象被垃圾回收时调用，但不保证一定执行（循环引用、解释器退出等），不要依赖它释放关键资源，应优先使用上下文管理器。
        # __format__ —— 支持 format 规范
        def __len__(self): # len()函数触发
            return 5

        def __getitem__(self, index):# 访问属性
        return self._data[index]      

        def __setitem__(self, index, value):# 设置属性
        self._data[index] = value

        def __iter__(self): # 迭代生成器， iter + next
        return self

        def __next__(self):
            if self.current <= 0:
                raise StopIteration
            self.current -= 1
            return self.current + 1
        
        def __getattr__(self, name): # 查询属性， 只有普通查找失败时才会进来
            if name.startswith("_"):
                raise AttributeError(name)
            value = f"computed-{name}"
            self._cache[name] = value
            return value
        # def __getattribute__(self, name):#所有属性都会进来
        
    class ExtendTest(Test):
        '''类继承 Extend_Test 是Test 的子类'''
        def __init__(self): 
            super().__init__('小明','18岁') # super 字段调用父类__init__ 初始化。定义__init__ 的话一定要调用，不调用会有很多问题，见下文
    
        def get_name(self): # 同名复写方法
            base_name = super().get_name() # super 可直接调用基类方法，然后再此基础上扩展
            return base_name+'扩展'
    
    class ExtendTestMore(ExtendTest): # 继承ExtendTest 的类
        # 不定义 __init__ 运行时 python会自定补全
        pass

    test2 = ExtendTestMore()
    print(type(test2) is ExtendTest) # True type 只是比较，只能比较是不是，不会追溯链
    print(type(test2) is Test) # false

    print(isinstance(test2,ExtendTest)) # True isinstance 可以用来判断类是否在实例继承链上
    print(isinstance(test2,Test)) # True

    print(issubclass(ExtendTestMore,ExtendTest)) # True issubclass 对比的是类本身，不能对比实例与类
    print(issubclass(ExtendTestMore,Test)) # True

```

类别	方法	说明
构造	__new__ / __init__ / __del__	创建 / 初始化 / 析构
表示	__repr__ / __str__ / __format__	开发者表示 / 用户表示 / 格式化
比较	__eq__ __ne__ __lt__ __le__ __gt__ __ge__ __hash__	比较与哈希
算术	__add__ __sub__ __mul__ … __radd__ … __iadd__	运算 / 反射 / 原地
容器	__len__ __getitem__ __setitem__ __delitem__ __contains__	序列语义
迭代	__iter__ __next__ __reversed__	for 循环
属性	__getattr__ __setattr__ __delattr__ __getattribute__	属性拦截
上下文	__enter__ __exit__	with 语句
可调用	__call__	实例当函数用
转换	__int__ __float__ __bool__ __index__	类型转换

实践建议
至少实现 __repr__，调试时价值巨大。

__eq__ 与 __hash__ 成对定义，避免对象意外不可哈希。

运算方法返回 NotImplemented，而不是 NotImplementedError。

别轻易重写 __getattribute__，容易造成递归和性能问题，优先用 __getattr__。

__init__ 里别做耗时 IO，把副作用放到显式方法或上下文管理器里。

__del__ 不可靠，资源释放用 with / contextmanager。

__slots__ 谨慎使用，会破坏动态属性，也会让 __getattr__ 等行为变化。

#### Q: 子类不调用 super().__init__() 会怎样 
 W: 情况1： 子类根本没定义 __init__ —— 没问题。这种情况 Python 会直接用父类的 __init__，等价于调用了。
 W: 情况2： 子类定义了 __init__ 但没调 super().__init__()
           1. 父类实例属性缺失 → 延迟的 AttributeError。构造时不报错，等某个方法访问 self.items 时才崩，堆栈离真正原因很远
           2. 父类的"副作用"丢失 
              父类 __init__ 往往不只是设属性，还做注册、资源分配、校验、启动后台任务
              这类 bug 不会立刻报错，表现为"插件就是不生效""连接池少一个连接"，排查成本高。
           3. 父类的不变量/校验被绕过
 W: 情况1： 调了但用的是 Base.__init__(self) 而非 super()。
            多继承（协作式继承）链断裂

            是 super() 而非 Base.__init__(self) 的核心价值：super() 沿 MRO 调用下一个类，让所有基类的 __init__ 都参与一次。
            Base.__init__(self) 会在链式多继承的时候，多次触发基类__init__ 造成数据相互覆盖。


### open 与 with
```python
    try:
        f = open('x.txt','r',encoding='utf-8')
        print(f.read())
    finally:
        if f:
            f.close()

    # 等价于上方写法
    with open('x.txt','r',encoding='utf-8') as f:
        print(f.read())

```
open(file,mode='r',buffering=-1,encoding=None,error=None,newline=None,closefd=True,opener=None)
file mode encoding 常用
errors: 偶尔用 报错级别，用于处理脏数据，设施是否报错方式
buffering: 特殊需求 设置缓冲 .日志实时性、性能调优

    **with 的优越性**:上下文管理器在代码块退出时无论正常还是报错都会自动调用清理(文件 close),不依赖手写 `f.close()`。好处=①少嵌套、更简洁;②不会因为中断路径漏写 close 致文件句柄泄漏/未刷盘。

with 的执行时机见：AI转型教程\学习产物\第03周\day18\beyond\with.md

#### try except else finally rasise
```python

class CustomErr(Exception):  # 自定义错误，所有错误都继承错误基类Exception
    def __str__():
        return '自定义错误信息'


try:
    with open('a.txt', 'r', encoding='utf-8') as f:
        for l in f:
            print(f)
        raise CustomErr()  # raise 主动抛错

except CustomErr:
    print('处理错误')
except (FileNotFoundError, FileExistsError) as err:  # except 接收错误类型，可以是元组
    print(err)
except OSError:  # 可以有多个 except，顺序匹配，直到匹配到一个或者没有错。但要 细分的放前面，不然匹配到基类错误，就永远走不到细分错误
    print('自定义')
else:
    print('try 块代码没有报错，就会走到这里，可选。适合处理依赖 try 数据的操作')
finally:
    print('无论报不报错，都会走这里')

```


## JS→Python 对照
js 创建 class A{} 继承 class B extend A{} -> python 创建 class A: 继承 class B(A):
js class 构造器 contructor(){} -> python __init__
js class this指向实例 是动态加入的，所以类方法不需要传入首个参数 -> python self指向实例，方法首个参数需要传self,因为他不是动态注入的，实例的时候就会确定
js fs.readFileSync(p,'utf8') → Python with open(p, encoding='utf-8') as f: f.read()
js fs.writeFileSync(p,s) → Python with open(p,'w',encoding='utf-8') as f: f.write(s)
js 手动fd.close() → Python with自动关闭
js line.trim() → Python line.strip()
js try{} catch(e){} finally{} 错误需要自己分类处理 -> python try expect else finally  expect 可以细分错误类型


## 卡点与解决(非必填)
<待填写>

## 两行自检(交检硬项 · 内容本人填,2026-10-24 v1.8 现行口径)

> 不誊行为表,行为-知识点对账由助教读产物完成。只写两行:

- 我说不出出处的知识点:暂无
- 学了但没落进任何行为的知识点:自定义错误类型 day19已落

## 今日越界索引(可选,不写不算欠项)
暂无
