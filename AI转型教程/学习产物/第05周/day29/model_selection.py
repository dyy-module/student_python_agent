# ===== day29 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:model_selection.py | 位置:学习产物\第05周\day29\ | ≤120 行 | 禁:本日不调 API、不读 key(SDK 仅 import 自检)
#
# 【题目·逐字抄自教程「当日产出」】国产大模型选型对比 + SDK 自检 + 对比表落盘(≤120行)
#   用 dict 或 list[dict] 组织至少 3 个国产大模型(通义千问/DeepSeek/智谱GLM):名称、核心优势、文档入口、是否有免费档;
#   遍历打印可读对比表,并给出"学习期推荐端点"结论+一句话理由(用 if 或字典取值,不做真实评分算法)
#   用 try/except ImportError 检测大模型 SDK 是否已安装:已装则打印版本,未装则打印安装提示(写明"在 venv 内 pip install")
#   用 pathlib 把对比表落盘:Path.cwd() 定位脚本所在目录,创建 output/ 子目录(mkdir 加 parents=True, exist_ok=True,已存在不报错),
#   把对比表全文 write_text 写入 output/model_compare.txt(encoding="utf-8")
#   本文件不调用任何 API、不读取任何 key(留到 day30);文件顶部用注释写明"key 零硬编码"的本周规矩;python 一次跑通、每步有 print,跑完确认 day29/output/model_compare.txt 已生成
#   知识点清单/讲解示例见周教程 Day29「学习内容」「讲解」「所用知识点清单」段(指针,本壳不复述)
# 【越界→隔离目录】SDK 具体调用参数(day30 首教);流式 Streaming/Function Calling(第06周)→欲试放 day29/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day29「教材与章节」段(三家官方文档首页;官方 pathlib 页;廖雪峰模块/import 复习页勿顺翻后续未学章)
# 【交检】跑通无报错、每步 print;确认 output/model_compare.txt 已生成且含对比表;index.md 末两行自检(①我说不出出处的知识点,没有写"无";②学了但没落进任何行为的知识点)
# 【加分可选】给对比表加一列"是否 OpenAI 兼容",并在结论里说明"一套代码可切多家端点"的意义(文字进 index.md,不进产物)
# 【复验待修】2026-11-15 第三轮:通过(4/5/5/4)——SDK 3.51.0 已装走版本分支/顶部 key 注释/提示语/reason/改名均闭环,落盘正确 ✓
#   P1 缓账: requirements.txt 未建 → pip freeze > requirements.txt(day22 口径),day30 开工前补
#   P2 缓账: write_model_info 写入成功无 print("每步有 print")
# ================= 以下开始盲写(壳不得改动下方实现行) =================

#key 零硬编码
from pathlib import Path

models = {
    "deepseek": {
        "model_name": "DeepSeek-V4.1-Flash-1017",
        "price": "1M输入 缓存命中 0.04元，缓存未命中：2元。1M输出：8元",
        "free_time_price": "1M输入 缓存命中 0.02元。，缓存未命中：1元。1M输出：4元",
        "desc": "并发500。网页版免费,无套餐",
        "free_token": '无',
        "price_url": "https://api-docs.deepseek.com/zh-cn/quick_start/pricing",
        "reason": "推荐度3星，便宜，足够用了",
    },
    "GLM": {
        "model_name": "GLM-5.3-Flash",
        "price": "1M输入 缓存命中 0.23元，缓存未命中：0.8元。1M输出：2.8元",
        "free_time_price": "无",
        "desc": "lite套餐，94.4，月60M token",
        "free_token": "新人用户15,000,000token",
        "price_url": "https://docs.bigmodel.cn/cn/coding-plan/overview",
        "reason": "推荐度1星，套餐有点贵，但量大"
    },
    "qwen": {
        "model_name": "Qwen3.8-Flash",
        "price": "1M输入 缓存命中 0.1元,缓存未命中：0.8元。1M输出：2.7元",
        "free_time_price": "无",
        "desc": "lite套餐，19.5，20,000 Credits。Essential 39.5 45,000 Credits / 月",
        "free_token": "新人用户100,000token",
        "price_url": "https://help.aliyun.com/zh/model-studio/token-plan-personal-overview?spm=a2c4g.11186623.0.i3",
        "reason": "推荐度3星，lite便宜，足够用了"
    },
    "kimi": {
        "model_name": "kimi-k3",
        "price": "1M输入 缓存命中 2元,缓存未命中：20元。1M输出：40元",
        "free_time_price": "无",
        "desc": "无",
        "free_token": "无",
        "price_url": "https://platform.kimi.com/docs/pricing/chat",
        "reason": "不推荐，太贵"
    }
}


def check_openai():
    '''检测在 venv 内 pip install 包是否存在，打印版本'''
    try:
        import openai
        print('SDK 版本', openai.__version__)
        return True
    except ImportError:
        print('未检测到openai，请在 venv 内 pip install openai')
        return False


def get_models_dec():
    '''展示model 对比'''
    text = '\n\n'.join([f"""{r[0]} 模型{r[1]['model_name']}
价格：{r[1]['price']}
闲时价格：{r[1]['free_time_price']}
其他信息：{r[1]['desc']}
新人福利：{r[1]['free_token']}
学习期推荐：{r[1]['reason']}""" for r in models.items()])

    return text


def write_model_info(text):
    '''将模型价格信息写入文件'''
    try:
        p = Path(__file__).resolve().parent.joinpath('output')
        # p.is_dir() True 表示文件已存在,mkdir没有返回值，它是一个动作
        if not p.is_dir():
            p.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('没有权限建文件夹')
    except IOError as err:
        print(err)
    else:
        p.joinpath('model_compare.txt').write_text(text, encoding='utf-8')


if __name__ == '__main__':
    is_openai = check_openai()
    print('openai', is_openai)
    models_info = get_models_dec()
    print(models_info)
    write_model_info(models_info)
