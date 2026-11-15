# ===== day29 跟练 extra v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_model_card.py | 位置:学习产物\第05周\day29\extra\ | ≤120 行 | 禁:第三方库、联网、调 API(仅标准库)
#
# 【题目·逐字抄自教程「跟练清单」】复用第03周 OOP,定义 ModelCard 类(模型名/端点/是否有免费档),实现 __str__;
# 为三家国产大模型各建一张卡,遍历打印。仅用标准库,不联网。
#   知识点/讲解指针见周教程 Day29 段(本壳不复述)
# 【越界→隔离目录】__repr__/__eq__ 等其他魔术方法如需试用(day17 已学可直用);访问限制 __xxx 属【超前】→放 day29/beyond/
# 【教材·只读】OOP 复习见周教程 Day29「教材与章节」指向的廖雪峰面向对象页(勿顺翻访问限制节)
# 【交检】python 跑通、每步 print;_extra 命名并置于 extra\ 目录
# 【复验待修】2026-11-15 第三轮:通过——__str__ 已实现且 print(r) 直接触发,实测闭环 ✓
#   P2 缓账: "有免费挡"应为"档";desc_price 收了从未输出(__str__ 里可补一行)
# ================= 以下开始盲写(壳不得改动下方实现行) =================

class ModelCard:
    def __init__(self, name, url, has_free, desc_price=''):
        self.model_name = name
        self.url = url
        self.has_free = has_free
        self.desc_price = desc_price

    def __str__(self):
        '''输出模型信息'''
        return f"""
{self.model_name}
{self.url}
{'有免费挡' if self.has_free else '没有免费档'}"""


deepseek = ModelCard('DeepSeek-V4.1-Flash-1017',
                     has_free=False,
                     url='https://api-docs.deepseek.com/zh-cn/quick_start/pricing',
                     desc_price='1M输入 缓存命中 0.04元，缓存未命中：2元。1M输出：8元'
                     )
glm = ModelCard('GLM-5.3-Flash',
                has_free=True,
                url='https://docs.bigmodel.cn/cn/coding-plan/overview',
                desc_price='1M输入 缓存命中 0.23元，缓存未命中：0.8元。1M输出：2.8元'
                )
qwen = ModelCard('Qwen3.8-Flash',
                 has_free=True,
                 url='https://help.aliyun.com/zh/model-studio/token-plan-personal-overview?spm=a2c4g.11186623.0.i3',
                 desc_price='1M输入 缓存命中 0.1元,缓存未命中：0.8元。1M输出：2.7元'
                 )

if __name__ == '__main__':
    model_list = [deepseek, glm, qwen]
    for r in model_list:
        print(r)