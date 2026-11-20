# ===== day30 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:first_chat.py | 位置:学习产物\第05周\day30\ | ≤120 行 | 禁:明文 key 写进代码;流式/工具调用(第06周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】环境变量读 key + 首次 Chat 调用(≤120行)
#   用 os.environ.get 读取所选国产大模型的 API key;
#   key 缺失时提示如何设置环境变量并优雅退出(raise SystemExit 或 try/except),零硬编码、不得把明文 key 写进代码
#   用大模型 SDK 创建客户端,base_url 指向国产端点;组织 messages(至少一条 role=user)完成一次 Chat API 调用,
#   提出一个简单问题 打印模型回复内容;
#   打印本次 token 消耗(usage),并记录消耗数值(产物注释或 index.md 均可,闸门要求)
#   用 try/except 捕获鉴权/网络异常,失败时打印友好提示、程序不崩溃;python 一次跑通(需先配好环境变量 key)、每步有 print
#   知识点清单/讲解示例见周教程 Day30「学习内容」「讲解」「所用知识点清单」段(指针,本壳不复述)
# 【越界→隔离目录】Streaming 流式返回(第06周);多轮记忆高级管理(第06周)→欲试放 day30/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day30「教材与章节」段(DeepSeek 首次调用/Chat 参考;官方 os 页按需检索勿通读;流式/FC 章属第06周勿顺翻)
# 【交检】跑通无报错、每步 print;确认无明文 key 泄漏;token 消耗数值留痕(产物注释或 index.md 均可,闸门要求)+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】把 base_url/model 名抽成变量并注明"换端点只改这两处",体会 OpenAI 兼容的意义(不展开多端点切换)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from openai import AuthenticationError, PermissionDeniedError, NotFoundError, BadRequestError
from my_client import creat_client


def ask_completion(question):
    """调用ai 回答问题"""

    if isinstance(question, str):
        client = creat_client()
        messages = [{"role": "user", "content": question}]
        completion = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=messages,
        )
        return completion
    else:
        raise ValueError("输入必须是字符串")


if __name__ == '__main__':
    try:
        completion = ask_completion('本周ai有什么最新动态')
        print(completion.choices[0].message.content)
        print(f'prompt_tokens:{completion.usage.prompt_tokens}\n',
              f'completion_tokens:{completion.usage.completion_tokens}\n',
              f'total_tokens:{completion.usage.total_tokens}\n'
              )
        #  prompt_tokens:65
        #  completion_tokens:413
        #  total_tokens:478
    except SystemExit as err:
        print(err)
    except AuthenticationError:
        print("鉴权失败：API Key 无效或过期")
    except PermissionDeniedError:
        print("权限不足：当前 Key 无权调用该模型")
    except NotFoundError:
        print("资源不存在：模型名或 base_url 可能写错了")
    except BadRequestError as e:
        print("请求参数错误：", e)
    except Exception as e:
        print("未预期错误：", e)
