# ===== day35 周检测任务说明 v3.1(闸门:45 分钟内盲写,不看教材/不看本周产物) =====
# 文件:json_task_bot.py | 位置:学习产物\第05周\day35\ | ≤180 行(周末检测放宽) | 禁:明文 key;流式/Function Calling/Schema 校验(【超前】)
#
# 【题目·逐字抄自教程「周检测」】45 分钟内独立盲写:读 key→调国产大模型→用 Prompt 完成任务→JSON Mode 输出并解析打印
#   1. 从环境变量读取国产大模型 API key(缺失则打印设置提示并优雅退出),零硬编码、不得写明文 key
#   2. 用大模型 SDK 创建客户端,base_url 指向所选国产端点
#   3. 组织 messages:含一条 system(设定角色,如"信息提炼助手")+ 一条 user(给定一段用户评论文本,要求提炼要点)
#   4. 开启 JSON Mode(response_format=json_object),要求模型返回含指定字段的 JSON(如 points 列表 + sentiment 情感标签)
#   5. 用 json.loads 解析返回,try/except 兜住解析失败;遍历打印每个要点与情感标签
#   6. 打印本次调用的 token 消耗(usage)
# 【通过标准】一次跑通无未捕获异常;key 从环境变量;messages 含 system+user;JSON Mode 可被 loads 成功解析;遍历打印要点+情感+token;每步 print;仅用截至 day35 闭包、三方仅大模型 SDK、≤180 行
# 【未通过补救】个别字段/参数拼错→对照 Day30/Day33 讲解订正+次日重盲写(≤45min);messages 组织或 JSON 解析不通→重做 Day31+Day33;严重超时(>90min)→第06周前 2 天补欠账,闸门顺延不取消
# 【越界→隔离目录】流式 Streaming/Function Calling(第06周);异步并发(【超前】);Schema/Pydantic(第13周)→如想试放 day35/beyond/,放对目录即留痕(检测不计分)
# 【交检】python 跑通无报错、每步 print;确认无明文 key;index.md 末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# ================= 以下开始限时盲写(壳不得改动下方实现行) =================
