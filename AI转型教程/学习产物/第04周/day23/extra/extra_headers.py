# ===== day23 跟练任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_headers.py | 位置:day23\extra\ | 行数从简 | 禁:aiohttp/httpx 异步库、独立 import json(【超前】)
#
# 【题目·逐字抄自教程「跟练清单」】用 requests 抓取一个公开地址,打印全部响应头(遍历 headers);
#   再用自定义 headers(如 User-Agent)发起一次请求,print 状态码,体会请求头的作用
#   知识点/教材见周教程 Day23 对应段(指针,本壳不复述) 
# 【越界→隔离目录】Session/代理/重试(教程未讲,属更高范围)→放 day23/beyond/,放对目录即留痕
# 【教材·只读】同 http_fetcher.py:周教程 Day23「教材与章节」段(廖雪峰 17.2 requests 的 headers 段)
# 【交检】python extra_headers.py 跑通无报错、每步 print;与固定产物分离在本 extra/ 目录内
# 【复验待修】2026-10-31 第三轮：已闭环——timeout、404 走 HTTPError 分支 print 状态码、第二块补 RequestException 均落实;实测跑通。with requests.get 属识别项不扣分
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import requests

try:
    with requests.get('https://api.github.com/events',timeout=2) as res:
        res.raise_for_status()
        print(res.status_code)
        for i in res.headers:
            print(i)
except requests.exceptions.HTTPError as err:
    print(err.response.status_code)
except requests.exceptions.RequestException as err:
    print(err)
    

try:
    url='https://api.github.com/some/endpoint'
    headers = {'user-agent': 'my-app/0.0.1'}
    with requests.get(url, headers=headers,timeout=2) as res:
        res.raise_for_status()
        for i in res.headers:
            print(i)
except requests.exceptions.Timeout:
    print('超时了')
except requests.exceptions.HTTPError as err:
    print(err.response.status_code)
except requests.exceptions.RequestException as err:
    print(err)


