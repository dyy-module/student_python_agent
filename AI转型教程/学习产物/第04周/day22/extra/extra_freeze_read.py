# ===== day22 跟练任务说明 v3(extra/extra_freeze_read.py,实现由你本人盲写) =====
# 文件:extra_freeze_read.py | ≤60 行 | 禁:第三方库(本跟练只用标准语法+文件读写)
#
# 【需求】把 requirements.txt 读成整齐清单(纯练 day22 的文件解析,不新增知识点)
#   1 打开 requirements.txt,对每行用字符串 split("==") 拆出包名与版本
#   2 print 成"包名 -> 版本"的对齐清单(逐行输出)
#   3 文件不存在时用 try/except 提示(题面见教程 Day22「跟练清单」原文,以教程为唯一出处)
#   自证:python extra_freeze_read.py 跑通;有该文件→打印清单,临时改名→走 except 提示不崩
# 【可用知识点】with open、encoding、for line in f、strip、split、try/except、print、f-string
# 【越界→隔离目录】无高发项;想用正则解析版本(如 "^包名==")属 day24 内容,今天先放 beyond/ 或直接 split
# 【教材·只读N节】复用 day22 主教材页;split/strip 忘了查菜鸟字符串方法页 https://www.runoob.com/python3/python3-string.html
# 【交检】跑通、每步 print;open 显式 encoding;extra 与固定产物分离在本 extra/ 目录内
# ================= 以下开始盲写(壳不得改动下方实现行) =================

def read_requirements():
    '''读取day22 requirements'''
    try:
        with open('requirements.txt','r',encoding='utf-8') as f1:
            print( f1.read(3) == b'\xef\xbb\xbf')
        with open('requirements.txt','r',encoding='utf-8') as f:
            for l in f:
                name,version = l.strip().split('==')
                print(f"{name} -> {version}")
    except (FileNotFoundError,ValueError) as err:
        print(err)

if __name__ =='__main__':
    read_requirements()