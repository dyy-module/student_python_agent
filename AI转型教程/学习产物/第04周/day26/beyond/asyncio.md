# asyncio API 全景图

asyncio 的 API 量不小，但**日常开发 80% 只用其中 10 个**，其余是低层工具和特殊场景。先给一张分类地图，再逐层展开。

```
asyncio API 地图
├─ 入口层      run() / 事件循环管理
├─ 编排层      sleep / create_task / gather / TaskGroup / timeout  ← 核心
├─ 同步原语    Lock / Event / Semaphore / Condition / Barrier
├─ 数据结构    Queue / PriorityQueue
├─ 逃生舱      to_thread / run_in_executor        ← 和阻塞代码共存
├─ 网络层      open_connection / start_server      ← TCP 编程
├─ 子进程      create_subprocess_exec / shell
└─ 低层        Future / call_soon / run_forever    ← 一般不用碰
```

---

## 一、入口：启动事件循环

| API | 说明 |
|---|---|
| `asyncio.run(main())` | **唯一推荐入口**。建循环→跑协程→关闭，一个程序只调一次 |
| `asyncio.run(main(), debug=True)` | 调试模式：抓“忘了 await"、慢回调警告，排障神器 |
| `asyncio.get_running_loop()` | 在协程内部拿当前循环 |

⚠️ **老代码里的 `get_event_loop()` / `ensure_future()`** 别再用了——前者已弃用(廖老师教程里就有)，后者被 `create_task()` 取代。

```python
# 生产标配:换 uvloop
import uvloop; uvloop.install()
asyncio.run(main())
```

## 二、任务编排(核心区，必须全掌握)

```python
import asyncio

# 1. 让出控制权(不是睡觉!挂定时器后让给循环)
await asyncio.sleep(1)

# 2. 立即并发跑,不等待
task = asyncio.create_task(job(), name="job-1")   # 存住引用!
result = await task                                # 需要结果时再等

# 3. 并发跑一批,等全部完成
results = await asyncio.gather(f1(), f2(), return_exceptions=True)

# 4. 结构化并发(3.11+):一个失败,自动取消其余并抛异常组
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(f1())
    t2 = tg.create_task(f2())
# 出了 with 块,所有任务保证结束,结果在 t1.result()

# 5. 超时控制(3.11+;旧版用 asyncio.wait_for)
async with asyncio.timeout(3):
    await slow_call()

# 6. 谁先完成先处理谁(比如多源竞价取最快)
for coro in asyncio.as_completed([f1(), f2(), f3()]):
    print(await coro)          # 按完成顺序拿到结果

# 7. 保护任务不被连带取消(取消"外层"时保住内部)
await asyncio.shield(critical_save())
```

**gather vs TaskGroup 怎么选**：

| | `gather` | `TaskGroup` (3.11+) |
|---|---|---|
| 错误处理 | 默认抛第一个异常，**其余继续跑**(除非手动取消) | 一个失败→**自动取消全部**，抛异常组 |
| 保证 | 无泄漏保证 | 出了块所有任务必结束(不会泄漏孤儿任务) |
| 建议 | 简单批处理、`return_exceptions=True` 收集结果 | 新代码默认选它(“结构化并发”) |

## 三、并发限流

```python
sem = asyncio.Semaphore(10)          # 最多 10 个并发

async def fetch(url):
    async with sem:
        return await client.get(url)

# 常见变体:分批跑
async def bounded(coro_fns, limit):
    sem = asyncio.Semaphore(limit)
    async def run(fn):
        async with sem:
            return await fn()
    return await asyncio.gather(*[run(fn) for fn in coro_fns])
```

爬虫、批量调第三方 API 必用——不限流就是给对方送 DDOS,对方封你 IP。

## 四、协程间同步原语

**和 `threading` 模块同名同概念，但必须用 `await` / `async with`**(不是可选的，是必须的)：

| 原语 | 典型用法 | 场景 |
|---|---|---|
| `Lock` | `async with lock:` | 多协程改共享结构(虽有 GIL,`await` 间隙仍会交错) |
| `Event` | `await event.wait()` / `event.set()` | 广播“开关打开”：优雅停机、等配置就绪 |
| `Semaphore` | `async with sem:` | 限流(见上) |
| `BoundedSemaphore` | 同上 | 限流 + 防止 release 超次数 |
| `Condition` | `await cond.wait()` / `cond.notify()` | 复杂等待/通知，配合队列用得少 |
| `Barrier` (3.11+) | `await barrier.wait()` | 凑齐 N 个协程一起放行 |

```python
event = asyncio.Event()

async def worker():
    print("就绪,等发令枪")
    await event.wait()
    print("开跑")

async def main():
    tasks = [asyncio.create_task(worker()) for _ in range(3)]
    await asyncio.sleep(1)
    event.set()                      # 一声令下,三个一起跑
    await asyncio.gather(*tasks)
```

## 五、队列(生产者-消费者)

```python
q = asyncio.Queue(maxsize=100)

async def producer():
    for item in range(10):
        await q.put(item)            # 满了自动挂起,不是报错

async def consumer():
    while True:
        item = await q.get()         # 空了自动挂起
        try:
            await process(item)
        finally:
            q.task_done()            # 配合 join() 计数

async def main():
    workers = [asyncio.create_task(consumer()) for _ in range(3)]
    await produce_all()
    await q.join()                   # 等所有条目被处理完
    # 结束时取消 worker ...
```

另有 `PriorityQueue`(按优先级出队)和 `LifoQueue`(栈)。**协程版队列的意义**:`await q.get()` 空了会挂起让出，不会像线程版那样忙等或阻塞线程。

## 六、阻塞代码逃生舱(与旧库共存)

| API | 用途 |
|---|---|
| `await asyncio.to_thread(fn, *args)` (3.9+) | **首选**。把同步阻塞函数丢线程池，不卡事件循环 |
| `loop.run_in_executor(pool, fn, *args)` | 低层版本，可指定自定义池(如进程池跑 CPU 任务) |
| `asyncio.run_coroutine_threadsafe(coro, loop)` | 反方向：**从其他线程**调用协程，拿回 concurrent.futures.Future |

```python
# 事件循环里必须用 requests / 同步 ORM 时的写法
r = await asyncio.to_thread(requests.get, url, timeout=5)

# CPU 密集:线程绕不开 GIL,得进程池
from concurrent.futures import ProcessPoolExecutor
result = await loop.run_in_executor(ProcessPoolPool(), cpu_heavy, data)
```

## 七、网络编程(TCP 流)

```python
# 客户端
reader, writer = await asyncio.open_connection("host", 8080)
writer.write(b"hello\n")
await writer.drain()                 # 写缓冲背压:满了让出
data = await reader.readexactly(4)   # 或 read(n) / readline() / readuntil(b"\n")
writer.close()
await writer.wait_closed()

# 服务端(一个协程一个连接,单线程扛几千连接)
async def handle(reader, writer):
    async for line in reader:
        writer.write(line.upper())
        await writer.drain()

server = await asyncio.start_server(handle, "0.0.0.0", 8080)
async with server:
    await server.serve_forever()
```

这就是上一轮聊的“单线程 + epoll”架构的裸写形态——实际项目直接用 aiohttp/FastAPI,它们底层就是这套。

## 八、子进程

```python
proc = await asyncio.create_subprocess_exec(
    "ls", "-l",
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
)
out, err = await proc.communicate()   # 并发收 stdout/stderr,防管道死锁
```

## 九、低层 API(知道即可，别在业务里用)

- `asyncio.Future` — 结果占位符，Task 的底层(上轮讲过)
- `loop.call_soon(fn)` / `call_later(t, fn)` — 往循环里塞回调/定时器，写框架才会碰
- `loop.run_forever()` — 手写服务器主循环
- `asyncio.eager_task_factory` (3.12+) — 任务急切执行优化，高级调优

---

## 版本速查(决定你能用哪些)

| 版本 | 新增/变化 |
|---|---|
| 3.7 | `run()`、`create_task()`(现代写法起点) |
| 3.9 | `to_thread()` |
| 3.11 | **TaskGroup、timeout()、Barrier**;删除 `@asyncio.coroutine` |
| 3.12 | `wait()` 传协程被弃用;eager task factory |

Python < 3.11 的项目：TaskGroup 换 gather,timeout 换 wait_for(注意它俩异常不同：前者抛 TimeoutError,wait_for 抛 asyncio.TimeoutError,3.11 后统一了)。

## 只背这 10 个，够写 90% 的代码

```
run / sleep / create_task / gather / TaskGroup
timeout / Semaphore / Queue / to_thread / Lock+Event
```

## 一个排障技巧收尾

开发期永远开着 debug 模式跑：

```python
asyncio.run(main(), debug=True)
# 或环境变量 PYTHONASYNCIODEBUG=1
```

它会告诉你：哪个协程**从没被 await**(“coroutine was never awaited”)、哪个回调**跑了超过 100ms**(阻塞了循环——八成是谁在循环里用了 requests)。上次说的“四大坑”，它一个能抓俩。

