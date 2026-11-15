# ===== day20 跟练 v3.1(extra/extra_todo.py,实现由你本人盲写) =====
# 文件:extra_todo.py | ≤60 行 | 禁:第三方库(Day22前)、未学知识点
#
# 【题目·对齐教程】把 student_manager 改造成待办清单(Todo),支持增/列/标记完成/存盘读盘,练习举一反三。(题面逐字抄自周教程 Day20「跟练清单」,就地可读免翻页)
#   Todo 规模本是主产物的子集(少成绩校验那类),不另列、不扩写;知识点/教材见周教程 Day20 对应段
# 【越界→隔离目录】@staticmethod(主产物壳已列为识别项/非必用,勿照搬),json(未首教)——想试放 day20/beyond/,放对即留痕
# 【教材·只读】见周教程 Day20「教材与章节」段(不重列),勿顺翻后续日章节
# 【交检】python extra_todo.py 跑通闭环、每步 print;所有 open 显式 encoding=utf-8;坏行不崩;extra_ 命名分离在 extra/;index.md 末两行自检(①说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【加分可选】空清单执行"标记完成/存盘"时友好提示
# ================= 以下开始盲写(壳不得改动下方实现行) =================

class Todo:
    '''待办类'''

    def __init__(self, date_str, desc, isDone=False):
        self.date_str, self.desc, self.isDone = date_str, desc, isDone

    def to_line(self):
        '''转为文字'''
        return f"{self.date_str},{self.desc},{'是' if self.isDone else '否'}"

    @staticmethod
    def from_line(r):
        '''文字转类'''
        date_str, desc, isDone = r.strip().split(",")
        return Todo(date_str, desc, isDone == '是')


def add_todo():
    '''添加待办'''
    try:
        date_str = input('请输入待办时间：')
        desc = input('请输入待办内容：')
        if date_str.strip() == '' or desc.strip() == '':
            raise ValueError('内容不能为空')
    except ValueError as err:
        print(err if err else '请输入正确的内容')
        return False
    else:
        return Todo(date_str, desc, False)


def show_todo(todos):
    '''展示待办'''
    if len(todos):
        print(
            '\n'.join((f"{todo[0]+1}: {todo[1].to_line()}" for todo in enumerate(todos))))
    else:
        print('暂无数据')


def get_seq(min_seq=0, max_seq=999999):
    '''获取正确序号'''
    try:
        seq = int(input('请输入任务序号：'))
        if seq < min_seq or seq > max_seq:
            raise ValueError('请输入范围内的序号')
    except ValueError as err:
        print(err)
        return get_seq(min_seq, max_seq)
    else:
        return seq


def change_done(todos):
    '''修改完成任务状态'''
    __todos = todos[:]
    show_todo(__todos)
    seq = get_seq(1, len(__todos))
    __todos[seq-1].isDone = True
    return __todos


def save_todo(path, todos):
    '''存储todo'''
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines([f"{r.to_line()}\n" for r in todos])
    except IOError as err:
        print(err if err else '存储失败')
        return False
    else:
        return True


def load_todo(path):
    '''取出todo,文件不存在当空列表沉默处理'''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            result = []
            for l in enumerate(f):
                try:
                    todo = Todo.from_line(l[1])
                except ValueError:
                    if (l[0] == 0 and len(l[1])) or l[0] != 0:
                        print(f"{l[0]}行解析失败")
                else:
                    result.append(todo)
            return result
    except FileNotFoundError:
        return []


def menu(path):
    '''菜单和操作选择 1.初始化读取代码 2.退出自动保存待办'''
    todos = load_todo(path)
    while True:
        print('\n'.join(['1:添加待办', '2:查看待办', '3:完成待办', '0:退出']))
        seq = get_seq(0, 3)
        if seq == 0:
            if (len(todos)):
                isEnd = save_todo(path, todos)
                if isEnd:
                    break
            else:
                break
        elif seq == 1:
            new_todo = add_todo()
            if new_todo:
                todos.append(new_todo)
        elif seq == 2:
            show_todo(todos)
        elif seq == 3:
            if (len(todos)):
                todos = change_done(todos)
            else:
                print('暂无待办任务')


if __name__ == '__main__':
    menu('todo_01.txt')
