from openai import OpenAI
from config import config
from typing import Optional

def creat_client(base_url:Optional[str] = None)-> OpenAI:
    '''创建返回client'''
    if not config.DASHSCOPE_API_KEY:
        raise SystemExit("错误：未配置DASHSCOPE_API_KEY,请在.env 文件补充")
    return OpenAI(
        base_url = base_url or config.BASE_URL,
        api_key=config.DASHSCOPE_API_KEY,
    )
