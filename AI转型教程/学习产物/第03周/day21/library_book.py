# ===== day21 产物任务说明 v3.1(周检测日,45 分钟限时盲写) =====
# 文件:library_book.py | ≤180 行(周末检测放宽) | 禁:第三方库(Day22 前)、未学知识点
#
# 【题目·对齐教程】45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第03周/day21/library_book.py(题面逐字抄自周教程 Day21「周检测」原文,就地可读免翻页;知识点见教程「周尾附录」累计清单,不重列):
#   1. 定义Book类:__init__(title, copies);__str__返回可读信息;__eq__按书名比较;borrow()借出一本(copies减1,为0时raise自定义异常NoCopyError)。
#   2. 定义自定义异常NoCopyError(Exception)。
#   3. 函数save_books(books, path)/load_books(path):文本文件持久化,load时用try/except处理FileNotFoundError(返回空表)与格式错误(跳过并警告)。
#   4. 主流程:创建3本书→存盘→读回→演示正常借书与借到0本时触发NoCopyError并被捕获打印,程序不崩溃。
# 【越界→隔离目录】@staticmethod/@property(讲解段属【超前】识别项、非本产物必用,勿照搬),json(未首教)——想试放 day21/beyond/,放对即留痕
# 【教材·只读】见周教程 Day21 及「周尾附录:完整知识点累计清单(截至第03周day21)」(不重列),勿顺翻第04周
# 【交检·通过标准】教程原文照抄:45min 内 python library_book.py 一次跑通无未捕获异常;class+至少 3 个 dunder(__init__/__str__/__eq__);自定义异常被 raise 且被 except 捕获;文件存/读闭环可用+格式错误容错;仅用截至 day21 闭包知识点、无第三方库、≤180 行;所有 open 显式 encoding=utf-8;index.md 末两行自检(①说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【未通过补救】见周教程 Day21「未通过补救方案」段(三档:个别 dunder/异常错→1h 缓冲订正重盲写;文件持久化不通→重做 day18+day20 的 save/load;>90min 或结构混乱→第04周前 2 天补欠账)
# ================= 以下开始盲写(计时 45 分钟,到点即使未跑通也停手交检;壳不得改动下方实现行) =================

class NoCopyError(Exception):
    '''书被借完了'''

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f'{self.name} 没有库存了'


class Book:
    '''书 模型'''

    def __init__(self, title, copies):
        if not isinstance(copies,int):
            raise ValueError('参数错误')
        self.title, self.copies = title, copies

    def __eq__(self, other):
        '''判断是不是一本书'''
        if isinstance(other, Book):
            return self.title == other.title
        else:
            return NotImplemented

    def __str__(self):
        '''展示书信息'''
        return f"书名：{self.title},剩余{self.copies}本"
    __repr__ = __str__

    def to_line(self):
        '''转换为存储格式， 既字符传记录title copies'''
        return f"{self.title},{self.copies}"

    @staticmethod
    def form_line(book_str):
        '''将存储的书字符信息转换为书'''
        title, copies = book_str.strip().split(',')
        return Book(title, int(copies))

    def borrow(self):
        '''借书程序, 默认一本'''
        if int(self.copies) <= 0:
            raise NoCopyError(self.title)
        else:
            self.copies = self.copies - 1


def save_books(books, path):
    '''将书存入文件'''
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines([f"{book.to_line()}\n" for book in books])
    except OSError:
        print('写入失败，请重试')
    else:
        print('写入成功')


def load_books(path):
    '''加载书信息'''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = []
            for book_line in enumerate(f):
                try:
                    book = Book.form_line(book_line[1])
                except ValueError:
                    print(f"{book_line[0]} 行 书解析失败")
                else:
                    result.append(book)
            return result
    except FileNotFoundError:
        return []
    except OSError as err:
        print(err)
        return []


if __name__ == '__main__':
    book_file = 'book_file_01.txt'
    book_1 = Book('西游记', 1)
    book_2 = Book('水浒传', 2)
    book_3 = Book('羊脂球', 5)
    save_books([book_1, book_2, book_3], book_file)
    read_books = load_books(book_file)
    print(read_books)

    try:
        read_books[0].borrow()
        read_books[0].borrow()
    except NoCopyError as err:
        print(err)
