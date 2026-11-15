# ===== day23 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:http_fetcher.py | 位置:day23\ | ≤120 行 | 禁:aiohttp/httpx 异步库、独立 import json(【超前】)
#
# 【题目·逐字抄自教程「当日产出」】编写 http_fetcher.py:健壮 HTTP 抓取器(≤120行)
#   用 requests.get 抓取一个自选公开接口/页面,必须设置 timeout,并检查 status_code
#   成功分支:print 状态码、Content-Type 响应头、正文前若干字符(text 切片);若响应为 JSON 则用 .json() 取出并 print 其中一个字段
#   演示一次带查询参数(params)的 GET,print 拼接后的最终 URL
#   用 try/except 分别捕获 Timeout 与 RequestException,print 友好错误信息,程序不崩溃
#   知识点清单/讲解示例见周教程 Day23「学习内容」「讲解」「所用知识点清单」段(指针,本壳不复述)
# 【越界→隔离目录】aiohttp/httpx(【超前】);raise_for_status(本日只教识别、产出不强制,教程 Day23【超前】区)→欲试用放 day23/beyond/,放对目录即留痕
# 【教材·只读】见周教程 Day23「教材与章节」段(主教材廖雪峰 17.2 requests);⚠17.2 下一页 17.3 chardet/17.4 psutil 非本周项,勿顺翻
# 【交检】python http_fetcher.py 跑通无报错、每步 print;补 index.md 覆盖全部学习内容+末两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【加分可选】同一 URL 对比 r.text 与 r.json() 差别,文字写进 index.md,不进产物
# 【复验待修】2026-10-31 第三轮：已闭环——P1 补 res.text[:80]、P2 去 with与孤儿pass、P3 headers.items() 含值打印(含 Content-Type)均落实;实测跑通。本轮无待修项
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import requests


def test_get():
    try:
        url = 'https://api.github.com/events'
        params = {'version': 1, 'test': 2}
        res = requests.get(url, params=params, timeout=2)
        res.raise_for_status()
        print(res.status_code)
        print(f'最终URL{res.url}')
        print(res.text[:80])
        data = res.json()
        if data and data[0] and data[0]['id']:
            print(data[0]['id'])
        
        for hd in res.headers.items():
            print(f'{hd[0]} {hd[1]}')
    except requests.exceptions.Timeout:
        print('请求超时')
    except requests.exceptions.HTTPError as err:
        print(err.response.status_code)
    except requests.RequestException as err:
        print(err)
    except (TypeError, IndexError) as err:
        print(err)
# data[0] data不存在会被TypeError 接住, data[0] 不存在会被IndexError接住

def test_post():
    try:
        payload = {'key1': 'value1', 'key2': 'value2'}
        r= requests.post("http://httpbin.org/post", data=payload, timeout=2)
        r.raise_for_status()
        print(r.text)
        print(r.cookies)
    except requests.exceptions.Timeout:
        print('请求超时')
    except requests.RequestException as err:
        print(err)
    except TypeError as err:
        print(err)


if __name__ == '__main__':
    test_get()
    test_post()
