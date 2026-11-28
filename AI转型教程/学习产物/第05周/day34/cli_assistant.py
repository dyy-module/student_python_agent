# ===== day34 产物任务说明 v3.1(项目日;实现由你本人盲写于本注释下方) =====
# 文件:cli_assistant.py | 位置:学习产物\第05周\day34\ | ≤150 行(项目日,教程口径) | 禁:明文 key;流式/Function Calling(第06周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】命令行问答助手(项目日,≤150行)
#   配置层:从环境变量读 key(零硬编码,缺失优雅退出),创建国产端点客户端;
#   会话层:用 messages 列表维护多轮上下文,首条为 system prompt 设定助手人设,每轮把 user 输入与 assistant 回复 append 回列表
#   交互层:while + input 菜单驱动,支持"普通问答"与"结构化模式"两种输入;输入退出词(q/退出)break
#   结构化模式:让模型用 JSON Mode 把用户给的一段话总结为 {summary, keywords},用 json.loads 解析后打印摘要与关键词列表
#   会话存档:每轮问答结束后,把本轮 user 消息与 assistant 回复用 json.dumps(d, ensure_ascii=False) 转成一行 JSON,
#   以追加模式("a", encoding="utf-8")写入 output/chat_history.jsonl(文件不存在自动新建);
#   output/ 目录用 pathlib.mkdir(parents=True, exist_ok=True) 幂等创建(day29 已学),存档失败只打印提示不中断对话
#   设置 temperature 并注释其作用;全链路 try/except 兜底网络/鉴权/解析异常,单次失败不导致程序崩溃
#   python cli_assistant.py 可交互跑通,演示"多轮问答 + 一次结构化总结 + 会话落盘"完整闭环,每步有 print,跑完确认 output/chat_history.jsonl 逐轮追加(知识点/分层示意见周教程 Day34 各段,指针不重列;讲解段仅示意非产物答案)
# 【越界→隔离目录】流式逐字输出/Function Calling(第06周);异步并发调用(【超前】);Schema 严格校验(第13周)→欲试放 day34/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day34「教材与章节」段(综合复习,回查各页标注复习日,勿整章重读)
# 【交检】跑通无报错、每步 print;确认 output/chat_history.jsonl 已生成且逐轮追加;index.md 覆盖分层设计思路+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】把"结构化模式"抽成独立函数复用 day33 写法;或加一个"清空上下文重新开始"的菜单项
# ================= 以下开始盲写(壳不得改动下方实现行) =================
