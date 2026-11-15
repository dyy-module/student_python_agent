# day18 越界探索日志(自由记录,不交检、不评分)
# 想多读/多试的清单外东西放同目录的 beyond_*.py,这里随手记一句"读了什么、和后面哪天冲突"即可。


# `with` 上下文管理的触发时机

## 完整执行时序

```python
class Demo:
    def __init__(self):
        print("1. __init__：实例化（with 后面的表达式求值时）")

    def __enter__(self):
        print("2. __enter__：进入 with 块之前触发")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("3. __exit__：离开 with 块时触发，无论怎么离开")

with Demo() as d:
    print("--- with 块内代码 ---")

# 输出：
# 1. __init__：实例化（with 后面的表达式求值时）
# 2. __enter__：进入 with 块之前触发
# --- with 块内代码 ---
# 3. __exit__：离开 with 块时触发，无论怎么离开
```

严格顺序是：**求值表达式并实例化 → `__enter__()` → 返回值绑定给 `as` 变量 → 执行块内代码 → `__exit__()`**。

注意区分：实例化发生在 `__enter__` **之前**，`with A() as f` 中绑定给 `f` 的不是 `A()` 实例本身，而是 `__enter__` 的返回值（文件对象返回的正是 `__enter__` 里的 self）。

## `__exit__` 的触发时机：六种离开方式全都触发

`__exit__` 扮演的是 `finally` 的角色，**不管以哪种方式离开 with 块都会执行**：

| 离开方式 | 是否触发 `__exit__` | 三个异常参数 |
|---|---|---|
| 块内代码正常跑完 | ✅ | `(None, None, None)` |
| 块内抛异常 | ✅ | `(异常类, 异常值, traceback)` |
| 块内 `return` 提前返回 | ✅ | `(None, None, None)` |
| 块内 `break` / `continue` | ✅ | `(None, None, None)` |
| 块内 `sys.exit()` | ✅ | `(SystemExit, code, tb)` |
| Ctrl+C（KeyboardInterrupt） | ✅ | `(KeyboardInterrupt, ...)` |

## 异常场景的触发细节

```python
class Demo:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"__exit__ 被触发")
        print(f"exc_type={exc_type}")
        print(f"exc_val={exc_val}")
        return False   # 不吞异常

with Demo():
    print("step 1")
    raise ValueError("出错了")
    print("step 2")    # ← 永远不执行

print("这行也不会执行")  # 异常继续上抛

# 输出：
# step 1
# __exit__ 被触发
# exc_type=<class 'ValueError'>
# exc_val=出错了
# Traceback ... ValueError: 出错了
```

关键点：**异常发生后，异常被“挂起”**——从异常发生的位置直接跳转到 `__exit__`，块内后续代码不执行；`__exit__` 跑完后，整个 with 语句才算结束，再决定异常的命运。

## `__exit__` 返回值决定异常去向

```python
# 返回 True → 吞掉异常，程序若无其事地继续
class Swallow:
    def __enter__(self): return self
    def __exit__(self, *args):
        return True

with Swallow():
    raise ValueError("被吞掉了")
print("正常继续执行")      # ✓ 能打印到

# 返回 False / None → 异常继续向上抛（默认行为）
```

两个进阶细节：

1. **`__exit__` 内部自己抛异常时**，新异常会替换掉块内的原异常，原异常丢失。
2. **不要依赖 `return True` 吞异常做常规流程控制**——它连 `sys.exit()` 的 `SystemExit` 都能吞掉，可能让退出信号失效。

## 常见误区

1. **以为块内不抛异常 `__exit__` 就不执行**——恰恰相反，正常结束是最主要的触发场景（文件 `close()` 就靠它）。

2. **以为 with 块有独立作用域**——没有。`as` 绑定的变量在块外依然存在：
   ```python
   with open("data.txt") as fp:
       content = fp.read()
   print(fp.closed)      # True，变量还能访问
   fp.read()             # 但 IO 操作会报 ValueError: I/O operation on closed file
   ```

3. **以为异常发生在 `__enter__` 里也能被 `__exit__` 兜住**——不能。`__enter__` 抛异常时 `__exit__` 根本不会被调用，因为“进入上下文”这个动作没完成。

4. **`with` 不是 try/except**——它只保证清理（finally 语义），异常处理（except 语义）要靠 `__exit__` 的返回值或外层 try。

## 时序总结图

```
with 表达式 as f:      ← ① 求值表达式、实例化
                       ← ② 调 __enter__()，返回值绑定 f
    块内代码            ← ③ 执行（正常跑完 / return / break / 抛异常 / sys.exit）
                       ← ④ 无论③怎么结束，都调用 __exit__(exc_type, exc_val, exc_tb)
                       ← ⑤ __exit__ 返回 True 吞异常；否则异常继续上抛
```

## 一句话总结

**`__enter__` 在进入 with 块之前触发（实例化之后），`__exit__` 在离开 with 块时必然触发——正常结束、抛异常、return、break、sys.exit 全都逃不掉；无异常时三个参数是 None，有异常时携带异常信息，返回 True 能吞掉异常。**



# `with open()` 组合详解

> 先纠正一下：你写的 `width` 应该是 `with` 的笔误——Python 里没有 `width` 关键字，下面全部按 `with` 来讲。

## 一句话理解两者的关系

**`open` 负责“开门”，`with` 负责“保证关门”**。它们各自独立，但组合起来才是黄金搭档：

```python
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
# 离开这一行时，文件必然已被关闭，数据必然已刷出
```

## 一、先看不用 with 的世界：手动 close 有三种死法

### 死法一：忘了写 close

```python
f = open("data.txt", encoding="utf-8")
content = f.read()
# 代码写着写着忘了 close —— 文件一直被占用，直到进程退出
```

### 死法二：中途抛异常，close 永远执行不到

```python
f = open("data.txt", encoding="utf-8")
content = f.read()
result = 100 / 0          # 💥 ZeroDivisionError
f.close()                 # ← 这行永远不会执行！
```

### 死法三：提前 return 绕过 close

```python
def read_config(path):
    f = open(path, encoding="utf-8")
    content = f.read()
    if not content:
        return {}         # 直接返回，close 被跳过
    f.close()
    return parse(content)
```

### 手动补救：try/finally

```python
f = open("data.txt", encoding="utf-8")
try:
    content = f.read()
finally:
    f.close()             # 无论如何都会执行
```

能写，但每个文件都要套这一层，啰嗦还容易漏。**`with open(...) as f:` 就是这段代码的语法糖，不多也不少。** 看懂这个等价关系，with 就不模糊了。

## 二、with open 的逐步执行时序

```python
with open("data.txt", encoding="utf-8") as f:
    print("块内")
    content = f.read()

print("块外", f.closed)   # True
```

```
执行到 with open("data.txt", encoding="utf-8") as f:
  │
  ├─ ① open(...) 执行 → 文件已打开（此刻就占用了文件描述符），返回文件对象
  ├─ ② 文件对象.__enter__() → 返回自身
  ├─ ③ 返回值绑定给 f          ← f 拿到的是 __enter__ 的返回值
  │
  ├─ ④ 执行块内代码（读写都通过 f）
  │       ↓ 无论正常跑完 / return / break / 抛异常，任何一种离开
  │
  └─ ⑤ 文件对象.__exit__(...) → 内部调用 f.close()
          ├─ 先 flush() 缓冲区 → 数据交给操作系统（呼应之前聊的 buffering）
          └─ 再释放文件描述符
```

注意 ①② 的顺序：**文件在 `__enter__` 之前就已经打开了**——`open()` 这个调用本身就完成了打开动作，`__enter__` 只是走个过场把自己返回去。

## 三、底层到底发生了什么（io 模块源码的简化版）

```python
# 文件对象内部实现，简化示意
class TextIOWrapper:
    def __enter__(self):
        return self            # 返回自己 → 这就是 as f 拿到的 f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()           # 关闭文件（内部先 flush 再释放句柄）
        return False           # 不吞异常，该抛的继续往外抛
```

就这么多。所谓“上下文管理”，对文件对象来说就是：**进门返回自己，出门 close 自己**。

## 四、异常发生时，with 保护了什么

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("关键数据已进入缓冲区")
    raise RuntimeError("中途崩溃")

# 实际发生的五件事：
# 1. RuntimeError 抛出，块内后续代码跳过
# 2. __exit__ 依然被调用 → f.close() 照常执行
# 3. close 内部先 flush → "关键数据"安全交给操作系统，不会丢
# 4. __exit__ 返回 False → RuntimeError 继续向上抛
# 5. 外面没人接住的话，程序照常崩溃报错
```

这正是 with 的价值：**它不阻止异常发生，但保证“临死前文件也是关好的”**。

## 五、为什么文件非关不可（不关的后果）

| 后果 | 说明 |
|---|---|
| 数据丢失 | 写入先进缓冲区，不 close/flush 就崩溃，缓冲数据全丢 |
| 句柄泄漏 | Linux 默认 `ulimit -n` 1024，服务循环开文件不关 → 跑几小时后 `Too many open files` 崩溃 |
| 文件被锁 | Windows 上文件被占用，无法删除、改名 |
| 别人写不进 | 多进程/多程序协作时，占用会阻塞对方 |

## 六、多文件场景的标准写法

```python
# ❌ 旧式嵌套，两层缩进很丑
with open("src.txt", encoding="utf-8") as fin:
    with open("dst.txt", "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line)

# ✅ Python 3.1+：一行挂多个
with open("src.txt", encoding="utf-8") as fin, open("dst.txt", "w", encoding="utf-8") as fout:
    for line in fin:
        fout.write(line)

# ✅ Python 3.10+：可以加括号换行，最清晰
with (
    open("src.txt", encoding="utf-8") as fin,
    open("dst.txt", "w", encoding="utf-8") as fout,
):
    for line in fin:
        fout.write(line)
```

## 七、高频疑问快答

| 疑问 | 答案 |
|---|---|
| with 结束后 `f` 还能用吗 | **变量还能访问**（with 块没有独立作用域），但读写抛 `ValueError: I/O operation on closed file` |
| with 能防“文件不存在”吗 | **不能**。`FileNotFoundError` 发生在 `__enter__` 之前，with 根本还没接管，要靠外层 try/except |
| with 会捕获处理异常吗 | **不会**。它只有 finally 语义（保证关门），没有 except 语义（处理意外） |
| 块内 `return` / `break` 会关门吗 | **会**。任何离开方式都触发 `__exit__` → `close()` |
| 一个 with 能管两个文件吗 | 能，见上文多文件写法，关闭顺序与打开顺序相同 |

验证第一个疑问：

```python
with open("data.txt", encoding="utf-8") as f:
    pass

print(f)          # <_io.TextIOWrapper name='data.txt' ...>  对象还在
print(f.closed)   # True  只是关了
f.read()          # ValueError!
```

## 八、常见错误写法

```python
# ❌ 错误一：把读写写在 with 块外面
with open("data.txt", encoding="utf-8") as f:
    pass
content = f.read()         # ValueError！文件已关

# ❌ 错误二：return 文件对象本身
def load():
    with open("data.txt", encoding="utf-8") as f:
        return f           # 调用方拿到的是已关闭的废对象
# ✅ 正确：return f.read() —— 把内容读出来再返回

# ❌ 错误三：以为 with 能兜住 open 自身的失败
with open("不存在.txt", encoding="utf-8") as f:   # 💥 在这一行就炸了
    ...
```

## 九、真实项目里的标准搭配：with 管关门，try 管意外

```python
try:
    with open("app.log", encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                print(line.strip())
except FileNotFoundError:
    print("日志文件不存在")
except UnicodeDecodeError:
    print("文件编码不对")
```

分工明确：**with 保证“无论出什么事，门都关好”；try/except 负责“出了事之后怎么应对”**。两者各司其职，缺一不可。

## 一句话总结

**`with open(...) as f` = `f = open(...)` + `try:` + `finally: f.close()` 的语法糖——open 负责开门，with 保证无论正常结束、抛异常、return 还是 break 都必然关门（close 内部还会先 flush 缓冲区）；但它不处理异常、也管不了 open 自身的失败，这两件事还得靠 try/except。**