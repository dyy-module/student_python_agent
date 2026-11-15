# ===== day21 闸门后加练壳 v3.1(可选,非检测项;30 分钟盲写,实现由你本人写) =====
# 文件:extra_task_list.py | ≤120 行(工作日预算,不沿用检测日 180 放宽) | 禁:第三方库(Day22 前)、未学知识点
#
# 【题目·对齐教程】(逐字抄自周教程 Day21「闸门后加练」v2.0 原文,就地可读免翻页;30 分钟内不看教材、不看本日 library_book.py 与本周任何产物独立盲写)
#   1. 定义TaskList类:__init__(name)建空任务清单;__str__返回可读信息;__len__返回任务数;__lt__(other)按任务数比较;add_task(task)添加任务(若task已在清单中则raise自定义异常DuplicateTaskError);__add__(other)合并两个清单返回新TaskList(任务并集,去重)。
#   2. 定义自定义异常DuplicateTaskError(Exception)。
#   3. 函数save_list(task_list, path)/load_list(path, name):文本文件持久化,存盘用模式'w'整表快照(注意与Day20追加账本区分场景);load用try/except处理FileNotFoundError(返回空TaskList并提示)与坏行(跳过并警告)。
#   4. 主流程:建两个清单并添加任务→演示重复添加被DuplicateTaskError拦截打印→print(len())与两清单 < 比较→合并为一个新清单→存盘→读回→验证读回清单任务数与合并结果一致。
# 【越界→隔离目录】@staticmethod/@property/set 及其并集语法(未首教),json——想试放 day21/beyond/,放对即留痕
# 【教材·只读】见周教程 Day17(魔术方法)与 Day20/Day21 段(不重列),勿顺翻第04周
# 【交检】python 一次跑通、每步 print;open 显式 encoding=utf-8;到点未跑通也停手交检;index.md 末两行自检照常(可并给本 extra)
# ================= 以下开始盲写(计时 30 分钟;壳不得改动下方实现行) =================
