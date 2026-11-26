# ===== day32 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:prompt_basic.py | 位置:学习产物\第05周\day32\ | ≤120 行 | 禁:明文 key;自洽性/ReAct 等 CoT 高级变体(第09周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】Prompt 工程技巧对比(≤120行)
#   从环境变量读 key(零硬编码,缺失优雅退出),创建国产端点客户端
#   用 def 封装一个"发一次请求并返回内容"的函数,供多次复用
#   至少演示 3 种 Prompt 技巧:角色设定(system)、清晰指令(明确格式/长度/语言)、少样本(messages 里塞示例对)
#   对同一个任务,分别用"裸 prompt(无技巧)"与"角色+指令+少样本"两版各调一次,并排打印两次输出,直观对比质量差异
#   用注释或 print 说明"思维链(让模型一步步想)"这一认知级技巧(不要求实现复杂变体)
#   每次调用 try/except 兜底;python prompt_basic.py 一次跑通,每步有 print(知识点清单/讲解示例见周教程 Day32 各段,指针不重列)
# 【越界→隔离目录】思维链高级变体(自洽性/ReAct,第09周 Agent);Prompt Chain(第07周)→欲试放 day32/beyond/,放对目录即留痕
# 【教材·只读】精读四章见周教程 Day32「教材与章节」段(提示原则/迭代优化/推断/聊天机器人,含在线章节级路径)
# 【交检】跑通无报错、每步 print;index.md 沉淀个人 Prompt 模板(角色+指令+示例结构)+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】把个人 Prompt 模板抽成 f-string 变量复用,展示"填空式模板"的工程价值
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from my_client import creat_client
from openai import AuthenticationError,RateLimitError,BadRequestError,InternalServerError,APIConnectionError,OpenAIError
from typing import Tuple,Optional
import time
from pathlib import Path

def ask_ai(msgs):
    '''调用ai,整理容错，返回结果文案'''
    try:
        client = creat_client()
        res = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=msgs
        )
        return res.choices[0].message.content , None
    except AuthenticationError:
        return None,'身份信息校验失败'
    except RateLimitError as err:
        return None,err.message
    except BadRequestError as err:
        err_msg = str(err.message).lower()
        if 'blance' in err_msg or 'quota' in err_msg or 'insufficient' in err_msg:
            return None,'账户余额不足，请充值。'
        elif  "context" in err_msg or "length" in err_msg or "maximum" in err_msg:
            return None,"输入内容太长，超出了模型的最大上下文限制。"
        else:
            return None,f'请求参数有误：{err.message}'
    except InternalServerError:
        return None, '模型服务商当前繁忙或正在维护，请稍后再试'
    except APIConnectionError:
        return None,'无法连接至服务器，请检查网络或代理设置'
    except OpenAIError as err:
        return None,f"未知模型错误：{str(err)}"
    except Exception as err:
        return None,f"【系统提示】系统内部错误：{str(err)}"
 
def write_md(str,file_name):
    '''将结论写入文档，方便对比'''
    try:
        base_pase = Path(__file__).resolve().parent
        output= base_pase.joinpath('output')
        output.mkdir(parents=True,exist_ok=True)
        file_path = output.joinpath(f'{file_name}.md')
        file_path.write_text(str,encoding='utf-8')
        print(file_path)
    except ImportError:
        print('无权限创建文件')
    except IOError as err:
        print(err)

def main(msgs,file_name):
    '''调度ai,写入结果，或打印错误'''
    res,err = ask_ai(msgs)
    if err:
            print(err)
    else:
        write_md(res,file_name)    
    
if __name__=='__main__':
    req='如何待本月比亚迪股票'
    print('-'*5,'直接问','-'*5)
    demo_msg_1 =[{'role':'user','content':req}]
    main(demo_msg_1,'直接问')
    
    time.sleep(5)
    print('-'*5,'设置角色','-'*5)
    demo_msg_2=[
        {'role':'system','content':'你是以为股票投资专家,请专业的回答问题'},
        {'role':'user','content':req}
    ]
    main(demo_msg_2,'设置角色')
    
    time.sleep(5)
    print('-'*5,'设置指令','-'*5)
    req_f=f'''
    请以专业的角度回答下放```包括的内容
    格式如下：
    走势原因：xxx
    投资建议: xxx
    简明扼要，每项不超过100个字
    问题：```{req}```
    '''
    
    demo_msg_3=[
        {'role':'system','content':'你是以为股票投资专家,请专业的回答问题'},
        {'role':'user','content':req_f}
    ]
    main(demo_msg_3,'设置指令')
    
    time.sleep(5)
    print('-'*5,'设置少量样本','-'*5)
    req_f_2=f'''
    请以专业的角度回答下放```包括的内容
    用户：如何待本月宁德时代股票
    回答：
        数据：A股收盘价 208.42元，5月7日高点467.06元，回撤约55%。A股单日跌幅-8.33%，总市值跌破1万亿元关口。
        总结：市场正经历一次显著的定价逻辑重估。股价持续承压，核心在于其盈利能力遭遇了来自政策、行业竞争和上游原材料的多重挤压，尽管其全球龙头地位和长期增长逻辑依然稳固
        原因：1.政策税负直接冲击利润。2.行业竞争加剧，客户“去宁化”。3.上游原料价格暴跌与定价逻辑切换。
    用户：{req}
    '''
    
    demo_msg_4=[
        {'role':'user','content':req_f_2}
    ]
    main(demo_msg_4,'少量样本')
    
    