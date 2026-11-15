# ===== day22 产物任务说明 v3(项目环境日;实现由你本人盲写于本注释下方) =====
# 文件:env_check.py | ≤120 行 | 第三方库已解禁(day22 起可用 requests);禁:未列进本日闭包的库/模块
#
# 【需求】虚拟环境自检脚本:证明"当前 Python 跑在 .venv 里且能拿到已锁依赖"
#   1 导入 requests:成功则 print 其 __version__ 与 __file__ 路径(肉眼确认 __file__ 含 .venv 即隔离生效)
#   2 读同目录 requirements.txt(用 with open),逐行 print 出已锁定的"包名==版本"清单
#   3 用 try/except 捕获 ImportError:若 requests 未装(未激活 .venv),print 友好提示"请先激活 .venv 再 pip install",程序不崩溃
#   自证:激活 .venv 后 python env_check.py 跑通、每步有 print;再在"未装 requests"的环境口径下确认走 except 分支不崩
#   (前置终端操作,非本文件代码:python -m venv .venv → .venv\Scripts\activate → pip install requests → pip freeze > requirements.txt;这些命令写进 index.md 备查,不要混进 .py)
# 【可用知识点】import、requests(day22 解禁)、__version__/__file__ 属性读取、try/except(ImportError)、with open、for line in f、strip、print、f-string
# 【越界→隔离目录】无高发项;若想用 subprocess 调 pip、读 sys.executable/sys.path 佐证隔离、或 pathlib 找文件,均属【超前】,想试请放 day22/beyond/(不写进交检产物)
# 【教材·只读N节,读完即停】
#   requirements.txt/pip freeze/install -r 权威出处:官方 https://docs.python.org/zh-cn/3/tutorial/venv.html —— 真讲到 freeze>requirements 与 install -r
#   创建/激活/deactivate:廖雪峰 https://liaoxuefeng.com/books/python/built-in-modules/venv/index.html (该页不讲 requirements)
# 【交检】跑通无报错、每步 print;读文件的所有 open 显式写 encoding="utf-8"(day19 教训,本周起硬性);index.md 末写两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点);终端命令归 index.md 不混入 .py
# 【加分可选】打印当前解释器路径以佐证在 .venv 内(若用到 sys 则放 beyond/,交检产物不强制)
# 【复验待修】已无——第4轮通过。P2缓账(周日对账):requirements.txt源头仍带BOM(239,187,191)未重建;extra读取口径统一为utf-8-sig;index订正utf-8档位拼写与ascii适用边界;.gitignore掉Include/Lib/Scripts/pyvenv.cfg后再首提
# ================= 以下开始盲写(壳不得改动下方实现行) =================
try:
    import requests
    print("requests 版本:", requests.__version__)
    print("来自路径:", requests.__file__) 
except ImportError:
    print('请先激活 .venv 再 pip install')


try:
    with open('requirements.txt', 'r', encoding='utf-8-sig') as f:
        for l in f:
            print(l.strip())
except FileNotFoundError as err:
    print(err)