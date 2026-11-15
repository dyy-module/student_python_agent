# ===== day31 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:multi_turn_chat.py | 位置:学习产物\第05周\day31\ | ≤120 行 | 禁:明文 key;上下文窗口裁剪/摘要压缩(第06周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】多轮上下文命令行对话(≤120行)
#   从环境变量读 key(零硬编码,缺失优雅退出),创建指向国产端点的客户端;定义一条 system prompt 设定助手角色/语气/输出约束,作为 messages 首条
#   用 while 循环 + input() 读取用户输入,把 user 消息 append 进 messages,发起调用,再把 assistant 回复 append 回 messages(体现多轮上下文累积)
#   设置 temperature 与 max_tokens 参数,并用注释/print 分别说明其作用(temperature 管随机度,max_tokens 管长度上限;可故意把 max_tokens 设小观察截断);支持输入退出词(如 q/退出)时 break 结束循环;每轮打印回复与"当前 messages 条数"
#   try/except 兜底调用异常,单轮失败不导致整个程序崩溃;python 可交互跑通、每步有 print
#   知识点清单/讲解示例见周教程 Day31「学习内容」「讲解」「所用知识点清单」段(指针,本壳不复述)
# 【越界→隔离目录】多轮记忆高级管理(上下文窗口裁剪/摘要压缩/长期 Memory,第06/09周);Function Calling(第06周)→欲试放 day31/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day31「教材与章节」段(DeepSeek Chat 参数/messages;百炼/GLM 文档)
# 【交检】跑通无报错、每步 print;index.md 记 system prompt 示例与 temperature/max_tokens 取值观察+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】给"当前 messages 条数"加一行解释:为什么条数会越来越多(上下文累积的意义)(文字进 index.md)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
