# ===== day28 阶段1闸门·周检测任务说明 v3(45min 限时盲写,不看教材/不看本周往期产物) =====
# 文件:news_summary.py | ≤180 行(周末检测放宽) | 第三方库:requests 可用(day22 已解禁)
#
# 【需求】新闻摘要生成器:requests 抓取 → re 清洗提取 → 输出摘要,三合一
#   1 用 requests 抓取一个自选公开新闻页面/接口(GET,必须设 timeout,检查 status_code 为 200 再继续)
#   2 用 re 从返回文本清洗并提取正文或标题(如去 HTML 标签、抽取标题/关键段落),至少用到 findall/search/sub 中的一种以上
#   3 基于提取结果生成摘要(如取前 N 个字符或前若干句),print 输出摘要与其字符数
#   4 用 try/except 兜底网络异常(Timeout/RequestException)与解析异常,任一环节失败都 print 友好提示且程序不崩溃
#   5 主流程跑通一次完整"抓取→清洗→摘要→输出",每步有 print
#   通过标准:45min 内完成、一次跑通无未捕获异常、requests(GET+status_code+timeout)与 re(≥一处提取/替换)用法正确、摘要非空且来自真实抓取、异常分支有兜底、仅用截至 day28 闭包、可用 requests、≤180 行
#   闸门附加:能在 index.md 讲清 Python 与 JS 至少三处差异(建议 包管理 venv/pip vs npm、typing 运行时不强制 vs TS 编译期强制、asyncio.run 手动启动 vs JS 事件循环内建)
# 【可用知识点】requests(day23)、re(day24)、typing(day25,可选)、asyncio(day26,可选)、week03 文件/异常、字符串切片、for/推导式、print、f-string
# 【越界→隔离目录】禁 import json(未首教);aiohttp/httpx/asyncio.gather/aiofiles 属【超前】;限时盲写以"跑通主路径"为先,别在本次尝试超前项
# 【教材·只读N节】检测期间不翻教材;订正阶段回查:requests 廖雪峰页、re 官方页 https://docs.python.org/zh-cn/3/library/re.html
# 【交检】45min 计时;python news_summary.py 一次跑通;每步 print;异常拔网也不崩;index.md 写满三处 Python vs JS 差异 + 末两行自检
# ================= 以下开始限时盲写(壳不得改动下方实现行) =================
import requests
import re
from typing import Optional

re_title_tag = re.compile(r'<h([1-6]){1}>([^<]+)</h[1-6]{1}>')
re_tag = re.compile(r'<[^>]+>')


def read_utl(url: str) -> str:
    '''request 读取文本'''
    try:
        res = requests.get(url, timeout=2)
        res.encoding = 'utf-8'
        if res.status_code != requests.codes.ok:
            res.raise_for_status()
    except requests.HTTPError as err:
        print('网络请求失败', err)
        return ''
    except requests.Timeout:
        print('网络请求超时，请重试')
        return ''
    except requests.RequestException as err:
        print(err)
        return ''
    else:
        print('资料读取成功')
        return res.text


def write_md(path: str, data: str) -> None:
    '''保存清洗完的md'''
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
            print('写入成功')
    except OSError as err:
        print(err)


def get_title(data: str) -> Optional[list[str]]:
    '''获取标题信息'''
    return [r[1] for r in re_title_tag.findall(data)]


def title_format(m: re.Match[str]) -> str:
    '''清理标题等级，h1 对应# h2 对应## h3及更多对应###'''
    level, rest = m.group(1), m.group(2)
    if level == '1':
        return '# '+rest
    elif level == '2':
        return '## '+rest
    else:
        return '### ' + rest


def space_clean(data: str) -> str:
    '''删除多个空行、空格'''
    text = re.sub(r'[ \t]+', ' ', data)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'\n[ \t]+\n', '\n\n', text)
    return text


def clean_html_to_md(data: str) -> str:
    '''
    清洗html,转为md
    清理标题等级，h1 对应# h2 对应## h3及更多对应###
    清理 pre 标题内容，为```python ```
    '''
    re_body = r'<body[^>]*>(.*?)</body>'
    re_script = r'<script[^>]*>.*?</script>'
    clean_other = re.search(re_body, data, flags=re.S)
    if clean_other:
        clean_script = re.sub(
            re_script, '', clean_other.group(1), flags=re.S | re.I)
        clean_title = re_title_tag.sub(title_format, clean_script)
        clean_html = re_tag.sub('', clean_title)
        clean_space = space_clean(clean_html)
        return clean_space
    else:
        return ''


def main(url, path):
    '''主函数，读取链接，清洗文档，写入md'''
    re_url = r"https?://[^\s]+"
    re_path = r'.*?.md$'
    if re.match(re_url, url) != None and re.match(re_path, path) != None:
        content = read_utl(url)
        titles = get_title(content)
        clean_md = clean_html_to_md(content)
        if clean_md:
            write_md(path, clean_md)
            print('文档主要信息:\n', titles)
            a = clean_md[0:300]
            print('摘要：', a, '长度', len(a))
    else:
        print('请检测输入值')


if __name__ == '__main__':
    url = 'https://www.ruanyifeng.com/blog/2026/10/weekly-issue-416.html'
    path = 'C:/Users/aaa/Desktop/test/AI转型教程/学习产物/第04周/day28/weekly-issue-416.md'
    main(url, path)
