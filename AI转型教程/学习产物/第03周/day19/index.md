# 第03周 · Day19 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言。末尾须做行为-知识点自证表(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
try/except/else/finally
按类型捕获多种异常(FileNotFoundError/PermissionError/ValueError等)与as e取异常对象
异常层次:所有异常继承自Exception
raise主动抛出异常(JS对应throw)
自定义异常类(继承Exception,结合Day16继承)

## 知识点小结

```python
# try/except/else/finally 结构
class CustomErr(Exception):
    ''' 自定义错误 '''
    def __str__(self):
        return '打印的时候访问，错误信息'

try: # try except 结构
    raise CustomErr() # raise 主动报错
except (ValueError, CustomErr) as err: #  except 拦截可以是元组，也可以顺序拦截。
    print(err if err else '这里报错了')
except FileNotFoundError:
    print('阶梯获取错误')
else:
    print('没报错可以走到这里，else可选')
finally:
    print('无论对错，有finally,在结束时都会走到这里')
```
异常层次表
BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ImportCycleError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning


```javascript
    try {
        throw new Error('主动报错信息') // js 主动抛错
    } catch(err) {
        console.log(err?.message || '报错处理') // catch 错误处理
    } finally{
        // 处理完成，无论对错都会走到这里
    }

```

## JS→Python 对照
js try {} catch(err){} finally{} ,没有else 需要自己处理,不能阶梯拦截报错，需自己区分 。 
python try: ... expect(可以有多个expect) Exception(可以为原组，但需要注意拦截属性，子类型在上边，不然匹配到父类错误，子类永远无法触发) as err: ... else: ... finally:... 

js 主动报错 throw new Error('错误信息')
python 主动报错 raise 错位

## 卡点与解决(非必填)
暂无

## 行为-知识点自证表(交检硬项 · 内容本人填)

> 行=safe_reader.py / extra_divider.py 里的一个行为;3 列;表外补一行「当日学了但没落进任何行为的知识点」。用方法/行为名定位,不写行号(加代码行号会漂)。

| 行为 | 用到的知识点 | 其中我说不出出处的 |
|---|---|---|
|safe_reader.py EmptyFileError | 自定义错误类型 EmptyFileError | |
|safe_reader.py safe_reader |try expect else finally 错误拦截结构 | |
|safe_reader.py safe_reader as err | 获取错误信息 | |
|safe_reader.py finally | finally，无论程序失败还是成功，都会执行 | |

表外一行(学了但没落进任何行为的知识点):(待填)

## 今日越界索引(可选,不写不算欠项)
暂无
