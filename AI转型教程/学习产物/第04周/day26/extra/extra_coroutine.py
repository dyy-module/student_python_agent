# ===== day26 跟练任务说明 v3(extra/extra_coroutine.py,实现由你本人盲写) =====
# 文件:extra_coroutine.py | ≤60 行 | 第三方库:无(标准库 asyncio)
#
# 【需求】两个协程的顺序执行时序演示
#   1 定义两个协程(如"下载"和"解析",各 await asyncio.sleep 模拟耗时),各 print 开始/完成
#   2 在 main 协程中顺序 await 执行,print 出清晰的开始/完成时序
#   3 用 asyncio.run 启动
#   自证:python extra_coroutine.py 跑通、时序体现串行
# 【可用知识点】async def、await、asyncio.sleep、asyncio.run、print、f-string
# 【教材·只读N节】复用 day26 廖雪峰 23.2 使用asyncio 页(勿读 23.1 yield 老写法)
# 【交检】跑通、每步 print;extra 与固定产物分离在本 extra/ 目录内
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import asyncio
import requests
import os  # [超前]
# requests 同步脚本不能用await，open 也是同步


async def download_file(url: str, save_path: str) -> None:
    '''下载文件'''
    print('开始下载了')
    res = requests.get(url, timeout=3)
    with open(save_path, 'wb') as f:
        f.write(res.content)
    await asyncio.sleep(1)
    print('下载完成了')


async def parase_file(file_path: str) -> None:
    '''解析文件'''
    print('开始解析了')
    await asyncio.sleep(1)
    with open(file_path, 'rb') as f:
        print(f.readline())
    print('解析结束')


async def sleep_t(n:int)->None:
    '''展示串行'''
    print(f'{n}开始了')
    await asyncio.sleep(1)
    print(f'{n}结束了')


async def main():
    url = 'https://www.runoob.com/python3/python3-iterator-generator.html'
    current_directory = os.getcwd()  # 拿到的是执行器的文件夹
    save_path = os.path.join(
        current_directory, "python3-iterator-generator.html")
    print(save_path)

    await download_file(url, save_path)
    await parase_file(save_path)

    await asyncio.gather(sleep_t(1),sleep_t(2)) 

if __name__ == '__main__':
    asyncio.run(main())
