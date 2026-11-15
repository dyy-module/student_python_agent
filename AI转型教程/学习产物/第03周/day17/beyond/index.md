
## 什么是专有方法

专有方法，又称**魔术方法**，命名固定为 `__名字__` 形式，两个核心特征：

1. **由解释器在特定时机自动调用**——你几乎从不手动调 `obj.__str__()`，而是调 `str(obj)`，解释器再去触发它
2. 是 Python 实现**协议**的方式——定义了它们，你的对象就能“伪装”成内置类型，支持 `+`、`[]`、`in`、`for`、`with` 等原生语法

你前两轮用到的 `__init__`、`__getattr__`、`__call__`、`__str__`、`__repr__` 都属于这个体系。

## 总览：语法 → 触发的方法

| 你写的语法 | 触发的方法 |
|------|------|
| `ClassName(...)` | `__new__` → `__init__` |
| `print(obj)` / `str(obj)` | `__str__` |
| 交互式回显 / `repr(obj)` | `__repr__` |
| `obj.attr`（常规查找**失败后**） | `__getattr__` |
| `obj.attr`（**所有**访问都拦） | `__getattribute__` |
| `obj.attr = v` / `del obj.attr` | `__setattr__` / `__delattr__` |
| `obj(...)` | `__call__` |
| `len(obj)` | `__len__` |
| `obj[k]` / `obj[k]=v` / `del obj[k]` | `__getitem__` / `__setitem__` / `__delitem__` |
| `for x in obj` | `__iter__` + `__next__` |
| `x in obj` | `__contains__` |
| `obj + other`（`- * / % **` 同理） | `__add__` 等一整族 |
| `obj == other` / `<` `<=` `>` `>=` | `__eq__` / `__lt__` `__le__` `__gt__` `__ge__` |
| `bool(obj)` / `if obj:` | `__bool__` |
| `hash(obj)`、放入 dict/set | `__hash__` |
| `int(obj)` / `float(obj)` | `__int__` / `__float__` |
| `with obj as x:` | `__enter__` / `__exit__` |
| `del obj`（引用归零时） | `__del__` |
| `f"{obj:spec}"` | `__format__` |

## 分组详解

### 1. 生命周期

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

单例模式就是靠重写 `__new__` 控制只创建一次。

### 2. `__str__` vs `__repr__`

| | `__str__` | `__repr__` |
|---|---|---|
| 触发 | `print()`、`str()` | 交互式回显、`repr()`、打印容器里的元素 |
| 受众 | 用户 | 开发者，理想情况是“能还原对象”的代码 |
| 未定义时 | 退回用 `__repr__` | 退回默认的 `<Demo object at 0x...>` |

Chain 例子里的 `__repr__ = __str__` 就是一箭双雕：`print()` 好看，在解释器里直接敲变量名也好看。

### 3. 属性访问（你踩过的坑就在这组）

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

三条铁律：
- `__getattr__` 是兜底：实例字典里**找得到**就不会触发它
- `__getattribute__` 拦截一切，内部任何 `self.xxx` 都会再次触发它自己，必须用 `super()` 委托
- `__setattr__` 内部赋值同理，要么 `super().__setattr__()`，要么直接操作 `self.__dict__`

### 4. 可调用 `__call__`

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

这就是 `Chain().users('michael')` 能成立的机制。判断可调用性用内置函数 `callable(obj)`。

### 5. 运算符重载

```python
from functools import total_ordering

@total_ordering                # 只写 __eq__ + 一个方向，其余四个自动补全
class Money:
    def __init__(self, v): self.v = v
    def __eq__(self, other): return self.v == other.v
    def __lt__(self, other): return self.v < other.v

class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o):        # v1 + v2
        return Vector(self.x + o.x, self.y + o.y)
    def __mul__(self, k):        # v * 3
        return Vector(self.x * k, self.y * k)
    __rmul__ = __mul__           # 3 * v：左操作数不支持时反向找它
```

另有增强赋值族 `__iadd__`（`+=`）、一元运算 `__neg__`（`-v`）、`__abs__`（`abs(v)`）等，规律一致。

### 6. 容器与迭代

```python
class Playlist:
    def __init__(self, *songs): self.songs = list(songs)

    def __len__(self): return len(self.songs)          # len(p)
    def __getitem__(self, i): return self.songs[i]     # p[0]、p[1:3]
    def __setitem__(self, i, s): self.songs[i] = s     # p[0] = s
    def __contains__(self, s): return s in self.songs  # 'x' in p
    def __iter__(self): return iter(self.songs)        # for s in p
```

只定义 `__getitem__` 也能支持 for 循环——解释器会按索引 0、1、2……依次取值直到 `IndexError`。

### 7. 上下文管理器

```python
import time

class Timer:
    def __enter__(self):              # 进入 with，返回值绑给 as
        self.t = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):   # 离开时（即使有异常）
        print('耗时', time.time() - self.t)
        return False                  # 返回 True 表示吞掉异常
```

这是 `with open(...) as f:` 背后的机制，也是替代 `__del__` 管理资源的**正确姿势**。

### 8. 布尔与哈希

- `if obj:` 先找 `__bool__`，没有就看 `__len__`（长度 0 为假），两者都没有则恒为真
- 定义了 `__eq__` 却不定义 `__hash__`，对象会自动不可哈希（无法放入 `set`、不能当 dict 键）——需要时补上 `__hash__ = hash(self.v)` 之类

## 常见坑

1. **别自造 dunder**：只有 Python 认识的名字才会被自动调用，自己发明 `__myhook__` 永远不会触发，还可能撞上未来版本
2. **递归陷阱**：`__getattribute__`、`__setattr__`、`__delattr__` 内部访问自身属性必须走 `super()`
3. **`__del__` 不可靠**：解释器退出时不保证调用，关闭文件/连接请用 `with` + `__exit__`
4. **`__str__`/`__repr__` 必须返回 `str`**，返回 `None` 或其他类型会报错
5. 定义 `__eq__` 影响的是 `==`；`is` 永远比较身份，不受任何魔术方法控制

一句话总结：**魔术方法是 Python 的“操作符接口”**——你在 Chain 里写的 `__getattr__`（属性链）、`__call__`（带参调用）、`__str__`（打印路径），正是靠这套接口把普通对象变成了能自然书写的“小语言”。