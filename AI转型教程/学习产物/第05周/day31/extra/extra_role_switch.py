# ===== day31 跟练 extra v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_role_switch.py | 位置:学习产物\第05周\day31\extra\ | ≤120 行 | 禁:明文 key;人设持久化/多轮 Memory(第06周【超前】)
#
# 【题目·逐字抄自教程「跟练清单」】用两个不同的 system prompt(如"严谨的技术文档"与"活泼的营销文案")对同一问题各调一次,并排打印两种风格回复,
#   体会 system 对人设的决定作用。key 从环境变量读。
#   知识点/讲解指针见周教程 Day31 段(本壳不复述)
# 【越界→隔离目录】system 动态注入/角色库(第09周 Agent Memory)→放 day31/beyond/
# 【教材·只读】见周教程 Day31「教材与章节」段(DeepSeek messages/role 说明)
# 【交检】python 跑通、每步 print;extra 命名并置于 extra\ 目录
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from my_client import creat_client
from message_history import MessageHistory
from openai import AuthenticationError,PermissionDeniedError,NotFoundError

message_history = MessageHistory()


def ask_question(message):
    '''输入ai问题，返回responese'''
    try:
        message_history.add_user(message)
        client = creat_client()
        messages = message_history.get()
        completion = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=messages,
        )
    except SystemExit as err:
        print(err)
    except AuthenticationError:
        print('鉴权失败：API Key 无效或过期')
    except PermissionDeniedError:
        print('权限不足：当前 Key 无权调用该模型')
    except NotFoundError:
        print('资源不存在：模型名或 base_url 可能写错了')
    except Exception as err:
        print("未预期错误：", err)
    else:
        content = completion.choices[0].message.content
        usage_dict = {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens,
        }
        message_history.add_assistant(content, usage_dict)
        return content
    return ''


if __name__ == "__main__":
    print('-'*5, '严谨的', '-'*5)
    message_history.add_system('严谨的技术文档')
    content = ask_question('讲讲python 装饰器 @property')
    print(content)
    print('使用了token', message_history.total_tokens)

    print('-'*5, '娱乐化', '-'*5)
    message_history.clear()
    message_history.add_system('活泼的营销文案')
    content = ask_question('讲讲python 装饰器 @property')
    print(content)
    print('娱乐化使用了token', message_history.total_tokens)
