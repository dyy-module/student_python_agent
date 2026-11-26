# ===== day32 跟练 extra v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_fewshot.py | 位置:学习产物\第05周\day32\extra\ | ≤120 行 | 禁:明文 key
#
# 【题目·逐字抄自教程「跟练清单」】少样本情感分类——在 messages 里给 2-3 组"句子→情感标签"示例对,再让模型对一句新评论分类,打印结果。key 从环境变量读。
#   知识点/讲解指针见周教程 Day32 段(本壳不复述)
# 【越界→隔离目录】CoT 高级变体(自洽性/ReAct,第09周);fine-tuning(后续周)→放 day32/beyond/,放对目录即留痕
# 【教材·只读】见周教程 Day32「教材与章节」段(Datawhale C1/5 推断章:情感二分类+单标签约束)
# 【交检】python 跑通、每步 print;extra 命名并置于 extra\ 目录
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from my_client import creat_client
from typing import Optional,Tuple,List
from openai import AuthenticationError,RateLimitError,BadRequestError,InternalServerError,APIConnectionError,OpenAIError


def ask_ai(messages)->Tuple[Optional[str],Optional[str]]:
    """根据输入内容，调度ai回答问题，返回具体内容"""
    try:
        client = creat_client()
        completions = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=messages
        )
        return completions.choices[0].message.content,None
    except AuthenticationError:
        return None,'API Key 无效或未配置，请检查配置。'
    except RateLimitError:
        return None,'请求太频繁或额度已用尽，请稍后再试'
    except BadRequestError as err:
        err_msg = str(err.message).lower()
        if 'balance' in err_msg or 'quota' in err_msg or 'insufficient' in err_msg:
            return None,'账户余额不足，请充值。'
        elif  "context" in err_msg or "length" in err_msg or "maximum" in err_msg:
            return None,"输入内容太长，超出了模型的最大上下文限制。"
        else:
            return None,f'请求参数有误：{err.message}'
    except InternalServerError:
        return None, '模型服务商当前繁忙或正在维护，请稍后再试'
    except APIConnectionError:
        return None,'无法连接至服务器，请检查网络或代理设置。'
    except OpenAIError as err:
        return None,f'未知错误：{str(err)}'
    except Exception as err:
        return None,f"【系统提示】系统内部错误：{str(err)}"
    
    
def main(messages):
    '''调度ask,展示结果'''
    demo_prompt=f"""
    以下用```分隔的产品评论的情感是什么？
    ```{messages}```
    给出结论，格式如下：
    用户情感倾向：<结论>
    解决方案：<结论>
    """
    modal_msg=[
        {"role":"system","content":"你是一名专业的电商运营人员，善于分析用户评论情绪"},
        {"role":"user","content":"这个怎么掉漆了"},
        {"role":"assistant","content":"""
         用户情感倾向:不满
         解决方案：联系顾客，安抚客户情绪，换货或补差价。联系产品，查清原因，补救后续产品
         """},
        {"role":"user","content":"造型真可爱，我儿子超喜欢"},
        {"role":"assistant","content":"""
            用户情感倾向:正面
            解决方案：给客户发送谢谢等积极回复
            """},
        {"role":"user","content":demo_prompt}
    ]
    res,err = ask_ai(modal_msg)
    if err:
        print(err)
    else:
        print(res)
        
if __name__ =='__main__':
    main('你们家配送怎么这么慢，五天才到，箱子还扁了')
    main('这个造型我超喜欢的')