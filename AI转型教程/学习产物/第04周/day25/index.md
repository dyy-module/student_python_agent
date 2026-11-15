# day25 学习笔记(学习者本人填写)

> 口径:标 `python` 的代码块须纯 Python 且可直接运行。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题

### typing
python 的 类型提示 工具包，v3.5 引入。
v3.9 list[int] 替代 typing.List，dict[T] 替代 Dict[T]
v3.10 int | None 替代 Optional, int | str 替代 typing.Union
typing 模块仍保留 Any、Callable、TypeVar、Literal、TypedDict、Protocol 等功能 #[超前]

```python
from typing import Optional,List,Dict,Callable,Any,Protocol,TypedDict,Literal # 导入typing 内容

def count_word(d:List[str])->Dict[str,int]: # List,Dict 类型定义
    pass

def get_word_count(d: Dict[str, int], key: str) -> Optional[int]:  # Optional 类型定义
    pass

# Callable[[参数类型列表], 返回类型]
# [超前][...,Any] 接收返回任意参数，... 表示任意参数，Any 为返回值。func_t 返回一个函数，接收int,str 两个参数，返回一个str
#  Callable[[], None] 无参、无返回值（最简回调）
# 一个容易忽略的点：类也满足 Callable
def func_t(func:Callable[...,Any])-> Callable[[int,str],str]: 
    pass

# 需要精确表达复杂签名时，用 Protocol 定义 __call__：[超前]
class AreaFn(Protocol):
    def __call__(self, *, width: float, height: float = 1.0) -> float:
        pass

def compute(fn: AreaFn) -> float:
    return fn(width=3.0, height=4.0)

# 字典的字段级类型提示 [超前]
class User(TypedDict): 
    id: int; 
    name: str;
u: User = {"id": 1, "name": "Alice"} 
# 限定字面量取值,key 只能是 id  name [超前]
def get_user_by_key(d:User,key:Literal['id','name']):
    pass

```
### 运行时不强制
零运行开销，不检查，不报错。
作用：
1.静态检查器 运行检测bug
2. IDE 智能支持 mypy/Pylance
3. 当作文档



## TS↔typing 对照表
<待填写:number[]↔List[int]、Record↔Dict、X|null↔Optional[X]、(x:number)=>number↔Callable[[int],int]、编译期强制↔运行时不强制>
ts (number|str)[] -> python List[Union[int, str]]
ts `Record<string, number>` → Python `Dict[str, int]`
ts `string | null` → Python `Optional[str]`;
ts `A | B` → Python `Union[A, B]` 3.10 后 `A | B`
ts `(x: number) => number` → Python `Callable[[int], int]`
ts 编译期强制类型 → Python 运行时**不**强制(仅注解,靠 mypy/IDE 检查)

## 两行自检
- ①我说不出出处的知识点: 无
- ②学了但没落进任何行为的知识点:
  Literal、TypedDict、Protocol

## 卡点与解决(非必填)
<可留空>
