# ===== day19 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:safe_reader.py | ≤120 行 | 禁:第三方库(Day22前);logging 段本日不用(见越界提醒)
#
# 【需求】健壮文件读取器:把 day18"文件不存在就崩"的坑用异常正式兜住,程序在任何场景都不崩溃
#   1 定义两个自定义异常 EmptyFileError 与 NegativeAmountError(都继承同一个异常基类)
#   2 写一个安全读取函数:尝试打开并读文件;分别处理"文件不存在""无权限";读到空内容时抛出 EmptyFileError;成功时给提示;收尾统一打印
#   3 用 as e 取到异常对象并把它的信息打印出来
#   4 主流程演示三种场景各 print 结果:读存在的文件 / 读不存在的文件 / 读空文件——三次跑完后主程序都能继续往下走
#   自证:python safe_reader.py 一次跑通、不崩溃;三种场景各走到自己的分支;每种场景都有"流程结束"类收尾输出
# 【可用知识点】try/except/else/finally、按类型多分支捕获、except ... as e、raise、自定义异常类(继承 Exception,用到 day16 继承)、open、with、encoding、print、if、f-string
# 【越界→隔离目录】廖 12.1 同页会讲到 logging(记录错误)与不带类型的裸 except: ——本日产物不用,若想试放 day19/beyond/,别写进交检产物(放对目录即留痕,不填表)
# 【教材·只读,读完即停】liaoxuefeng.com/books/python/error-debug-test/error/index.html(12.1:try/except/finally/else/raise/自定义异常/继承层次 全讲到)
#   ⚠ 12.1 里的 logging 段与"错误传播"读到即停、本日不接;速查另参 官方 tutorial errors.html(8)、菜鸟 python3-errors-execptions.html
# 【交检】跑通无报错、三场景都有可见分支输出;index.md 末写两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点;2026-10-24 起不再誊写行为-知识点表,行为对账由助教读产物完成);不誊教材章节
# 【加分可选】给自定义异常写更友好的错误信息;并观察把 except 顺序写成"先宽后细"会怎样、记进 index.md
# ================= 以下开始盲写(壳不得改动下方实现行) =================


class EmptyFileError(Exception):
    '''文件为空时错误类型'''

    def __str__(self):
        return '文件不能为空'


class NegativeAmountError(ValueError):
    '''金额不能小于0'''

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f'金额不能小于0,输入金额为{self.value}'


def safe_read(file_name):
    '根据名称读取文件'
    try:
        with open(file_name, 'r', encoding="utf-8") as f:
            if f.read(1) == '':
                raise EmptyFileError
    except FileNotFoundError:
        print('文件不存在')
        return []
    except PermissionError:
        print('文件无访问权限')
        return []
    except (EmptyFileError, NegativeAmountError) as err:
        print(err)
        return []
    else:
        with open(file_name, 'r', encoding="utf-8") as f:
            return [l for l in f]
    finally:
        print('读取结束')


def input_amt():
    try:
        amt = float(input('请输入金额'))
        if amt < 0:
            raise NegativeAmountError(amt)
    except NegativeAmountError as err:
        print(err)
    except ValueError:
        print('请输入数字')
    except TypeError:
        print('类型错误')


if __name__ == '__main__':
    print(safe_read('none.txt'))
    with open('empty.txt', 'w', encoding='utf-8') as f:
        f.write('')
    print(safe_read('empty.txt'))
    with open('c.txt', 'w', encoding='utf-8') as f:
        f.write('122')
    print(safe_read('c.txt'))
    input_amt()
