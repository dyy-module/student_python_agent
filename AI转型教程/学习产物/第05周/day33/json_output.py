# ===== day33 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:json_output.py | 位置:学习产物\第05周\day33\ | ≤120 行 | 禁:明文 key;JSON Schema/Pydantic 严格校验(第13周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】JSON Mode 结构化输出与解析(≤120行)
#   从环境变量读 key(零硬编码,缺失优雅退出),创建国产端点客户端;在 Prompt 里明确要求模型返回指定字段的 JSON(如 label 与 score),并开启 JSON Mode(response_format=json_object)
#   用 json.loads 把返回字符串解析为 dict,按 key 取字段并打印
#   用 try/except(json.JSONDecodeError 或 Exception)兜住解析失败,打印原始返回便于排查,程序不崩溃;解析成功后校验返回是否含预期字段(如 label/score):缺失时打印友好提示,程序不崩(用 in 判断或 dict.get 取默认值)
#   做一次对比:同一问题"未开 JSON Mode"与"开 JSON Mode"各调一次,打印两者输出并说明可解析性差异
#   python 一次跑通、每步有 print(知识点清单/讲解示例见周教程 Day33 各段,指针不重列)
# 【越界→隔离目录】JSON Schema/Pydantic 严格校验(第13周 FastAPI);Function Calling 结构化取参(第06周)→欲试放 day33/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day33「教材与章节」段(DeepSeek JSON/结构化返回;官方 json 模块页按需检索)
# 【交检】跑通无报错、每步 print;index.md 记 JSON 字段约定写法与一次解析成功/失败对照+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】"未开/开启 JSON Mode"两次调用的 token 消耗一并打印,观察结构化输出的成本(文字进 index.md)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
