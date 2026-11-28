# ===== day33 产物任务说明 v3.1(实现由你本人盲写于本注释下方) =====
# 文件:json_output.py | 位置:学习产物\第05周\day33\ | ≤120 行 | 禁:明文 key;JSON Schema/Pydantic 严格校验(第13周【超前】)
#
# 【题目·逐字抄自教程「当日产出」】JSON Mode 结构化输出与解析(≤120行)
#   从环境变量读 key(零硬编码,缺失优雅退出),创建国产端点客户端;
#   在 Prompt 里明确要求模型返回指定字段的 JSON(如 label 与 score),并开启 JSON Mode(response_format=json_object)
#   用 json.loads 把返回字符串解析为 dict,按 key 取字段并打印
#   用 try/except(json.JSONDecodeError 或 Exception)兜住解析失败,打印原始返回便于排查,程序不崩溃;
#   解析成功后校验返回是否含预期字段(如 label/score):缺失时打印友好提示,程序不崩(用 in 判断或 dict.get 取默认值)
#   做一次对比:同一问题"未开 JSON Mode"与"开 JSON Mode"各调一次,打印两者输出并说明可解析性差异
#   python 一次跑通、每步有 print(知识点清单/讲解示例见周教程 Day33 各段,指针不重列)
# 【越界→隔离目录】JSON Schema/Pydantic 严格校验(第13周 FastAPI);Function Calling 结构化取参(第06周)→欲试放 day33/beyond/,放对目录即留痕
# 【教材·只读】精读页见周教程 Day33「教材与章节」段(DeepSeek JSON Output 专页/百炼参数页/官方 json,含已核验锚点与勿顺翻提醒)
# 【交检】跑通无报错、每步 print;index.md 记 JSON 字段约定写法与一次解析成功/失败对照+末两行自检(①说不出出处的知识点写"无";②学了但没落进任何行为的知识点)
# 【加分可选】"未开/开启 JSON Mode"两次调用的 token 消耗一并打印,观察结构化输出的成本(文字进 index.md)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
from my_chat import MyChat
from message_history import MessageHistory
from pydantic import BaseModel, Field  # 超前
from typing import List
import json


class MyAgent:
    """
    初始化 chat history
    调度ai,更新history,记录token
    """

    def __init__(self, int_msgs=None) -> None:
        self.chat = MyChat()
        self.history = MessageHistory(int_msgs)

    def ask_ai(self, msg, response_type=None):
        """调度ai,更新历史记录"""
        self.history.add_user(msg)
        res, err = self.chat.ask_create(
            msgs=self.history.get(), response_type=response_type
        )

        if err:
            return None, err
        else:
            content = res.choices[0].message.content
            self.history.add_assistant(content, res.usage)
            return content, None

    def ask_parse(self, msg, schema):  # schema parse 超前
        """调度ai,更新历史记录"""
        self.history.add_user(msg)
        res, err = self.chat.ask_parse(msgs=self.history.get(), schema=schema)

        if err:
            return None, err
        else:
            self.history.add_assistant(res.choices[0].message.content, res.usage)
            return res.choices[0].message.parsed, None

    def show_tokens(self):
        """展示总token"""
        print("总token", self.history.total_tokens)
        print("输入token", self.history.total_prompt_tokens)
        print("输出token", self.history.total_completion_tokens)

    @staticmethod
    def parse_json(s):
        try:
            result = s
            if isinstance(s, str):
                result = json.loads(s)
            if hasattr(result, "model_dump"):
                result = result.model_dump()  # Pydantic   model_dump 超前
            for r in result.get("items", []):
                label = r.get("label", None)
                score = r.get("score", None)
                reason = r.get("reason", None)
                if label is not None and score is not None:
                    print(f"标签: {label}, 得分: {score}, 原因: {reason}")
                else:
                    print("标签或得分不存在")

            return result
        except Exception as err:
            print(f"解析失败: {str(err)}\n原始返回(raw): {repr(s)}")
            return {}


if __name__ == "__main__":
    demo_json = {
        "items": [
            {
                "label": "公司名称(代码)",
                "score": "评分0-100",
                "reason": "原因，不要超过100个字",
            }
        ]
    }
    err_ques = f"""
    在A股上市的汽车公司，根据最近三个月的表现，对其分析，评价是否可买入。
    结果：{json.dumps(demo_json)}
    """
    ques = err_ques+'返回使用json格式'
    base_msgs = [
        {
            "role": "system",
            "content": "你是一位资深A股市场投资专家，擅长给予股市专业的评价和预测",
        },
    ]
    # --------------------------
    print("-" * 5, "json版", "-" * 5)
    json_agent = MyAgent(base_msgs)
    # ---- 错误示例
    res, err = json_agent.ask_ai(err_ques, response_type="json_object")
    print(
        "错误示例:", err
    )  #  400 - 'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.
    # ---- 正确示例
    res, err = json_agent.ask_ai(ques, response_type="json_object")
    if err:
        print(err)
    else:
        json_agent.parse_json(res)
        json_agent.show_tokens()  # 总token 5903 输入token 205 输出token 5698
    # -------------------------------
    print("-" * 5, "text版", "-" * 5)
    text_agent = MyAgent(base_msgs)
    res, err = text_agent.ask_ai(ques)
    if err:
        print(err)
    else:
        print(res)
        text_agent.show_tokens()  # 总token 9432 输入token 1054 输出token 8378

    # --------------schema 版本----------------
    print("-" * 5, "schema", "-" * 5)

    class Result(BaseModel):
        label: str = Field(description="公司名称(代码)")
        score: int = Field(description="评分0-100", ge=0, le=100)
        reason: str = Field(description="原因，不要超过100个字", max_length=100)

    class ListResult(BaseModel):
        items: List[Result]

    ques_schema = f"""
    在A股上市的汽车公司，根据最近三个月的表现，对其分析，评价是否可买入。
    返回json结果：{ListResult.model_json_schema()}
    """
    schema_agent = MyAgent(base_msgs)
    res, err = schema_agent.ask_parse(msg=ques_schema, schema=ListResult)
    if err:
        print(err)
    else:
        schema_agent.parse_json(res)
        schema_agent.show_tokens()  # 总token 3959 输入token 2559 输出token 1410
