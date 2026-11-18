from dataclasses import dataclass
import os


@dataclass
class Config:
    DASHSCOPE_API_KEY: str
    BASE_URL: str


def load_config() -> Config:
    return Config(
        DASHSCOPE_API_KEY=os.getenv('DASHSCOPE_API_KEY', '').strip(),
        BASE_URL="https://ws-l9ip5sskm8s5scpy.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    )
