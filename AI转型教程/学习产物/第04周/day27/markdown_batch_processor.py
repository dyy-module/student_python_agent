# ===== day27 产物任务说明 v3.1(项目日;实现由你本人盲写于本注释下方) =====
# 文件:markdown_batch_processor.py | 位置:学习产物\第04周\day27\ | ≤150行(项目日,教程口径) | 禁:import json(本周未首教,序列化手写字符串拼接)
#
# 【题目·对齐教程】照抄周教程 Day27「当日产出」:Markdown 批量处理器(项目日,≤150行),分层设计(获取/清洗/存储)
#   准备测试用 .md 源文件(含 HTML 标签/杂乱标题/链接等噪声,自己造数据)放本目录;获取层:遍历指定目录下多个 .md 文件并读入(with open,week03);
#  可选扩展——用 requests 抓取一个公开 md 源(标为可选,离线也能跑主路径)。
#  注:列目录需 os.listdir/glob(标准库 os 本周仅"识别"未正式教,属【超前】最小片段——目录列表可在程序内硬编码文件名规避,或直接用硬编码列表起批,os 欲试用放 day27/beyond/,不判未教先用)
#   清洗层:用 re 对每个文件做至少两项清洗(如去 HTML 标签、规整标题层级、提取或重写链接),用 typing 给清洗函数加参数与返回类型标注
#   存储层:把清洗后的内容批量写入 output 子目录(文件名可加 _clean 后缀),并生成一个汇总(处理文件数、总字符数)print 出来
#   健壮性:用 try/except 保证单个文件读/写/解析失败时 print 警告并跳过,不中断整批处理;python markdown_batch_processor.py 可跑通"多文件读入→清洗→批量写出→汇总"完整闭环
# 【知识点·指针】见教程 Day27「所用知识点清单」段(文件读写/异常=week03、re=day24、typing=day25、for/推导式、str 方法;可选 requests=day23、可选 asyncio=day26,均已学)
# 【越界→隔离目录】aiofiles 真异步文件 IO;asyncio.gather 并发批处理;aiohttp/httpx;json 序列化(出处见教程 Day27【超前】区)——要试放 day27/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day27「教材与章节」段(综合复习,回查各页标注的复习日,勿整章重读)
# 【交检】跑通无报错、每步 print;index.md 末两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【加分可选】用 asyncio 协程包裹单文件处理再顺序 await(复习 day26);或加一行"提取所有链接并计数"报告
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import re
from typing import Tuple, List, Dict, Union
import os


def clean_html_tag(data: str) -> str:
    '''清理html标签'''
    tag_re = r'<[^>]+>'
    return re.sub(tag_re, '', data)


def parse_title(data: str) -> str:
    '''规划md标题，规则：
        第一个为 一级标题 #,如果不是则改为#
        非首个一级标题 替换为 ##
        超过三级 替换为 ###
    '''
    title_re = r'(^#{1,6})\s+(.*)$'
    is_first = False

    def fix_title(m: re.Match[str]) -> str:
        nonlocal is_first
        hashes, rest = m.group(1), m.group(2)
        if not is_first:
            is_first = True
            return '# '+rest
        n = len(hashes)
        if n == 1:
            return '## ' + rest
        elif n > 3:
            return '### '+rest
        else:
            return m.group()

    parts = re.split(r'(```[\s\S]*?```)', data)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(title_re, fix_title, parts[i], flags=re.M)
    return ''.join(parts)


def format_url(data: str) -> Tuple[str, List[str]]:
    '''格式化url, 返回url合集'''
    url_re = r"https?://[^\s\)]+" 
    url_list = []

    def repl(m: re.Match[str]) -> str:
        url = m.group()
        url_list.append(url)
        return f'({url})'

    return re.sub(url_re, repl, data),url_list


def read_md(file_path: str) -> str:
    '''读取文件,返回'''
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print('文件不存在，路径：', file_path)
    else:
        return content
    return None


def write_md(file_path: str, data: str) -> None:
    '''按路径output 写入清理后的文件夹，文件名加_clean'''
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)
    except Exception as err:
        print(err)


def read_path_to_write(file_path: str) -> str:
    '''转换写入文件 名称'''
    base_path = 'C:/Users/aaa/Desktop/test/AI转型教程/学习产物/第04周/day27/output'
    # title_re = r'.*/([^/]+)\.md$'
    # name_m = re.match(title_re, file_path)
    # if write_path:
    #     write_path = f'{base_path}/{name_m.group(1)}_clean.md'
    #     return write_path
    # else:
    #     print('路径解析失败')
    #     return ''
    title = file_path.split('/')[-1].split('.')[0]
    return  f'{base_path}/{title}_clean.md'


def main(file_list) -> Dict[str, Union[str | int]]:
    '''遍历文件路径，读取文件，清理文件内容，然后写为新文件'''
    statistics = []
    for file_path in file_list:
        context = read_md(file_path)
        if context:
            old_len = len(context)
            write_path = read_path_to_write(file_path)
            context = clean_html_tag(context)
            context, urls = format_url(context)
            context = parse_title(context)
            write_md(write_path, context)
            statistics.append({
                "old_path": file_path,
                "new_path": write_path,
                "old_len": old_len,
                "new_len": len(context),
                "urls": urls
            })
    print('批量清理文件，执行完毕')
    return statistics


if __name__ == "__main__":
    files_path = 'C:/Users/aaa/Desktop/test/AI转型教程/周教程'
    paths = os.listdir(files_path)
    result = main([f'{files_path}/{r}' for r in paths if re.match(r'.*?\.md$',r)])
    print('\n'.join(
        [f"文件：{r['new_path']} 清洗{r['old_len']}文字 结果{r['new_len']}" for r in result]))
    print(f"清洗{len(paths)} 个文件，共 {sum([r['old_len'] for r in result])}文字")
    urls = {url for d in result for url in d['urls']}
    print('汇总链接', urls)
