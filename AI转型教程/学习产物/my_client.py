from openai import OpenAI
from config import config


def creat_client()-> OpenAI:
    '''创建返回client'''
    if not config.DASHSCOPE_API_KEY:
        raise SystemExit("错误：未配置DASHSCOPE_API_KEY,请在.env 文件补充")
    return OpenAI(
        base_url=config.BASE_URL,
        api_key=config.DASHSCOPE_API_KEY,
    )
