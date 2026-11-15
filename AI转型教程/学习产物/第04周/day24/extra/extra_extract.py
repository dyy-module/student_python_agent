# ===== day24 跟练任务说明 v3(extra/extra_extract.py,实现由你本人盲写) =====
# 文件:extra_extract.py | ≤60 行 | 第三方库:无(标准库 re)
#
# 【需求】从一段混合文本中提取三类信息并分组打印
#   1 re.findall 提取所有 URL、所有日期(YYYY-MM-DD)、所有中国大陆手机号,分三行 print
#   2 对手机号用 re.search + 分组 print 号段与尾号
#   自证:python extra_extract.py 跑通、每步 print
# 【可用知识点】re.findall、re.search、分组 group()、字符类与量词、原始字符串 r""、for、print、f-string
# 【越界→隔离目录】命名分组/非捕获组 属【超前】,想试放 beyond/
# 【教材·只读N节】复用 day24 主教材;findall 见官方 re 页
# 【交检】跑通、每步 print;extra 与固定产物分离在本 extra/ 目录内
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import re


def parse_phone_date_url(text):
    '''分离 url 日期 手机号'''
    url_re = r'https?://[a-zA-Z0-9.:?/=]+'
    date_re = r'[0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[0-1])' #超前，非捕获组
    phone_re = r'(?<!\d)1[3-9]\d{9}(?!\d)'# 超前，零宽断言
    phone_group = r'(1[3-9][0-9])\d{4}(\d{4})'

    urls = re.findall(url_re, text)
    dates = re.findall(date_re, text)
    phones = re.findall(phone_re, text)
    print(urls)
    print(dates)
    print(phones)
    for p in phones:
        begin,tail = re.match(phone_group,p).groups()
        print(f'号段{begin},尾号{tail}')


if __name__ == '__main__':
    test = """2024-03-15 项目例会纪要：门户地址 https://www.example.com/news/2024 ，镜像地址 http://demo.site.cn/page?id=88 ，
    文档中心 https://docs.example.org/guide 。联系人张三，手机 13812345678 ；李四，手机 15900001111 。请于 2025-01-09 前提交反
    馈，紧急联系电话 18688889999 。上一版发布日期为 2023-12-31 ，请一并核对。"""
    parse_phone_date_url(test)
