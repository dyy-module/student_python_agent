# ===== day18 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:file_reader.py | ≤120 行 | 禁:第三方库(Day22前)、try/except(归day19)
#
# 【需求】文本文件统计器:程序自己先生成一个测试文本,再读回来做统计,练熟三种文件模式与逐行遍历
#   1 先用写模式生成 sample.txt,写入若干行(含中英文、含至少一个空行)
#   2 再用读模式打开,统计并 print:总行数、总字符数、非空行数、最长的那一行
#   3 读取用逐行遍历文件对象的方式(不要一次性 readlines 全塞进内存)
#   4 用追加模式再写入一行后重新统计,验证行数变多了
#   自证:python file_reader.py 一次跑通;靠"先写后读"保证文件必存在(本日不处理"文件不存在",留给 day19);四个统计值都有可见输出;追加前后行数差 1
# 【可用知识点】open、with、文件模式 r/w/a、encoding='utf-8'、for line in f、str.strip()、len()、+=、print、f-string
# 【越界→隔离目录】本日无高发项;若想试 pathlib/Path 或其它未列出的文件 API,放 day18/beyond/,别写进本产物(放对目录即留痕,不用填表)
# 【教材·只读,读完即停】liaoxuefeng.com/books/python/io/file/index.html(13.1:open/with/read/readline/readlines/for-line/encoding/write 全讲到)
#   ⚠ 13.1 读完即停、勿顺翻(同章往后是 Path/操作文件夹=未学);速查另参 官方 tutorial 7.2、菜鸟 python3-file-methods.html
# 【交检】跑通无报错、每步 print;index.md 末做行为-知识点自证表(行=一个行为,3列)+表外一行差集;不誊教材章节
# 【加分可选】再统计词数(用字符串方法切分);打印每行时带上行号(enumerate)
# ================= 以下开始盲写(壳不得改动下方实现行) =================\
    
    
class FileReader:
    def __init__(self,file_path):
        self.file_path = file_path
    
    def write_art(self,article):
        '''根据内容，写入文件'''
        with open(self.file_path,'w',encoding='utf-8') as f:
            f.write(f'''{article}''')
            
    def write_art_lines(self,artList):
        '''一次写入多行'''
        if isinstance(artList,list):
            with open(self.file_path,'a',encoding='utf-8') as f:
                f.writelines(artList)
        
    
    def read_art(self):
        '''读取文章'''
        with open(self.file_path,'r',encoding='utf-8') as f:
            for l in f:
                print(l,end='')
    
    def sum_art(self):
        '''统计文章'''
        with open(self.file_path,'r',encoding='utf-8') as f:
            # lines = [l for l in f]
            # print(f'总行数{len(lines)}')
            # print(f'总字符数{sum(len(r) for r in lines)}')
            # print(f"非空行数{len([r for r in lines if r.strip() !=''])}")
            # sort_lines = sorted(lines,key=lambda r: len(r),reverse=True)
            # print(f'最长的行: {sort_lines[0]}',end='')
            total_line = 0
            total_word = 0
            total_empty_line = 0
            max_line_text = ''
            for l in f:
                total_line += 1
                total_word += len(l)
                if l.strip() == '':
                    total_empty_line += 1
                if len(l) > len(max_line_text):
                    max_line_text = l

            print(f'总行数{total_line}')
            print(f'总字符数{total_word}')
            print(f"非空行数{total_line - total_empty_line}")
            print(f'最长的行: {max_line_text}',end='')

if __name__ =='__main__':
    file_a= FileReader('sample.txt')
    file_a.write_art('''Caveats:
# Text mode with universal newlines: '\r\n' is translated to '\n', so counting '\n' in text mode gives logical lines.
# Last line without trailing '\n': sum(1 for _ in f) counts it correctly, but read().count('\n') doesn't. Need to add 1 if last char isn't '\n' and file non-empty.
# Character vs byte: len() on text-mode string counts characters (Chinese chars count as 1 each); binary mode counts bytes (UTF-8 Chinese char = 3 bytes).
# wc -l counts newlines, not lines, same caveat.
# Also mention os.path.getsize() for file size in bytes without opening.
# f.tell() after reading whole file in text mode? tell() returns opaque number in text mode, not reliable for char count. In binary mode tell() gives byte offset.
# Edge cases:

# Empty file: 0 lines, 0 chars.
# File with just '\n': 1 line.
# Unicode: combining characters? Probably too deep. But mention that len(str) counts code points (字符，Unicode 码点), not grapheme clusters. Maybe brief note.
# Performance: for one-time stats on small/medium files, len(f.read()) is fine. For huge files, chunked.

# Also can do both at once:''')
    file_a.read_art()
    file_a.sum_art()
    print(f"{'-'*10}")
    file_a.write_art_lines(['这是一行','并不会换行','\n换行得加换行符'])
    file_a.read_art()
    file_a.sum_art()