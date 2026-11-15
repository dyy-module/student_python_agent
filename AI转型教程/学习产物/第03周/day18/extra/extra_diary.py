# ===== day18 跟练任务说明 v3(extra/extra_diary.py,实现由你本人盲写) =====
# 文件:extra_diary.py | ≤60 行 | 禁:第三方库、try/except(归day19)
#
# 【需求】日记追加器:让用户输入几行日记,按行带日期落盘,再读回全部打印
#   1 用 input() 收集若干行日记内容
#   2 用追加模式写入 diary.txt,每行前面自动带上当天日期(用已学的 date 取今日,别把日期写死)
#   3 写完再用读模式把 diary.txt 全部内容逐行读回并 print,验证与写入一致
#   自证:python extra_diary.py 跑通;输入几行后,落盘文件里每行都带日期,读回内容与写入对得上
# 【可用知识点】input、with、open 模式 a/r、encoding='utf-8'、write、for line in f、print、f-string、datetime.date(第01周已学)
# 【越界→隔离目录】无高发项;想试更高等级的文件/时间 API 放 day18/beyond/
# 【教材·只读】同 file_reader 壳的 13.1 一节 + 官方 tutorial 7.2;取今日日期查已核验的第01周 date 锚点
# 【交检】跑通无报错、每步 print;extra_ 命名分离在 extra/;行为并入 index.md 自证表即可,不必单列
# 【加分可选】给每条日记加序号;读回时只打印今天写的那几条
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from datetime import datetime

def user_log_in():
    ''' 收集用户日记，并写入 '''
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log= input(f'{now_time} 日记:')
    if log.strip() !='':
       with open('diary.txt','a+',encoding='utf-8') as f:
            log_len = len(f.readlines())
            f.write(f'({log_len+1}){now_time}: {log}\n')
    else:
        print('请输入正确的日志内容')

def user_log_show():
    '''展示用户日志'''
    with open('diary.txt','r',encoding='utf-8') as f:
        # line = f.readline()
        # while line:  # while 版本碰到空行，会意外退出
        #     print(line, end='')
        #     line = f.readline()
        for l in f:
            start = l.find(')') + 1
            log_time = datetime.strptime(l[start:start+19],'%Y-%m-%d %H:%M:%S')
            if log_time.date() == datetime.today().date():
                print(l,end='')


if __name__ =="__main__":
    user_log_in()
    user_log_show()
            
            