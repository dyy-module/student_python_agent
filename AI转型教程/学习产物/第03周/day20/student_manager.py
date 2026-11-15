# ===== day20 产物任务说明 v3.1(项目日;实现由你本人盲写) =====
# 文件:student_manager.py | ≤150 行 | 禁:第三方库(Day22前)、未学知识点
#
# 【题目·对齐教程】(逐字抄自周教程 Day20「当日产出」原文,就地可读免翻页;知识点/教材见教程对应段,不重列)
#   student_manager.py:学生成绩管理系统(项目日,≤150行)
#   Student类:__init__(name, score)、__str__、to_line()、from_line()(反序列化)
#   save(students, path):用with open("a")把本次新增学生逐行**追加**写入(账本式存盘,多轮次累加不丢历史);存盘成功后清空内存暂存,避免同一批被重复追加;try/except处理写盘异常
#   load(path):用with open("r")读回全量(含历史批次追加的所有行);FileNotFoundError时返回空列表并提示;单行格式错误时try/except ValueError跳过并print警告(不崩溃)
#   菜单while循环:1添加/2查看/3保存/4加载/0退出
#   python student_manager.py可交互跑通,演示完整增-存-退-载-查闭环
# 【越界→隔离目录】@staticmethod(讲解段自带【超前】,仅需识别、非本产物必用,勿照搬),json(未首教)——想试放 day20/beyond/,放对即留痕
# 【教材·只读】见周教程 Day20「教材与章节」段(不重列),勿顺翻后续日章节
# 【交检】python 跑通闭环、每步 print;所有 open 显式 encoding=utf-8(day19 教训,本日硬项);坏行不崩;index.md 末两行自检(①说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【加分可选】成绩范围校验(0-100);重名处理;数据文件塞一条坏行验证容错
# ================= 以下开始盲写(壳不得改动下方实现行) =================
class Student:
    '''学生信息类，用于添加 传递 统一数据'''

    def __init__(self, id, name, score):
        self.id, self.name, self.score = id, name, score

    def to_line(self):                    # 序列化:对象→文件行
        return f"{self.id},{self.name},{self.score}"

    @staticmethod                         # 【超前】最小片段,仅识别
    def from_line(line):
        id, name, score = line.strip().split(",")
        return Student(id, name, float(score))

def load_student(path):
    '''读表查询学生数据'''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = []
            for stu in enumerate(f):
                try:
                    stu = Student.from_line(stu[1])
                except (ValueError, AttributeError) as err:
                    print(err)
                else:
                    result.append(stu)
            return result
    except FileNotFoundError:
        print('数据文件不存在')
        return []

def save_student(path, students):
    '''将学生信息存起来'''
    try:
        with open(path, 'a', encoding='utf-8') as f:
            f.writelines([f"{s.to_line()}\n" for s in students])
        print('存储成功')
        return True
    except Exception as err:
        print(err if err else '存储过程出错', '请重试')
        return False

def in_name():
    '''获取学生名称，并验证'''
    name = input('请输入姓名')
    if name.strip() == '':
        raise ValueError('请输入正确的名称')
    else:
        return name

def in_score():
    '''输入学生成绩，并校验'''
    score = float(input('请输入成绩'))
    if score < 0 or score > 100:
        raise ValueError('无效成绩，成绩范围0<x<100')
    else:
        return score

def in_id():
    '''输入学生ID，并校验'''
    id = input('请输入ID:')
    if id.strip() == '':
        raise ValueError('ID不能为空')
    else:
        return id


def get_student_info():
    '''获取学生成绩信息'''
    try:
        id, name, score = in_id(), in_name(), in_score()
    except (TypeError, ValueError) as err:
        print(err if err else '请输入正确的数据')
        return None
    else:
        return Student(id, name, score)

def show_stu_info(students=[]):
    '''展示学生信息'''

    if len(students):
        print('\n'.join((stu.to_line() for stu in students)))
    else:
        print('暂无数据')

def get_seq():
    '''获取序号并校验'''
    try:
        seq = int(input('请输入序号：'))
        if seq < 0 or seq > 4:
            raise ValueError
    except ValueError:
        print('请输入正确的序号')
        return get_seq()
    else:
        return seq


def menu(path):
    '''菜单，循环展示，q退出'''
    stus = []
    while True:
        print('1: 添加', '\n2:查看缓存数据', '\n3:保存', '\n4:加载', '\n0: 退出')
        seq = get_seq()
        match seq:
            case 0:
                if len(stus) == 0:
                    break
                else:
                    confirm = input('有未保存信息，退出将丢失信息，确认输入 y:')
                    if confirm == 'y':
                        break
            case 1:
                stu = get_student_info()
                if stu:
                    stus.append(stu)
            case 2:
                show_stu_info(stus)
            case 3:
                if len(stus):
                    isSuccess = save_student(path, stus)
                    if (isSuccess):
                        stus = []
                else:
                    print('暂无数据需要保存')
            case 4:
                stus = load_student(path)
                print('加载成功')


if __name__ == '__main__':
    menu('students_01.txt')
