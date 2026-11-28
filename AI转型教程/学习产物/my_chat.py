from my_client import creat_client
from openai import (
    AuthenticationError,
    RateLimitError,
    BadRequestError,
    InternalServerError,
    APIConnectionError,
    OpenAIError,
)
from typing import Tuple, Optional
from functools import wraps


def askai_cache(func):
    """ai调用兜底修饰符，减少冗余，统一收口错误信息"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res, None
        except SystemExit as err:
            return None, str(err)
        except AuthenticationError:
            return None, "身份校验失败, 请检查key是否失效"
        except RateLimitError as err:
            return None, f"请求过于频繁，请稍后重试（{err}）"
        except BadRequestError as err:
            return None, f"请求参数错误：{err}"
        except InternalServerError:
            return None, "模型服务歇菜了，请稍后重试"
        except APIConnectionError:
            return None, "网络连接失败，请检测网络"
        except Exception as err:
            return None, f"未知错误：{str(err)}"

    return wrapper


class MyChat:
    """
    ai 调用封装
    __init__:初始化 client, base_url
    ask_ai: 调用函数,封装错误信息，返回信息和报错，结构 res,err,没有就为None
    """

    def __init__(self, base_url=None) -> None:
        self.client = creat_client(base_url)
        pass

    @askai_cache
    def ask_create(self, msgs, model=None, response_type=None, temperature=None):
        """调度ai,处理报错，返回结果"""

        res = self.client.chat.completions.create(
            model=model or "qwen3.8-flash",
            messages=msgs,
            response_format={"type": response_type or "text"},
            temperature=temperature or 0.6,
        )
        return res

    @askai_cache
    def ask_parse(self, msgs, schema, model=None, temperature=None):
        """schema 方式调用 parase"""
        res = self.client.chat.completions.parse(
            model=model or "qwen3.8-flash",
            messages=msgs,
            response_format=schema,
            temperature=temperature or 0.6,
        )
        return res
