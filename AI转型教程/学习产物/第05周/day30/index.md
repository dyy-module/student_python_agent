# day30 笔记(学习者本人填写)

## 今日主题

### os.environ 是什么

os.environ 是 python 一个类字典对象,表当前进程的环境变量，可读、可写、可遍历

```python
import os

# 读取（键不存在 → 抛 KeyError）
os.environ.setdefault('BASE_URL', 'https://api.example.com')  # 演示准备:保证键存在
base_url = os.environ['BASE_URL']

# 安全读取
port = os.environ.get('PORT')            # 不存在返回 None
port = os.environ.get('PORT', '8000')    # 不存在返回 '8000'
port = os.getenv('PORT', '8000')    # 完全等价 environ.get。语法糖

#遍历
for k, v in os.environ.items():
    print(k, '=', v)

# 判断
if 'DEBUG' in os.environ: ...

# 写入（仅影响当前进程及其子进程，不影响父进程/系统）
os.environ['MY_VAR'] = 'hello' # 只能设置字符串

os.putenv('FOO', 'bar')       # ❌ 不推荐！os.putenv 直接调 C 函数，不会更新 os.environ 的内部字典

# 删除
del os.environ['MY_VAR']
os.environ.pop('MY_VAR', None)

```

#### 一些不能放入项目的密钥怎么办，环境配置？

项目配置文件：.env ,格式： KEY=VALUE !!!不要上传仓库，因为是明文，容易泄露。.gitignore
项目配置文件示例： .env.example 用于告诉其他开发者都需要配置些什么环境变量

怎样加载环境变量

```python
from dotenv import load_dotenv
load_dotenv() # 加载环境变量，一般放在项目入口
# load_dotenv 干了什么
# 1.找到项目根目录（或指定路径）的 .env 文件
# 2.逐行解析 KEY=VALUE
# 3.对每个键值对调用 os.environ[key] = value
```

最佳实践

```python
# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    database_url: str
    debug: bool
    port: int

os.environ.setdefault("DATABASE_URL", "postgres://localhost/demo")  # 演示准备:保证键存在

def load_config() -> Config:
    return Config(
        database_url=os.environ["DATABASE_URL"],
        debug=os.getenv("DEBUG", "false").lower() == "true",
        port=int(os.getenv("PORT", "8000")),
    )

config = load_config()
```

```python
# app.py
from config import load_config
config = load_config()
print(config.BASE_URL)  # 业务代码不碰 os.environ
```

【配置从哪来】

```text
生产：Docker -e / K8s / 云平台面板 ──┐
                                  ├──► 操作系统进程环境表
本地：.env 文件 ──load_dotenv()──► ──┘
                                  │
                                  │ os.environ / os.getenv 读取
                                  ▼
                          config.py（集中管理）
                                  │
                                  ▼
                               业务代码
```

### openai sdk

是什么：是一个 REST API 的封装器，负责处理网络请求、认证、重试、流式解析等底层细节。
#### client.chat.completions.create

```python
import httpx
from openai import (
    OpenAI, AuthenticationError, PermissionDeniedError, NotFoundError,
    BadRequestError, RateLimitError, APITimeoutError, APIConnectionError,
    InternalServerError, APIError,
)
from config import load_config
from dotenv import load_dotenv

load_dotenv()
config = load_config()
http_client = httpx.Client(
    proxies={
        "http://": "http://127.0.0.1:7890",
        "https://": "http://127.0.0.1:7890",
    }
)

client = OpenAI(
    api_key=config.DASHSCOPE_API_KEY, # 身份验证 模型api_key
    base_url=config.BASE_URL,# 模型请求地址
    timeout=3,  # 单位为秒，控制请求最多等待多久。可全局设，也可在 create() 单次覆盖
    max_retries=2,  # 网络抖动、5xx 时自动重试，默认一般是 2 次
    default_headers={
        "X-Request-Id": "req-001",
        "X-Gateway-Protocol": "openai",
    }, # 请求头
    default_query={
        "requestId": "req-001",
        "version": "v2",
    }, # 查询参数
    http_client=http_client,  # 自定义 httpx 客户端
    # http_client=httpx.Client(verify=False) #跳过 SSL 验证
)
question = "用一句话介绍你自己"
messages = [{"role": "user", "content": question}]

try:
    response = client.chat.completions.create(
        model="qwen3.8-flash",
        messages=messages,
        # stream=True # 开启流式输出
    )
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
    content = response.choices[0].message.content
    print("内容：", content)
    print("总token：", response.usage.total_tokens)

```

| 异常 | 含义 |
|---|---|
| AuthenticationError | Key 错、过期、被撤销 |
| PermissionDeniedError | Key 有效，但没有权限 |
| NotFoundError | 模型名、路径、资源 ID 不对 |
| BadRequestError | 参数、格式、JSON 不对 |
| RateLimitError | 429 限流 |
| APITimeoutError | 超时 |
| APIConnectionError | 网络/代理/base_url 连不上 |
| InternalServerError | 服务端 5xx |
| APIError | 其他 API 错误兜底 |
| Exception | 真正的未知异常 |

#### 流式与非流式区别

| 维度 | 非流式 `stream=False` | 流式 `stream=True` |
|---|---|---|
| 返回对象 | `ChatCompletion` | 可迭代对象，每个元素是 `chunk` |
| 内容字段 | `response.choices[0].message.content` | `chunk.choices[0].delta.content` |
| Token 统计 | `response.usage.total_tokens` | OpenAI 官方需加 `stream_options={"include_usage": True}`；百炼兼容端点默认末 chunk 带 usage（day30 实测可不加） |
| 适用场景 | 批量处理、后台任务、需要完整结果再判断 | 聊天界面、命令行实时输出、长文本生成 |

非流式：
```python
from openai import OpenAI
from config import load_config
from dotenv import load_dotenv

load_dotenv()
config = load_config()
client = OpenAI(
    api_key=config.DASHSCOPE_API_KEY,
    base_url=config.BASE_URL,
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
)

print(response.choices[0].message.content)
print(response.usage.total_tokens)
```
流式：
```python
from openai import OpenAI
from config import load_config
from dotenv import load_dotenv

load_dotenv()
config = load_config()
client = OpenAI(
    api_key=config.DASHSCOPE_API_KEY,
    base_url=config.BASE_URL,
)

stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}],
    stream=True,
    stream_options={"include_usage": True},  # 想要 token 统计就加这个
)

for chunk in stream:
    if chunk.choices:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
    elif chunk.usage:
        print("\n总token:", chunk.usage.total_tokens)
```

#### client.responses.create()
2025 年起，openai@v3 推荐的新写法

| 维度 | Chat Completions | Responses API |
|---|---|---|
| 方法 | `client.chat.completions.create()` | `client.responses.create()` |
| 输入 | `messages=[{"role":"user","content":"..."}]` | `input="..."` 或 `input=[...]` |
| 系统指令 | `{"role":"system","content":"..."}` | `instructions="..."` |
| 返回值 | `ChatCompletion` | `Response` 对象 |
| 取文本 | `response.choices[0].message.content` | `response.output_text` |
| 取完整输出 | `response.choices` | `response.output` |
| Token | `response.usage.total_tokens` | `response.usage.total_tokens` |
| 续上下文 | 自己维护 `messages` | `previous_response_id` |

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx", base_url="你的地址")

response = client.responses.create(
    model="qwen3.8-max",
    input="介绍一下人工智能",# content
    instructions="你是一个友好的助手",# role
)

print(response.output_text)
print(response.usage.total_tokens)
```

```python
from openai import OpenAI

client = OpenAI(api_key="sk-xxx", base_url="你的地址")

stream = client.responses.create(
    model="qwen3.8-max",
    input="介绍一下人工智能",
    instructions="角色设定",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        print("\n总token:", event.response.usage.total_tokens)
```


## 两行自检

- ① 我说不出出处的知识点:无
- ② 学了但没落进任何行为的知识点:client.responses.create() 流式
