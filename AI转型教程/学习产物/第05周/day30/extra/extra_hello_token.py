# ===== day30 跟练 extra v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_hello_token.py | 位置:学习产物\第05周\day30\extra\ | ≤120 行 | 禁:明文 key;计费优化(第17周【超前】)
#
# 【题目·逐字抄自教程「跟练清单」】
# 对同一问题分别用"短 prompt"和"长 prompt"各调一次,打印两次的 total_tokens,直观感受 prompt 长度对 token/成本的影响(认知,不做计费优化)。
# key 同样从环境变量读。
#   知识点/讲解指针见周教程 Day30 段(本壳不复述)
# 【越界→隔离目录】token 计费/缓存/小模型路由(第17周)→放 day30/beyond/
# 【教材·只读】见周教程 Day30「教材与章节」段(DeepSeek usage 说明)
# 【交检】python 跑通、每步 print;extra 命名并置于 extra\ 目录
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from openai import (
    OpenAI,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    BadRequestError,
    RateLimitError,
    APITimeoutError,
    APIConnectionError,
    InternalServerError,
    APIError,
)
from config import load_config
from dotenv import load_dotenv

load_dotenv()
config = load_config()


def get_client():
    if not config.DASHSCOPE_API_KEY:
        raise SystemExit("错误：未配置DASHSCOPE_API_KEY,请在.env 文件补充")
    client = OpenAI(
        api_key=config.DASHSCOPE_API_KEY,
        base_url=config.BASE_URL,
    )
    return client


def ask_q(q: str):
    '''输入问题，打印回复，统计token'''
    try:
        client = get_client()
        messages = [{"role": "user", "content": q}]
        completion = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=messages
        )
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
    except RateLimitError:
        print("触发限流：请求太频繁或额度不足")
    except APITimeoutError:
        print("请求超时：网络慢或模型响应太久")
    except APIConnectionError:
        print("连接失败：网络、代理或 base_url 有问题")
    except InternalServerError:
        print("服务端错误：平台暂时异常，稍后重试")
    except APIError as e:
        print("其他 API 错误：", e)
    except Exception as e:
        print("未预期错误：", e)
    else:
        print('内容', completion.choices[0].message.content)
        print('总token', completion.usage.total_tokens, '输入',
              completion.usage.prompt_tokens, '输出', completion.usage.completion_tokens)


if __name__ == '__main__':
    ask_q('token是什么')  #总token 812 输入 63 输出 749
    long_txt = '''
    ## 引用
结果由"tool_1"返回。其每条消息称为“来源”，引用ID为首次出现的【turn\d+\w+\d+】，如【turn2file1】，其中turn2file1就是来源引用ID。
引用指向tool_1来源，可引用一个或多个。
单来源必须写为{CITATION_START}cite{CITATION_DELIMITER}turn\d+\w+\d+{CITATION_STOP}，如{CITATION_START}cite{CITATION_DELIMITER}turn2file5{CITATION_STOP}。
多来源必须写为{CITATION_START}cite{CITATION_DELIMITER}turn\d+\w+\d+{CITATION_DELIMITER}turn\d+\w+\d+{CITATION_DELIMITER}...{CITATION_STOP}，如{CITATION_START}cite{CITATION_DELIMITER}turn2file5{CITATION_DELIMITER}turn2file1{CITATION_DELIMITER}...{CITATION_STOP}。
不要把引用放进Markdown加粗、斜体或代码围栏内，否则无法正确展示；放在这些格式外。围栏外的引用也不得与结束围栏处于同一行。
绝不直接在正文写turn\d+\w+\d+，必须包在{CITATION_START}...{CITATION_STOP}中。
- 默认段末引用，段落长时可行内引用，用户指定位置时按其要求。
- 引用放标点之后。
- 不把全部引用集中在回复末尾。
- 不让某行或某段只有引用。
一句话总结一下，不要超过20字
    '''
    ask_q(long_txt)#总token 967 输入 415 输出 552
