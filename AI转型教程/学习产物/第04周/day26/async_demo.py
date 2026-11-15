# ===== day26 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:async_demo.py | ≤120 行 | 第三方库:无(标准库 asyncio);asyncio 本日首教
#
# 【需求】协程执行顺序演示器:让人肉眼看清"顺序 await 是串行"
#   1 用 async def 定义 2-3 个协程,每个内部先 print"开始"、await asyncio.sleep(不同秒数)、再 print"完成"并 return 一个结果
#   2 定义 main 协程,用顺序 await 依次调用这些协程,print 出执行是串行(一个完成才下一个开始)
#   3 用 asyncio.run(main()) 启动(不在协程里、点火事件循环)
#   4 额外:用 print 文字说明"若把 await asyncio.sleep 换成阻塞的 time.sleep 会发生什么"(仅文字,不 import time)
#   自证:python async_demo.py 跑通,开始/完成时序清晰体现串行
# 【可用知识点】async def、await、asyncio.sleep、asyncio.run、协程 return 值、print、f-string
# 【越界→隔离目录】asyncio.gather / create_task / Task 并发编排、aiohttp 异步请求 属【超前】,本日只在注释识别,想试放 day26/beyond/,不写进交检产物
# 【教材·只读N节,读完即停】
#   廖雪峰 23.2 使用asyncio(本日 async def/await/asyncio.run 正式出处):https://liaoxuefeng.com/books/python/async-io/asyncio/index.html
#   ⚠ 勿读 23.1「协程」(async-io/coroutine):那是 yield 老式写法,与产物 async def 完全不同;23.2 下一页即 23.3「使用aiohttp」(【超前】),勿顺翻
#   官方 asyncio 概览:https://docs.python.org/zh-cn/3/library/asyncio.html
# 【交检】跑通、每步 print、时序能证明串行;index.md 末两行自检
# 【加分可选】把两个协程改用注释写出"若并发改成 gather 预计耗时"(gather 本体放 beyond/,不强制进产物)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import asyncio


async def sleep_1():
    '''第一个async'''
    print('第一个开始')
    await asyncio.sleep(1)
    print('第一个结束')
    return '第一个async'


async def sleep_2():
    '''第二个async'''
    print('第二个开始')
    await asyncio.sleep(1)
    print('第二个结束')
    return '第二个async'


async def sleep_3():
    '''第三个async'''
    print('第三个开始')
    await asyncio.sleep(1)
    print('第三个结束')
    return '第三个async'


async def main():
    '''main 函数调用'''
    await sleep_1()
    await sleep_2()
    await sleep_3()
    # 上方会顺序执行
    # "若把 await asyncio.sleep 换成阻塞的 time.sleep。上方打印结果和时间都没有变化，只是会挂起线程，影响其他函数执行
    res = await asyncio.gather(sleep_1(), sleep_2(), sleep_3()) 
    #gather 一次触发三个，打印顺序： 第一个开始 第二个开始 第三个开始 第一个结束 第二个结束 第三个结束
    print('若把 await asyncio.sleep 换成阻塞的 time.sleep。 打印结果会变成顺序的')
    print(res)
    print('调用结尾')

if __name__=='__main__':
    asyncio.run(main())

#