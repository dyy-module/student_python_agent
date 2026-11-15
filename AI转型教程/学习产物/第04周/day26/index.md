# day26 学习笔记(学习者本人填写)

> 口径:标 `python` 的代码块须纯 Python 且可直接运行。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题

### 什么是asyncio
是python 用于处理异步 I/O的框架，用来在单线程内并发执行"需要等待"的任务。
### 为什么需要它
同步代码遇到网络请求、文件读写、数据库查询等会阻塞线程，进行等待。而异步I/O可以在这段时间执行其他的代码。
实现高并发，节省内存

```python
import asyncio # 引入模块

async def test1(): # async 定义协程 可以被事件循环暂停和恢复
    print('开始')
    await asyncio.sleep(1) # await 等待协程，告诉事件循环可以执行其他东西
    print('结束')

async def main(): # 一般结构，用main 统一调用协程
    #test1() 协程函数 前面不加await 不会执行，会报RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    await test1()
    await test1()
    #  并行执行，串行打印结果 ：开始（约1秒） 结束 开始（约1秒） 结束
    await asyncio.gather(test1(),test1())
    # gather 会同时触发多个协程，打印结果：开始  开始（约1秒） 结束 结束

asyncio.run(main()) # 协程触发器，启动事件循环
# 作用：
# 检查有没有准备好的异步任务
# 执行这些任务
# 处理网络 IO、定时器等各种事件

```

## JS↔asyncio 对照
<待填写:async function↔async def、事件循环内建↔必须asyncio.run手动点火、setTimeout↔await asyncio.sleep(time.sleep会阻塞)、调async返回Promise会执行↔调协程返回coroutine不await不执行>

js async function a... ->py async def a ...
js 协程等待 await a ... ->py await a ...
js 调用协程 a() 事件循环运行时内建、直接调 async 函数 -> py asyncio.run(a()) 需要专门的循环触发器
js setTimeout(()=>{},n) -> py await asyncio.sleep(n)
js promise.all([a,b]),入参数组，放入promise即可 -> py await asyncio.gather(a(),b()) ，一个一个逗号分隔，带()
js 调 async 函数返回 Promise(会开始执行)→ Python 调协程返回 coroutine 对象(不 await 不执行)

## 两行自检
- ①我说不出出处的知识点:无
- ②学了但没落进任何行为的知识点:无

## 卡点与解决(非必填)
<可留空>
