# ===== day27 跟练任务说明 v3.1(extra\extra_md_stats.py,实现由你本人盲写) =====
# 文件:extra_md_stats.py | 位置:学习产物\第04周\day27\extra\ | 第三方库:无(标准库 re + week03 文件读写)
#
# 【题目·对齐教程】照抄周教程 Day27「跟练清单」:读取一个本地 .md 文件,用 re 统计并 print——一级/二级标题(#)数量、
# Markdown 链接 []() 数量、代码块 ``` 数量,练习正则计数。
# 【知识点·指针】with open/read(week03)、re.findall/search(day24)、len/print/f-string,均在教程 Day27「所用知识点清单」内
# 【越界→隔离目录】跨行代码块匹配如需 re.DOTALL 等 flag(本周未教,属【超前】识别项)——要试放 day27/beyond/
# 【教材·只读】精读页见周教程 Day27「教材与章节」段(复习 day24 re 官方页 findall 词条即可)
# 【交检】python extra_md_stats.py 跑通、每步 print;open 显式 encoding(week03 规范);与固定产物分离在本 extra/ 目录;index.md 两行自检覆盖到本文件
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from typing import TypedDict
import re


class Count_md(TypedDict):#[超前]TypedDict
    '''定义统计输出模型'''
    first_title: int
    second_title: int
    url: int
    parentheses: int
    code_block: int


def parase_md(data: str) -> Count_md:
    '''解析读取的md,并统计'''
    first_title_re = r'^# '
    second_title_re = r'^## (?!#)'#[超前] 断言
    url_re = r'https?://[^\s]+'
    parentheses_re = r'\[.*?\]|\(\S*?\)'
    code_block_re = r'```[\s\S]*?```'

    first_title = re.findall(first_title_re, data, re.M)#[超前] 逐行
    second_title = re.findall(second_title_re, data, re.M)#[超前] 逐行
    url = re.findall(url_re, data)
    parentheses = re.findall(parentheses_re, data)
    code_block = re.findall(code_block_re, data)

    return {
        "first_title":len(first_title),
        "second_title":len(second_title),
        "url":len(url),
        "parentheses":len(parentheses),
        "code_block":len(code_block)
    }


def read_md(path: str) -> Count_md:
    '''读取md文档，并统计'''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            result =parase_md(md_content)
    except FileNotFoundError:
        print('文件不存在')
    except (ValueError, TypeError) as err:
        print('解析问题：', err)
    except Exception as err:
        print(err)
    else:
        return result

if __name__ =='__main__':
    path = 'C:/Users/aaa/Desktop/test/AI转型教程/周教程/第03周_OOP文件异常_day15-21.md'
    result = read_md(path)
    print('一级标题：',result['first_title'],'个')
    print('二级标题：',result['second_title'],'个')
    print('url：',result['url'],'个')
    print('括号：',result['parentheses'],'个')
    print('代码块：',result['code_block'],'个')