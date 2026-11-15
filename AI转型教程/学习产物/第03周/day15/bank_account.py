# ===== Day15 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:bank_account.py | ≤120 行 | 禁:第三方库(Day22前)、try/except(本周未学)
#
# 【需求】BankAccount 类:姓名与余额为实例属性(余额默认 0),银行名为类属性(全体共享)
#   1 存款:amt>0 才生效并显示新余额;非正数不得改动余额
#   2 取款:余额充足则扣减并显示新余额;不足时不得扣成负数、给出可读提示,并让调用方拿到成败结论(返回值+print)
#   3 展示:可独立调用,一行打印"谁的 / 多少钱"
#   自证:python bank_account.py 建 2 个账户 → 每步 print → 含一次余额不足被拒 → 再用 isinstance() 判定对象类型并打印
# 【可用知识点】class/__init__/self/实例属性/类属性/实例方法/if/print/isinstance()/type()/f-string
# 【越界需留痕(用了不删,标一行)】私有属性 __xxx(10.2,归 day17) | datetime.now/timezone/strftime(只学过 datetime.date) | 三目表达式(归属待确认)
#   留痕格式:【超前】知识点 | 出处 | 归 dayXX | 影响哪个行为
# 【教材·只读三节,读完即停】前缀 https://liaoxuefeng.com/books/python/
#   oop/class/index.html(10.1) | oop/props/index.html(10.5) | oop/attr/index.html(10.4,type/isinstance 出处)
#   ⚠ 10.1 下一页即 10.2 访问限制(day17 项),勿顺翻;其余归属查周文件「前置闭包 + 【超前】预警」
# 【交检】跑通无报错、每步 print;index.md 末做行为-知识点自证表(行=一个行为,3列)+表外一行差集
# 【加分可选】金额=0 与"取走全部余额"两个边界;改一次银行名后两账户同值(交易记录你已实现 ✅)
#
# 【⑥ 结清 2026-10-10】结论=通过;⑤ 的三个阻塞点你已自行修完(语法/作用域/KeyError 均消失,四件全 RUN=0)
#   选型已定✓且自洽：name 进返回包→展示跟着数据走。实测 `a.print_result(**b.deposit(3))` 输出"b存入成功...余额为8"——当年的串号 bug 类已消失,day18 遍历多账户展示不再有风险
#   唯一代价（不是 bug，是结构的必然后果）：同一个 dict 既 append 进 history 又当返回包,所以 name 又回到了每条历史（实测字段含 name;三条约重复三个同值）。你的判据本来选的是"name 跟着变→不存",现在它挡在 print_result 前又装回来——真正卡你的不是选型,是一个 dict 兼任两个角色（落盘账目 + 自描述消息）
#   到期 day18 前处理（今天不动）：要么接受冗余,要么把"落盘的"与"上报的"分成两个容器——分开后你昨天删字段那个动作就不会白删
# ================= 以下开始盲写(本次未改动你的实现) =================

from datetime import datetime


class BankAccount():
    '''银行用户信息,用于处理存取查询'''

    bank_name = '中国工商银行'
    operate_tip = {
        "deposit": "存入",
        "withdraw": "取出",
        "create": "初始账户"
    }

    def __init__(self, name, amt=0):
        self.__name = name
        self.__amount = amt
        self.__history = [
            {"time": datetime.now(), "name": name, "operate": 'create', "amt": amt, 'balance': amt}]

    def deposit(self, amt):
        '''钱款存入'''
        if (amt > 0):
            self.__amount += amt
            result = {"time": datetime.now(), "name": self.__name,
                      "operate": "deposit", "amt": amt, "balance": self.__amount}
            self.__history.append(result)
            return {"success": True, **result}
        else:
            return {"success": False, "message": "输入金额不正确"}

    def withdraw(self, amt):
        '''钱款取出'''
        if amt <= 0 or amt > self.__amount:
            return {"success": False, "message": f'金额不正确, 0< X <={self.__amount:.2f}'}
        else:
            self.__amount -= amt
            result = {"time": datetime.now(), "name": self.__name,
                      "operate": "withdraw", "amt": amt, 'balance': self.__amount}
            self.__history.append(result)
            return {"success": True, **result}

    def show_history(self):
        '''查看历史记录'''
        print('\n'.join(
            [f"时间：{r['time'].strftime('%Y-%m-%d %H:%M:%S')} ，操作：{BankAccount.operate_tip[r['operate'] ]} ，金额：{r['amt']} ，账户余额：{r['balance']}" for r in self.__history]))

    def print_result(self, success, **rest):
        if success:
            print(
                f"{BankAccount.bank_name} {rest['name']}{BankAccount.operate_tip[rest['operate'] ]}成功，{rest['amt']}元，余额为{rest['balance']}")
        else:
            print(rest['message'])

    def show_user_info(self):
        '''显示用户信息'''
        print(f'所属:{BankAccount.bank_name} 账户人：{self.__name} 账户余额：{self.__amount} ')


if __name__ == '__main__':
    user_a = BankAccount('a', 10)
    user_a.print_result(**user_a.deposit(12))
    user_a.print_result(**user_a.withdraw(8))
    user_a.show_history()
    user_a.show_user_info()
    print(type(user_a) is BankAccount)
    print(isinstance(user_a, BankAccount))

    user_b = BankAccount('b')
    user_b.print_result(**user_b.withdraw(8))
    user_b.print_result(**user_b.deposit(-2))
    user_b.print_result(**user_b.deposit(3))
    user_b.show_history()
    user_b.show_user_info()
    BankAccount.bank_name = '修改测试啊啊'
    print(f"{'-' * 5} 修改 {'-' * 5}")
    user_a.show_history()
    user_b.show_history()
