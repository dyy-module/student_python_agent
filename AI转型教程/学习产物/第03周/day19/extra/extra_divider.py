# ===== day19 跟练任务说明 v3(extra/extra_divider.py,实现由你本人盲写) =====
# 文件:extra_divider.py | ≤60 行 | 禁:第三方库
#
# 【需求】安全除法:写一个函数做 a÷b,用异常兜住两类错误并保证调用后程序不崩
#   1 分别处理"除以零"与"传入的类型根本没法做除法"(如字符串)两类错误
#   2 没出错时拿到并打印结果;无论成败都在收尾打印一行日志
#   3 主流程用多组输入(正常 / 除零 / 类型错)验证函数每次都能返回、程序不中断
#   自证:python extra_divider.py 跑通;三组输入各走各的分支且都有可见输出;收尾日志每条都出现
# 【可用知识点】try/except(多分支)、except ... as e、else、finally、def、return、print、f-string
# 【越界→隔离目录】无高发项;想试 assert 或自定义异常放 day19/beyond/
# 【教材·只读】同 safe_reader 壳的 12.1 一节 + 官方 tutorial errors.html
# 【交检】跑通无报错、每步 print;extra_ 命名分离在 extra/;行为并入 index.md 自证表即可
# 【加分可选】把非法类型也拦成一句友好提示,而不是甩出 traceback
# ================= 以下开始盲写(壳不得改动下方实现行) =================

def a_div_b(a, b):
    'a / b'
    try:
        result = a/b
    except ZeroDivisionError:
        return {"status": False, "message": "b 不能为0"}
    except TypeError:
        return {"status": False, "message": 'a, b必须为数字'}
    else:
        return {"status": True, "message": None, "result":result}
    finally:
        print('流程结束')

def show_result(result):
    if result["status"]:
        print(f"结果为{result['result']}")
    else:
        print(result['message'])

if __name__ == '__main__':
   show_result(a_div_b(1, 2))
   show_result(a_div_b(1, 0))
   show_result(a_div_b('2', '1'))
   
# ：try 里 return 之后，同块后续代码还会不会执行、else/finally 还走不走
# try return 后，else 不再执行，finally 照常走