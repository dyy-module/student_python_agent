# ===== day33 跟练 extra v3.1(实现由你本人盲写于本注释下方) =====
# 文件:extra_json_parse.py | 位置:学习产物\第05周\day33\extra\ | ≤120 行 | 禁:明文 key;Schema 校验(第13周【超前】)
#
# 【题目·逐字抄自教程「跟练清单」】让模型用 JSON Mode 返回含列表的 JSON(如 {"tips":["...","...","..."]}),
# 用 json.loads 解析后 for 遍历打印每条,体会嵌套结构解析。key 从环境变量读。
#   知识点/讲解指针见周教程 Day33 段(本壳不复述)
# 【越界→隔离目录】嵌套多层 Schema 约束(第13周)→放 day33/beyond/
# 【教材·只读】见周教程 Day33「教材与章节」段(官方 json 模块页)
# 【交检】python 跑通、每步 print;extra 命名并置于 extra\ 目录
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from my_client import creat_client
from openai import AuthenticationError,RateLimitError,BadRequestError,InternalServerError,APIConnectionError,OpenAIError
import json

def ask_ai(msgs,response_type = "text"):
    '''调用ai,兜底错误，返回结果'''
    response_format={
        "type": response_type,
    }
    try:
        client = creat_client()
        res = client.chat.completions.create(
            model="qwen3.8-flash",
            messages=msgs,
            response_format={
                "type": response_type,
            }
        )
        return res.choices[0].message.content,None
    except AuthenticationError:
        return None,'身份校验失败'
    except RateLimitError:
        return None,'请求过于频繁，请稍后重试'
    except BadRequestError as err:
        return None,str(err.message).lower()
    except InternalServerError:
        return None,'模型服务商当前繁忙或正在维护，请稍后再试'
    except APIConnectionError:
        return None,'无法连接至服务器，请检查网络或代理设置'
    except OpenAIError as err:
        return None,f'模型未知错误，信息：{str(err)}'
    except Exception as err:
        return None,f'未知错误，信息：{str(err)}'

def parse_json(s, default={}):
    try:
        return json.loads(s)
    except (json.JSONDecodeError, TypeError):
        return default       

def ask_json(msg):
    '''出入参数结构化，调用ai'''
    
    dict_model={
        "title":"输出新闻标题",
        "summary":{
            "city":"提取国家信息",
            "main":"提取正文信息"
        },
    }
    sys_model=f'''
    你是一个严格的新闻总结工作人员，回答问题严格通过下方json格式返回
    {json.dumps(dict_model)}
    '''
    msgs=[
        {"role":"system","content":sys_model},
        {"role":"user","content":msg},
    ]
    res, err = ask_ai(msgs)
    if err:
        print(err)
        return {}
    else:
        return parse_json(res)


if __name__ =='__main__':
    res = ask_json('''美东时间周三，美联储公布全美经济形势调查报告，即“褐皮书”。褐皮书显示，今年11月全美物价压力范围进一步扩大，印证美联储官员对通胀粘性的担忧。

　　美联储官员将结合这份一线调研信息，在两周后的议息会议上做出利率决议。市场普遍预期美联储将加息25个基点，为年内第二次加息。

　　美国通胀压力持续升温

　　美联储褐皮书汇总全美企业与消费者一线调研信息，用以研判经济形势。报告显示，11月前两周，美国能源、运输、医疗、保险以及关税相关支出端“成本压力持续存在”；原材料、金属、货运以及专项进口品同样推高企业经营成本。

　　受市场竞争以及客户价格敏感度约束，美国企业难以把成本上涨完全转嫁给下游，生产耗材成本涨幅普遍高于产品售价涨幅。褐皮书还提到，企业预计未来数月开支与售价仍将继续上行。

　　在这份褐皮书公布之前，据报道，美国即将宣布对来自中国等十几个国家的商品加征关税。关税提升预计将进一步加大美国国内物价升温压力。

　　周三出炉的美联储偏好的通胀指标也再度升温：美国10月剔除波动较大食品和能源价格的核心个人消费支出（核心PCE）同比上涨3.3%，高于市场预期的3.2%，9月为3.1%；核心PCE环比持平于0.3%，符合预期。

　　美国就业市场整体平稳

　　与此同时，褐皮书反映出，美国就业市场边际企稳：多个行业企业用工需求持平或走高，但受不确定性、居民消费走弱拖累，企业招工意愿偏谨慎。

　　同时，美国劳动力供给整体保持平稳，普通岗位招人难度不大，但技术类、专业岗位招工难问题依旧。

　　整体而言，美国11月就业小幅增长，多数企业人员规模维持稳定，招聘以补流失岗位为主，仅少数企业大幅增聘。''')
for r in res.items():
    if r[0]=='summary':
        for r_summary in r[1].items():
            print(f'{r_summary[0]}:{r_summary[1]}')
    else:
        print(f'{r[0]}:{r[1]}')