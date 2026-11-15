# 第13周 · FastAPI + Docker + docker-compose(工程化部署)

> 与主计划的差异说明:本周严格对应修订版路线图「阶段5前段」(17周映射第13周),主题为 FastAPI(路由/依赖注入/Pydantic/SSE 流式接口)、Docker(镜像/容器/Dockerfile)、docker-compose(多服务编排)与项目拆分。本周把第10-12周前端对接的后端正式**服务化 + 容器化**,直接支撑主计划作品集**项目1「商品知识库导购问答」(FastAPI + 向量库 + React SSE 流式)**的后端与上线,是第14周云端部署的地基。周闸门为 day91「本地一键起全链路(前端→FastAPI→LLM/RAG)」;阶段5 正式闸门在 day98(第14周末)。FastAPI/Docker/docker-compose 均在本周首教,与 reference 日程表第13周完全一致,不增删。
> 变更记录:首版(基于2026市场修订版生成)。
> 变更记录:2026-10-26 uv 引入预登记(学习者决策,待第13周检测时落地):uv(Astral 出品,pip+venv drop-in 加速替代)不进第04周 day22,正式落位本周——day85 主线仍 venv+pip(概念地基),加一行 uv 对照注记(`uv venv`/`uv pip install` 同构命令);day88 Dockerfile 增选做 `uv pip install --system` 提速构建变体。锚点=Astral 官方文档 docs.astral.sh/uv(需人工核验,现体系无中文 A 级教程页)。缘起见第04周 day22 排期讨论。
> 本周产物约定:固定产物置于 学习产物/第13周/dayN/,含 .py 与 Dockerfile / docker-compose.yml / requirements.txt / .dockerignore / .env.example;跟练统一命名 extra_* 放入 学习产物/第13周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。**大模型 key 一律从环境变量读取、零硬编码、不写进代码与镜像**(.env 不入库、被 .dockerignore 排除,compose 用 env_file 注入)。

## 本周概览

- 主题:把 AI 后端从"脚本"升级为"可部署服务"——用 FastAPI 暴露带类型校验的 HTTP/SSE 接口,用 Docker 固化运行环境,用 docker-compose 一键编排多服务。
- 为什么对拿offer有用:FastAPI 是当前 AI 应用后端的**主流框架**,招聘 JD 硬门槛技能里"后端/API"几乎默认指向它(自带 Pydantic 类型校验 + OpenAPI 文档,和你熟悉的 TS 类型心智高度契合);Docker 是部署与团队协作的**必备工程能力**(解决"在我机器上能跑"的顽疾),JD 高频要求"Linux + Git + Docker"。本周把第10-12周你写的 React 流式前端真正接到一个后端服务上,并容器化,是项目1上线、第14周云端部署的直接地基——面试时"我用 FastAPI 做了 SSE 流式后端并用 Docker Compose 编排上线"是可讲的完整工程闭环。
- 教材使用策略:主教材 黑马 FastAPI(A级视频)+ FastAPI 官方中文文档(60%),Docker 用 尚硅谷 Docker(A级视频)+ 官方文档搜索词(25%),菜鸟/廖雪峰做语法速查(15%)。FastAPI 部分优先用你的 Express/Koa + TS 经验做映射式理解,只重点看差异(装饰器路由、Pydantic 自动校验、依赖注入)。
- 本周结束时应能做到:
  1. 用 FastAPI 写带 Pydantic 请求/响应模型的路由,并用依赖注入(Depends)统一管理配置。
  2. 写一个 SSE 流式接口(后端从环境变量读 key 调国产大模型),让第10-12周的前端逐字接收。
  3. 用 Dockerfile 把 FastAPI 打包成镜像并 docker build/run 跑通;用 docker-compose 编排"api + 向量库"多服务并通过 env_file 注入 key。
  4. day91 周检测:45 分钟内独立盲写"含 SSE 流式接口的 FastAPI 服务(key 从环境变量读)+ 配套 Dockerfile",可构建运行。

## 前置知识点闭包(截至第12周已学)

Python 全栈基础:基础类型/print/input/f-string/控制流/for-while-range-enumerate/字符串切片与方法/list-tuple-dict-set/推导式/生成器表达式/random/datetime、def/docstring/参数全体系/lambda/map-filter/模块与包/import/闭包/nonlocal/装饰器、OOP(class/继承/多态/魔术方法/isinstance-type)/文件读写(open-with)/异常全体系(try-except-else-finally/raise/自定义异常)、venv/pip/requirements.txt/requests/正则 re/类型提示 typing/asyncio(async-await-asyncio.run-asyncio.sleep)。
AI 应用线:大模型 API 调用/**环境变量读 key(零硬编码)**/Prompt 工程/结构化输出 JSON Mode、流式 Streaming/Function Calling、LangChain/LCEL/RAG 全链路/向量库(Chroma/Milvus/Faiss)/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP(认知)。
前端线(TS):TS SSE/流式渲染/打字机效果、Vercel AI SDK(useChat)/LangChain.js/工具调用可视化、Agent 交互模式/React 流式对话组件。

本周新增(首教):FastAPI(路由 / 请求响应 / Pydantic 模型 / 依赖注入 Depends / SSE 或 WebSocket 流式接口)、Docker(镜像 / 容器 / Dockerfile / .dockerignore)、docker-compose(多服务编排 / env_file 环境变量注入)、项目拆分(后端分层:入口/客户端/服务)。
【超前】预警:Kubernetes(K8s)容器编排、CI/CD 流水线、Nginx 反向代理细节、HTTPS 证书/域名/备案(第14周正式教)、多阶段构建进阶与镜像深度瘦身、docker 网络高级配置、生产级 gunicorn 多 worker 调优、WebSocket 集群与心跳重连——本周均不作正式教学,若产物需要仅以【超前】最小片段出现并标注。

---

## Day85(周一,7h)· FastAPI 基础:路由 / 请求响应 / Pydantic 模型

今天正式进入 AI 应用后端。你写了十年前端,一直消费别人的 API;从今天起你自己写 API。FastAPI 对你异常友好——它像 Express/Koa 一样用路由,但内建了 Pydantic 类型校验(≈ zod)与自动 OpenAPI 文档(≈ Swagger,你团队的 TS 类型契约在这里自动生成)。产出:一个带 Pydantic 请求/响应模型的最小 FastAPI 服务。

💡 JS开发者速读:心智模型高度可迁移——`@app.get("/")` ≈ Express `app.get("/", handler)`;Pydantic 的 `BaseModel` ≈ zod schema / TS interface,**但会自动校验请求体并返回 422**(Express 要手写校验);函数参数写类型注解即自动解析 query/body(≈ 装饰器注入,TS 里没有这么自动的);最大差异:FastAPI 靠**装饰器 + 类型注解**驱动,而不是链式中间件;启动用 `uvicorn main:app`(≈ nodemon/node 起服务)。

### 学习内容

- 安装与启动:venv 内 `pip install fastapi uvicorn`,用 `uvicorn main:app --reload` 起服务(JS对应 npm i express + node 起服务)
- 路由装饰器 `@app.get/@app.post` 与路径/查询参数(JS对应 app.get/app.post + req.params/req.query)
- Pydantic `BaseModel` 定义请求体/响应模型,自动校验与序列化(JS对应 zod schema / TS interface)
- 自动交互式文档 `/docs`(OpenAPI/Swagger,前端联调利器)
- 项目拆分意识:入口(app)、模型(schemas)、路由分离(JS对应 routes/models 分层)

### 讲解

结论先行:FastAPI 的核心红利是"类型注解即契约"——你用 Pydantic 声明请求体结构,框架自动完成解析、校验、错误提示与文档生成,这正是 TS 给你的安全感在后端的翻版。下面是最小可运行骨架(教学演示,**不是**当日产物答案),产物需你补充更完整的模型与多路由。

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):          # Pydantic 模型:自动校验+序列化(≈ zod schema)
    name: str
    price: float

@app.get("/")                    # 路由装饰器(≈ Express app.get)
def root():
    return {"msg": "服务已启动"}

@app.post("/items")
def create_item(item: Item):     # 请求体自动解析为 Item 并校验
    return {"ok": True, "name": item.name}
```

### 教材与章节

- 主教材/视频(A级,已核验):黑马 FastAPI 从入门到实战 https://yun.itheima.com/course/1084.html
- 速查:FastAPI 官方中文文档 — 教程/第一步、请求体与 Pydantic https://fastapi.tiangolo.com/zh/
- 语法速查:菜鸟教程 Python3 https://www.runoob.com/python3/ ;搜索词「FastAPI Pydantic 请求模型 响应模型 中文」

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 安装启动、路由装饰器、路径/查询参数、Pydantic 请求响应模型、/docs 文档 精读+敲示例 |
| 技术练习 | 2h | 编写 main.py + requirements.txt + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 FastAPI 官方英文文档片段 |
| 输出 | 1h | GitHub commit(本项目新建后端目录),记录 /docs 截图为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第13周/day85/main.py:最小 FastAPI 服务(≤120行)
  - 定义至少两个 Pydantic 模型(一个请求体模型、一个响应模型),字段含类型注解
  - 实现至少三个路由:一个 GET 根路由(返回服务状态)、一个带路径/查询参数的 GET、一个接收 Pydantic 请求体的 POST(校验通过后返回响应模型)
  - 启动后能访问 /docs 看到自动生成的交互式文档(在 index.md 记录访问方式)
  - python 层面:`uvicorn main:app --reload` 可启动,curl 或 /docs 试调各路由均正常
  - 所用知识点清单:FastAPI 实例、路由装饰器(get/post)、路径参数、查询参数、Pydantic BaseModel、类型注解(typing 复用)、返回 dict/响应模型
- [ ] 编写 学习产物/第13周/day85/requirements.txt:锁定 fastapi、uvicorn 版本(venv 内 `pip freeze` 生成)
- [ ] 补记 学习产物/第13周/day85/index.md:覆盖全部学习内容(代码块纯 Python 可运行,启动命令用文本标注)

### JS→Python对照笔记

- JS `const app = express()` → Python `app = FastAPI()`
- JS `app.get("/x", (req,res)=>...)` → Python `@app.get("/x")` + `def x():`
- JS `req.params.id` / `req.query.q` → Python 路由函数参数 `id: str` / `q: str`(自动解析)
- JS zod schema 校验 body → Python Pydantic `BaseModel`(校验失败自动 422)
- JS 手写 Swagger → Python 自动生成 `/docs`(OpenAPI)
- JS `node index.js` / nodemon → Python `uvicorn main:app --reload`

### 跟练清单(放extra/)

- extra_health.py:给服务补一个 `/health` 健康检查路由(返回状态与一个用 datetime 生成的时间戳)和一个返回响应模型的 GET 路由,练习多路由与响应模型复用。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| FastAPI 路由/请求响应/Pydantic 模型/项目拆分 | 黑马FastAPI;FastAPI官方中文-教程 | main.py + requirements.txt | FastAPI 路由装饰器、路径/查询参数、Pydantic BaseModel、类型注解、/docs |

【超前】标注集中区:本日无超前内容(依赖注入 Depends 明日深入;Nginx/HTTPS 属第14周)。
硬约束复查:仅用 day85 闭包知识点 ✓ 第三方库合规(fastapi/uvicorn,Day22 已解禁,写入 requirements.txt)✓ key 零硬编码(本日不涉及 key)✓ .py≤120行 ✓ extra/命名正确 ✓

---

## Day86(周二,7h)· FastAPI 流式接口:SSE(对接第10-12周前端)

今天写你前端消费了两周的那个"服务端"。第10-12周你在 React 里用 EventSource/fetch 消费 SSE 流、做打字机效果;今天你亲手写产出这条流的后端接口。这是项目1"React SSE 流式"的服务端一半,也是面试最能讲的差异化点(前端×LLM 交互层)。产出:一个 SSE 流式接口。

💡 JS开发者速读:SSE 的**帧格式**你早已烂熟(`data: ...\n\n`)——今天只是在服务端产出它。差异:Express 里你要手动 `res.write("data: ...\n\n")` 并保持连接;FastAPI 用 `StreamingResponse` 包一个**异步生成器**(async generator,`yield` 逐块产出),`media_type="text/event-stream"`。异步生成器 ≈ JS 的 `async function*` + `yield`,心智可直接迁移;`await asyncio.sleep()` 模拟大模型逐 token 返回的延迟。

### 学习内容

- `StreamingResponse` + 异步生成器(`async def` + `yield`)产出 SSE 流(JS对应 async function* + res.write)
- SSE 帧格式 `data: <内容>\n\n` 与 `media_type="text/event-stream"`(前端第10周消费的正是它)
- 流式中 `await asyncio.sleep()` 模拟逐 token 延迟(复用 day26 asyncio)
- WebSocket 接口作为双向流的另一种选择(认知:SSE 单向足够 LLM 流式,WS 适合双向)
- 与前端联调:第10-12周的 useChat/EventSource 直接对接本接口

### 讲解

结论先行:SSE 后端 = 一个不断 `yield` "data: 片段\n\n" 的异步生成器,交给 `StreamingResponse` 以 `text/event-stream` 持续推送。浏览器 EventSource 收到一帧就触发一次 onmessage,这正是你前端打字机效果的数据源。下面是流式路由骨架(教学演示,**不是**产物答案),产物需接入真实内容源。

```python
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def token_stream():                 # 异步生成器:逐块产出(≈ async function*)
    for word in ["你好", "，", "世界", "!"]:
        yield f"data: {word}\n\n"          # SSE 帧格式(前端 EventSource 消费)
        await asyncio.sleep(0.3)           # 模拟大模型逐 token 延迟

@app.get("/stream")
def stream():
    return StreamingResponse(token_stream(), media_type="text/event-stream")
```

### 教材与章节

- 主教材/视频(A级,已核验):黑马 FastAPI https://yun.itheima.com/course/1084.html
- 速查:FastAPI 官方中文文档 https://fastapi.tiangolo.com/zh/ ;搜索词「FastAPI StreamingResponse SSE 流式 服务端」
- 语法速查:Python 官方中文 asyncio(异步生成器)https://docs.python.org/zh-cn/3/library/asyncio.html

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | StreamingResponse、异步生成器、SSE 帧格式、WebSocket 认知、与前端联调 精读+敲示例 |
| 技术练习 | 2h | 编写 sse_api.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 FastAPI/MDN SSE 英文文档片段 |
| 输出 | 1h | GitHub commit;用第10-12周前端页面联调,截图流式效果为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第13周/day86/sse_api.py:FastAPI SSE 流式服务(≤120行)
  - 实现一个 GET SSE 接口:用异步生成器逐块 `yield` "data: ...\n\n" 帧,以 text/event-stream 返回
  - 内容源可为"把一段固定文本按字/词切分逐块推送"(用 asyncio.sleep 模拟节奏);本阶段先不接大模型(day87 接入)
  - 再实现一个 POST 接口:接收 Pydantic 请求体(如用户问题),把问题回显进流式内容,体现"请求→流式响应"
  - 用第10-12周的前端页面或 curl -N 验证流式逐块到达(在 index.md 记录验证方式)
  - 所用知识点清单:FastAPI 路由、StreamingResponse、异步生成器(async def + yield)、SSE 帧格式、asyncio.sleep、Pydantic 请求模型、media_type
- [ ] 补记 学习产物/第13周/day86/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `async function*` + `yield` → Python `async def` + `yield`(异步生成器)
- JS Express `res.write("data: x\n\n")` → Python `yield f"data: {x}\n\n"` 交给 StreamingResponse
- JS `res.setHeader("Content-Type","text/event-stream")` → Python `media_type="text/event-stream"`
- JS 前端 `new EventSource("/stream")` → 对接本日后端 GET /stream(格式一致)
- JS `setTimeout` 延时 → Python `await asyncio.sleep()`(不阻塞事件循环)

### 跟练清单(放extra/)

- extra_ws_echo.py:用 FastAPI WebSocket 写一个"回声"接口(客户端发什么、服务端流式回什么),对比 SSE 单向流,体会两种流式接口的适用场景。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| FastAPI SSE 流式接口/异步生成器/WebSocket 认知 | 黑马FastAPI;FastAPI官方中文;Python官方-asyncio | sse_api.py | StreamingResponse、异步生成器、SSE 帧格式、asyncio.sleep、Pydantic、路由 |

【超前】标注集中区:WebSocket 心跳/断线重连/集群属【超前】,本日仅认知 WS 存在与基本用法,不深入;生产级 SSE 反代缓冲关闭(Nginx X-Accel-Buffering)属第14周/【超前】。
硬约束复查:仅用 day86 闭包知识点 ✓ 第三方库合规(fastapi/uvicorn)✓ key 零硬编码(本日不接大模型,不涉及 key)✓ .py≤120行 ✓ extra/命名正确 ✓

---

## Day87(周三,7h)· 后端接入国产大模型 API + 依赖注入(key 从环境变量,前端零暴露)

今天把昨天的"假流式"接上真实大模型,并解决一个前端老手最容易踩的安全坑:key 绝不能放在前端。做法是——后端做**代理层**:key 从环境变量读(复用第05周能力),前端只调你的后端,后端持 key 调国产大模型再把流转发回前端。同时学 FastAPI 的依赖注入(Depends),优雅管理配置与客户端。产出:一个大模型流式代理服务。

💡 JS开发者速读:这就是你熟悉的 **BFF(Backend For Frontend)代理模式**——前端不碰密钥,后端代持并转发。差异:FastAPI 的 `Depends(get_settings)` ≈ Express 的中间件/上下文注入,但更声明式(在路由参数里写 `= Depends(...)` 即自动注入),比 React 的 Context/Provider 更贴近"函数级依赖注入"。key 读取沿用你在 Node 里的 `process.env.KEY` 心智 → Python 是 `os.getenv("KEY")`(第05周已学)。

### 学习内容

- 依赖注入 `Depends`:把"读配置/建客户端"抽成依赖函数,路由参数注入(JS对应 中间件/上下文注入)
- 环境变量读 key:`os.getenv("LLM_API_KEY")`,零硬编码、启动即校验是否为空(复用第05周)
- 后端代理国产大模型(通义千问/DeepSeek/GLM):后端持 key 调用,把返回流转成 SSE 转发前端
- 流式对接:大模型的流式响应 → 逐块 yield 成 SSE 帧(串起 day86)
- 安全:.env 存 key 且不入库、被 .dockerignore 排除;compose 用 env_file 注入(day88-89 落实)

### 讲解

结论先行:依赖注入让"配置/客户端"成为可测试、可替换的依赖,而不是散落各处的全局变量;key 只在后端环境变量里,前端永远拿不到。下面演示 `Depends` 注入一个从环境变量读 key 的配置依赖(**教学演示,不是产物答案**;真实调用大模型的逻辑由你在产物中实现)。

```python
import os
from fastapi import FastAPI, Depends

app = FastAPI()

def get_settings():                        # 依赖:统一从环境变量读 key(零硬编码)
    return {"api_key": os.getenv("LLM_API_KEY", "")}

@app.post("/chat")
def chat(s=Depends(get_settings)):         # Depends 注入配置(≈ 中间件/上下文注入)
    if not s["api_key"]:
        return {"error": "未配置 LLM_API_KEY 环境变量"}   # 后端持 key,前端不接触
    return {"ok": True}                    # 实际调用国产大模型 + 转 SSE 流(产物中实现)
```

### 教材与章节

- 主教材/视频(A级,已核验):黑马 FastAPI https://yun.itheima.com/course/1084.html
- 速查:FastAPI 官方中文文档(依赖注入)https://fastapi.tiangolo.com/zh/ ;国产大模型官方文档(A级)DeepSeek https://platform.deepseek.com/api-docs/zh-cn/ 、阿里云百炼通义千问 https://help.aliyun.com/zh/model-studio/qwen-function-calling 、智谱 GLM https://docs.bigmodel.cn/cn/guide/develop/http/introduction
- 语法速查:菜鸟教程 Python3 https://www.runoob.com/python3/ ;搜索词「FastAPI 依赖注入 Depends 中文」

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 依赖注入 Depends、os.getenv 读 key、国产大模型 API 调用、流式转 SSE 精读+敲示例 |
| 技术练习 | 2h | 编写 llm_proxy.py + .env.example + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读大模型 API 英文文档片段 |
| 输出 | 1h | GitHub commit(确认 .env 已被忽略、未上传);记录代理层设计为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检 key 零硬编码 |

### 当日产出

- [ ] 编写 学习产物/第13周/day87/llm_proxy.py:大模型流式代理服务(≤120行)
  - 用依赖注入(Depends)提供一个"读环境变量 key 与模型配置"的依赖函数;启动或首次调用时校验 key 是否为空,为空返回明确错误提示
  - 实现一个流式接口:接收前端问题(Pydantic 模型),后端持 key 调用一个国产大模型(通义千问/DeepSeek/GLM 任选),把返回内容逐块以 SSE 帧转发给前端
  - key 全程从环境变量读取,代码中**不得出现任何明文 key**;不实际打印 key 值
  - 前端(第10-12周页面)调本服务即可流式收到大模型回答,前端不接触 key
  - 所用知识点清单:FastAPI 依赖注入 Depends、os.getenv(第05周)、Pydantic 模型、StreamingResponse/异步生成器(day86)、国产大模型 API 调用(第05-06周)、异常处理、f-string
- [ ] 编写 学习产物/第13周/day87/.env.example:列出所需环境变量名(如 LLM_API_KEY=、MODEL_NAME=),仅示例占位、**不含真实 key**;真实 .env 不入库
- [ ] 补记 学习产物/第13周/day87/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `process.env.LLM_API_KEY` → Python `os.getenv("LLM_API_KEY")`(第05周已学)
- JS Express 中间件 `app.use(inject)` → Python 路由参数 `s=Depends(get_settings)`(声明式注入)
- JS React Context/Provider 传依赖 → Python Depends(函数级依赖注入,更贴近后端)
- JS BFF 代理转发流 → Python 后端调大模型 + StreamingResponse 转 SSE
- JS `.env` + dotenv → Python `.env`(由 compose env_file 或运行环境注入,不入库)

### 跟练清单(放extra/)

- extra_env_guard.py:封装一个 `get_key(name)` 安全读取函数——从环境变量读指定 key,为空时抛出自定义异常(复用第03周)并给出配置提示;写几组用例验证"有值/缺失"两种情况均不泄露真实值。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 依赖注入/环境变量读 key/大模型代理/SSE 转发 | 黑马FastAPI;FastAPI官方中文;大模型官方文档 | llm_proxy.py + .env.example | Depends、os.getenv、Pydantic、StreamingResponse、异步生成器、大模型 API、异常、f-string |

【超前】标注集中区:key 的密钥管理服务(Vault/KMS)、限流与鉴权中间件(JWT/OAuth)属【超前】,本日仅用环境变量 + 空值校验,不深入。
硬约束复查:仅用 day87 闭包知识点 ✓ 第三方库合规(fastapi/uvicorn/大模型 SDK)✓ **key 零硬编码(环境变量读取,.env 不入库)** ✓ .py≤120行 ✓ extra/命名正确 ✓

---

## Day88(周四,7h)· Docker 基础:镜像 / 容器 / Dockerfile 打包 FastAPI

今天解决那个折磨过你无数次的"在我机器上能跑,到别人/服务器就挂"的问题。Docker 把运行环境(Python 版本、依赖、系统库)连同你的代码一起固化成**镜像**,任何装了 Docker 的机器都能一模一样地跑起来。这是第14周云端部署的前提——服务器上你只需 docker run 一个镜像。产出:一个能打包并运行 FastAPI 的 Dockerfile。

💡 JS开发者速读:Docker ≈ 把整个 `node_modules + node 运行时 + 你的代码`冻结成一个可移植快照,再也不用 `npm install` 对环境;`Dockerfile` ≈ 一份"构建配方"(像 CI 的 build 脚本);`docker build` ≈ `npm run build` 产出制品;`docker run` ≈ 起一个隔离的服务实例(比 pm2 更彻底,连 OS 依赖都隔离)。`requirements.txt` 在镜像里对应你熟悉的 `package.json` 锁依赖;`EXPOSE`/`-p` 端口映射 ≈ 你配的服务端口。

### 学习内容

- 镜像 vs 容器:镜像是只读模板,容器是运行实例(JS对应 构建制品 vs 运行进程)
- Dockerfile 指令:FROM / WORKDIR / COPY / RUN / EXPOSE / CMD(JS对应 构建配方)
- 构建与运行:`docker build -t myapi .`、`docker run -p 8000:8000 myapi`(JS对应 build + 起服务)
- 依赖分层与构建缓存:先 COPY requirements.txt 再 RUN pip install(改代码不重装依赖)
- .dockerignore:排除 .env / .venv / __pycache__(**防止 key 与本地环境进镜像**)

### 讲解

结论先行:Dockerfile 就是"从基础镜像出发,拷依赖→装依赖→拷代码→声明端口→定义启动命令"的配方;把 `pip install` 放在拷贝代码之前,能利用构建缓存大幅加速重建。**务必用 .dockerignore 排除 .env**,否则 key 会被打进镜像层泄露。下面是最小 Dockerfile(教学演示,**不是**产物答案)。

```dockerfile
# 最小 Dockerfile:把 FastAPI 固化成镜像
FROM python:3.12-slim            # 基础镜像(≈ 运行时基座)
WORKDIR /app                     # 容器内工作目录
COPY requirements.txt .          # 先拷依赖清单(利用构建缓存)
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                         # 再拷源码
EXPOSE 8000                      # 声明服务端口
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 教材与章节

- 主教材/视频(A级,已核验):尚硅谷 3 小时速通 Docker https://www.atguigu.com/video/307
- 速查:Docker 官方文档——用中文搜索词「Docker 官方文档 Dockerfile 指令 中文」定位(本环境不杜撰具体链接)
- 语法速查:菜鸟教程 Python3 https://www.runoob.com/python3/ ;搜索词「Docker 打包 FastAPI uvicorn 镜像」

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 镜像/容器概念、Dockerfile 六指令、build/run、构建缓存、.dockerignore 精读+实操 |
| 技术练习 | 2h | 编写 Dockerfile + .dockerignore,build 并 run 起 day85 的 FastAPI |
| 英语 | 0.5h | AI 辅助精读 Docker 官方英文文档片段 |
| 输出 | 1h | GitHub commit(Dockerfile/.dockerignore,确认无 .env);记录镜像构建流程 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检 key 未进镜像 |

### 当日产出

- [ ] 编写 学习产物/第13周/day88/Dockerfile:打包 FastAPI 服务(简洁可用为准)
  - 基于官方 python slim 基础镜像;设工作目录;先 COPY requirements.txt 再 RUN pip install(利用缓存);再 COPY 源码;EXPOSE 服务端口;CMD 用 uvicorn 启动 day85 的 main:app(监听 0.0.0.0)
  - `docker build -t <镜像名> .` 能成功构建;`docker run -p 8000:8000 <镜像名>` 能起服务并访问 /docs
  - 通过环境变量注入 key(`docker run -e LLM_API_KEY=... ` 或后续 compose env_file),镜像内**不含明文 key**
- [ ] 编写 学习产物/第13周/day88/.dockerignore:排除 .env、.venv/venv、__pycache__、*.pyc、.git 等,确保 key 与本地环境不进镜像
- [ ] 补记 学习产物/第13周/day88/index.md:覆盖全部学习内容,记录 build/run 命令(命令用文本标注)

### JS→Python对照笔记

- JS `npm run build` 产出 dist → Python `docker build` 产出镜像
- JS package.json 锁依赖 → Python requirements.txt(镜像内 pip install)
- JS `node server.js` / pm2 起服务 → Python `docker run` 起容器(CMD 定义启动)
- JS `.gitignore` 忽略敏感/构建物 → Python `.dockerignore` 忽略 .env/.venv(防 key 进镜像)
- JS 端口 `PORT=8000` → Python Dockerfile `EXPOSE 8000` + `docker run -p 8000:8000`

### 跟练清单(放extra/)

- extra_Dockerfile.slim:写一个更精简的 Dockerfile 变体(如用更小的基础镜像标签或合并 RUN 层减少体积),对比构建出的镜像大小,练习镜像瘦身意识(深度多阶段构建属【超前】,仅体验)。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 镜像/容器/Dockerfile/build-run/.dockerignore | 尚硅谷Docker;Docker官方文档(搜索词) | Dockerfile + .dockerignore | FROM/WORKDIR/COPY/RUN/EXPOSE/CMD、构建缓存、端口映射、.dockerignore 排除 .env |

【超前】标注集中区:多阶段构建、镜像深度瘦身、docker 网络/卷高级配置属【超前】,本日仅识别;K8s/CI-CD 不在本周范围。
硬约束复查:仅用 day88 闭包知识点 ✓ 第三方库合规(docker 为工具,非 pip 库)✓ **key 零硬编码(.dockerignore 排除 .env,镜像无明文 key)** ✓ Dockerfile 简洁可用 ✓ extra/命名正确 ✓

---

## Day89(周五,7h)· docker-compose:FastAPI + 向量库多服务编排 + env 注入

今天从"单个容器"升级到"一组容器协同"。真实的 AI 后端不止一个服务:FastAPI 应用 + 向量库(项目1 用 pgvector/Chroma/Milvus)+ 可能的 DB。手动 docker run 一个个起太痛苦,docker-compose 用一个 yml 文件声明所有服务、网络、依赖与环境变量,一条命令全起。这是项目1"本地一键起全链路"的关键。产出:一份编排 api + 向量库的 docker-compose.yml。

💡 JS开发者速读:docker-compose.yml ≈ 一个"多服务版的 package.json scripts + 环境声明"——你在 monorepo 里用 `concurrently` 或 docker-compose 起前端+后端+DB 的经验可迁移;`services` ≈ 你的多个 workspace 包;`depends_on` ≈ 启动顺序依赖(像 `wait-on`);`env_file` ≈ 把 `.env` 喂给容器(≈ dotenv,但注入到容器环境);`ports` ≈ 端口映射;`build` vs `image` ≈ 本地构建 vs 拉现成镜像(≈ 自建包 vs npm 依赖)。

### 学习内容

- compose 文件结构:services / 每个服务的 build 或 image / ports / env_file / depends_on(JS对应 monorepo 多服务编排)
- 用 build 起 FastAPI(复用 day88 Dockerfile),用 image 起向量库/DB 现成镜像
- env_file 注入环境变量(key 走 .env,**不写进 compose 明文、不进镜像**)
- depends_on 控制启动顺序(api 依赖向量库先起)
- 一键起停:`docker compose up -d` / `docker compose down`(JS对应 一条命令起全套)

### 讲解

结论先行:compose 把"多容器 + 网络 + 环境变量 + 启动依赖"声明在一个 yml 里,`docker compose up` 即拉起整条链路。key 用 `env_file` 从 .env 注入容器环境,既不进代码也不进镜像,安全且可移植。下面是最小编排骨架(教学演示,**不是**产物答案;向量库镜像名请按你项目1实际选型替换)。

```yaml
# 多服务编排:FastAPI + 向量库(≈ 多容器版 package.json scripts)
services:
  api:
    build: .                    # 用当前目录 Dockerfile 构建(day88)
    ports:
      - "8000:8000"
    env_file: .env              # 从 .env 注入 key(不写死、不进镜像)
    depends_on:
      - vectordb                # 等向量库先起
  vectordb:
    image: <你的向量库镜像>       # 如 pgvector / chroma,按项目1选型替换
    ports:
      - "8001:8000"
```

### 教材与章节

- 主教材/视频(A级,已核验):尚硅谷 3 小时速通 Docker(含 compose 章节)https://www.atguigu.com/video/307
- 速查:Docker 官方文档 Compose——用中文搜索词「docker compose 官方文档 多服务 编排 env_file 中文」定位(本环境不杜撰具体链接)
- 语法速查:FastAPI 官方中文(部署)https://fastapi.tiangolo.com/zh/ ;搜索词「docker-compose FastAPI 向量库 编排」

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | compose 结构、build/image、ports/env_file/depends_on、up/down 精读+实操 |
| 技术练习 | 2h | 编写 docker-compose.yml 编排 api + 向量库,`docker compose up` 起全链路 |
| 英语 | 0.5h | AI 辅助精读 Docker Compose 英文文档片段 |
| 输出 | 1h | GitHub commit(compose + .env.example,确认 .env 未上传);记录一键起链路 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检 key 走 env_file |

### 当日产出

- [ ] 编写 学习产物/第13周/day89/docker-compose.yml:多服务编排(简洁可用为准)
  - 声明两个服务:api(build 当前目录,复用 day88 Dockerfile,映射端口)与 vectordb(image 用项目1 选型的向量库镜像,如 pgvector/Chroma,映射端口)
  - api 通过 `env_file: .env` 注入大模型 key 与向量库连接配置;`depends_on` 让 api 等 vectordb 先起
  - compose 文件中**不出现任何明文 key**;真实 .env 不入库,仅提交 .env.example
  - `docker compose up -d` 能一键起 api + 向量库,`docker compose down` 能干净停止;访问 api /docs 正常
- [ ] 复用/编写 学习产物/第13周/day89/.env.example:列出 api 所需环境变量名(LLM_API_KEY、向量库地址等),占位不含真实值
- [ ] 补记 学习产物/第13周/day89/index.md:覆盖全部学习内容,记录 up/down 命令(文本标注)

### JS→Python对照笔记

- JS monorepo `concurrently`/docker-compose 起多服务 → Python `docker compose up`(一份 yml 声明全部)
- JS 包 `build` 自建 vs `dependencies` 拉现成 → compose `build:` vs `image:`
- JS `wait-on` 等依赖就绪 → compose `depends_on`(仅启动顺序,就绪探测属【超前】)
- JS dotenv 读 .env → compose `env_file: .env`(注入容器环境变量)
- JS `PORT` 映射 → compose `ports: "宿主:容器"`

### 跟练清单(放extra/)

- extra_compose.env_demo.yml:写一个 compose 覆盖/示例变体,演示用 `environment` 直接注入非敏感变量(如日志级别)与用 `env_file` 注入敏感 key 的区别,并加注释说明为何 key 不写进 compose 明文。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| docker-compose 多服务编排/env_file/depends_on | 尚硅谷Docker;Docker官方文档(搜索词) | docker-compose.yml + .env.example | services、build/image、ports、env_file、depends_on、up/down |

【超前】标注集中区:healthcheck 就绪探测、compose 网络/卷高级配置、多机 Swarm 属【超前】,本日 depends_on 仅保证启动顺序,不深入就绪探测。
硬约束复查:仅用 day89 闭包知识点 ✓ 第三方库合规(docker compose 为工具)✓ **key 零硬编码(env_file 注入,compose 无明文,.env 不入库)** ✓ compose 简洁可用 ✓ extra/命名正确 ✓

---

## Day90(周六,7h)· 综合项目实战:RAG/Agent 后端服务化 + 容器化一键起

今天是项目日,把本周(FastAPI + SSE + 依赖注入 + Docker + compose)与第07-09周的 RAG/Agent 能力拧成一个**可一键起的后端服务**——这就是项目1「商品知识库导购问答」的后端骨架:前端提问 → FastAPI(依赖注入配置)→ RAG 检索 → 大模型流式生成 → SSE 回推前端,全部用 docker-compose 编排。产出:容器化的 RAG 后端 + compose,本地一键起全链路(即本周闸门能力预演)。

💡 JS开发者速读:这就是你在前端做过的"数据层 + 服务层 + 展示层"分层,只是搬到了后端并容器化。整体像你搭过的全栈脚手架(Vite 前端 + Node BFF + DB),差异在:后端用 FastAPI 的 Depends 做依赖注入(比 React Context 更函数级)、用 docker-compose 编排(比 concurrently 更彻底隔离)。RAG/Agent 逻辑你在第07-09周已写熟,今天是"把它包进服务 + 装进容器"。

### 学习内容(综合复用,无全新理论)

- 项目拆分分层:入口(main:路由/SSE)、客户端(llm_client:读 env key 调大模型)、服务(rag_service:检索)
- 用依赖注入把"配置/向量库客户端/大模型客户端"注入到路由(复用 day87)
- 把 RAG 检索(第07-08周)接进 SSE 流式接口(复用 day86):检索结果 + 大模型生成 → 逐块 yield
- 用 Dockerfile 打包后端(复用 day88)、docker-compose 编排 api + 向量库(复用 day89)
- 一键起全链路:`docker compose up` 后,前端(第10-12周)→ FastAPI → RAG/大模型 跑通

### 讲解

结论先行:综合项目的关键是"分层解耦 + 依赖注入 + 容器编排"三件事同时到位——每层单一职责、配置与客户端用 Depends 注入(便于测试与替换 key 来源)、最后用 compose 把 api 与向量库一键拉起。下面只演示**项目目录分层结构**(教学演示,**不是**产物答案,各层实现由你完成)。

```text
rag_backend/                 # 综合项目分层(结构演示,非产物答案)
├── main.py                  # FastAPI 入口:路由 + SSE 流式接口
├── llm_client.py            # 大模型客户端:key 从环境变量读(零硬编码)
├── rag_service.py           # RAG 检索:复用第07-08周能力
├── requirements.txt         # 依赖锁定
├── Dockerfile               # 打包后端为镜像(day88)
├── docker-compose.yml       # 编排 api + 向量库(day89)
└── .dockerignore            # 排除 .env/.venv(防 key 进镜像)
```

### 教材与章节

- 主教材/视频(A级,已核验):黑马 FastAPI https://yun.itheima.com/course/1084.html + 尚硅谷 Docker https://www.atguigu.com/video/307(综合)
- 速查:FastAPI 官方中文文档 https://fastapi.tiangolo.com/zh/ ;Docker/Compose 官方文档用中文搜索词定位
- 语法速查:廖雪峰 Python(综合回顾)https://liaoxuefeng.com/books/python/ ;菜鸟教程 Python3 https://www.runoob.com/python3/

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画分层结构与依赖注入方案、想清 RAG→SSE 数据流与异常场景(含英语 0.5h) |
| 项目实战 | 3.5h | 编写 rag_service.py + Dockerfile + docker-compose.yml,准备本地语料 |
| 输出 | 1h | GitHub commit(确认 .env 未上传);把架构图/一键起链路整理为项目1 README 素材 |
| 复盘 | 0.5h | 补 index.md,自检闭包合规与 key 安全,列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第13周/day90/rag_service.py:容器化 RAG 后端(项目日,≤150行)
  - 分层:FastAPI 入口暴露一个 SSE 流式问答接口;用依赖注入提供"配置 + 向量库客户端 + 大模型客户端"
  - 数据流:接收前端问题(Pydantic)→ 调 RAG 检索(复用第07-08周,检索商品知识库)→ 把检索片段 + 问题交大模型(key 从环境变量读)→ 生成内容逐块 yield 成 SSE 帧回推
  - 健壮性:用 try/except 兜底检索/大模型调用异常,失败时以 SSE 帧返回友好错误,不使整个服务崩溃
  - 配套 Dockerfile 与 docker-compose.yml(编排 api + 向量库,env_file 注入 key);`docker compose up` 后,用第10-12周前端页面提问可流式收到"带检索依据"的回答
  - 所用知识点清单:FastAPI 路由/依赖注入 Depends、Pydantic、StreamingResponse/异步生成器、SSE 帧、os.getenv、RAG 检索(第07-08周)、大模型 API(第05-06周)、异常处理、Dockerfile、docker-compose/env_file
- [ ] 编写 学习产物/第13周/day90/Dockerfile 与 docker-compose.yml(简洁可用为准;key 走 env_file,.dockerignore 排除 .env)
- [ ] 补记 学习产物/第13周/day90/index.md:覆盖分层设计思路与全部学习内容

### JS→Python对照笔记

- JS 前端数据层/服务层/展示层分层 → Python main(入口)/llm_client(客户端)/rag_service(服务)分层
- JS React Context 传依赖 → Python FastAPI Depends(函数级依赖注入)
- JS Vite+Node BFF+DB 用 concurrently 起 → Python docker compose up 起 api+向量库
- JS fetch 消费 SSE → 前端不变,后端本日提供真实 RAG+大模型 SSE 源
- JS `process.env` → Python `os.getenv`(key 从 compose env_file 注入)

### 跟练清单(放extra/)

- extra_readiness.py:给综合服务加一个 `/ready` 就绪探针路由——检查向量库是否可连、key 是否已配置,返回就绪状态(为第14周云端部署的健康检查做铺垫;真实 compose healthcheck 属【超前】)。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| FastAPI+依赖注入+SSE+RAG+Docker+compose 综合 | 黑马FastAPI;尚硅谷Docker;FastAPI官方中文;廖雪峰 | rag_service.py + Dockerfile + docker-compose.yml | 路由、Depends、Pydantic、StreamingResponse、异步生成器、os.getenv、RAG 检索、大模型 API、异常、Dockerfile、compose/env_file |

【超前】标注集中区:compose healthcheck 就绪探测、gunicorn 多 worker、Nginx 反代/HTTPS(第14周)、K8s 编排属【超前】,本日仅以 extra 的 /ready 路由做认知铺垫,不深入。
硬约束复查:仅用 day90 闭包知识点 ✓ 第三方库合规(fastapi/uvicorn/大模型 SDK/向量库客户端)✓ **key 零硬编码(env_file 注入,.dockerignore 排除 .env)** ✓ 项目日 .py≤150行、Dockerfile/compose 简洁可用 ✓ extra/命名正确 ✓

---

## Day91(周日,7h)· 周检测 + 对账

今天是本周闸门。目标是限时独立完成一个"含 SSE 流式接口的 FastAPI 服务(后端从环境变量读 key 调国产大模型)+ 配套 Dockerfile",验证你已能把 AI 后端服务化并容器化。通过后即具备"本地一键起全链路"能力,可平稳进入第14周(云端部署),冲击 day98 阶段5 闸门(作品公网可点开)。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第13周/day91/sse_llm_service.py 与配套 Dockerfile:

1. 用 FastAPI 建服务,实现一个 SSE 流式接口(GET 或 POST),以 text/event-stream 逐块 yield "data: ...\n\n" 帧。
2. 后端从环境变量读取大模型 key(os.getenv),**代码中不得出现任何明文 key**;key 缺失时返回明确错误提示而非崩溃。
3. 用该 key 调用一个国产大模型(通义千问/DeepSeek/GLM 任选),把回答逐块转发成 SSE 流(可先用固定文本模拟流式,再替换为真实调用)。
4. 编写配套 Dockerfile:基于 python slim 镜像,装 requirements,用 uvicorn 启动;确保 .env 不进镜像(配 .dockerignore 或用 -e/env 注入)。
5. `docker build` 能构建、`docker run -p 8000:8000 -e LLM_API_KEY=... ` 能起服务,curl -N 或前端能收到流式响应。

通过标准(须全部满足):

- 45 分钟内完成,`uvicorn sse_llm_service:app` 本地可启动、SSE 接口能持续吐帧;
- 正确使用 FastAPI + StreamingResponse/异步生成器产出合规 SSE 帧;
- **key 从环境变量读取、零硬编码**,镜像与代码内均无明文 key;
- Dockerfile 可 `docker build` 成功并 `docker run` 起服务(端口映射正确、能访问接口);
- 仅用截至 day91 的闭包知识点,**可用第三方库**(fastapi/uvicorn/大模型 SDK,写入 requirements.txt),.py ≤180 行(周末检测放宽)。

未通过补救方案:

- 仅个别 FastAPI/SSE 写法出错 → 当天用缓冲 1h 对照 Day86/Day87 讲解订正,次日重盲写一次(≤45min);
- SSE 流式或 Dockerfile 构建逻辑不通 → 重做 Day86 + Day88,再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第14周前 2 天先补 FastAPI/Docker 欠账,再进入云端部署,**本周闸门顺延但不取消**(day98 阶段5 闸门相应顺延)。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day85/main.py ☐ day85/requirements.txt ☐ day85/extra/extra_health.py ☐ day85/index.md ☐
   - day86/sse_api.py ☐ day86/extra/extra_ws_echo.py ☐ day86/index.md ☐
   - day87/llm_proxy.py ☐ day87/.env.example ☐ day87/extra/extra_env_guard.py ☐ day87/index.md ☐
   - day88/Dockerfile ☐ day88/.dockerignore ☐ day88/extra/extra_Dockerfile.slim ☐ day88/index.md ☐
   - day89/docker-compose.yml ☐ day89/.env.example ☐ day89/extra/extra_compose.env_demo.yml ☐ day89/index.md ☐
   - day90/rag_service.py ☐ day90/Dockerfile ☐ day90/docker-compose.yml ☐ day90/extra/extra_readiness.py ☐ day90/index.md ☐
   - day91/sse_llm_service.py + Dockerfile(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5/卡点/补救(第13周行)。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第14周前 2 天改补欠账。
4. 验收:每个 .py 必须能跑通(main/sse_api/llm_proxy/rag_service 用 uvicorn 启动;llm_proxy/rag_service/day91 需真实 key,离线时确认异常分支已兜底不崩);Dockerfile 能 build、compose 能 up;**确认全周无任何明文 key 入库/进镜像**(.env 已被 .gitignore/.dockerignore 排除)。

## 周尾附录:完整知识点累计清单(截至第13周day91)

第01-04周(已有):Python 基础(类型/控制流/数据结构/推导式/生成器表达式)、函数/模块/闭包/装饰器、OOP/魔术方法/文件读写/异常全体系、venv/pip/requirements.txt/requests/正则 re/类型提示 typing/asyncio(async-await-asyncio.run-sleep)。
第05-09周(已有):大模型 API 调用/环境变量读 key(零硬编码)/Prompt 工程/JSON Mode 结构化输出、流式 Streaming/Function Calling、LangChain/LCEL/RAG 全链路/向量库(Chroma/Milvus/Faiss)/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP(认知)。
第10-12周(已有):TS SSE/流式渲染/打字机效果、Vercel AI SDK(useChat)/LangChain.js/工具调用可视化、Agent 交互模式/React 流式对话组件。

第13周(本周新增):

- FastAPI:应用实例、路由装饰器(get/post)、路径/查询参数、Pydantic 请求/响应模型、依赖注入 Depends、StreamingResponse + 异步生成器实现 SSE 流式接口、WebSocket(认知)、自动 /docs(OpenAPI)、uvicorn 启动
- Docker:镜像 vs 容器、Dockerfile(FROM/WORKDIR/COPY/RUN/EXPOSE/CMD)、构建缓存分层、docker build/run、端口映射、.dockerignore(排除 .env/.venv)
- docker-compose:services、build/image、ports、env_file 环境变量注入、depends_on、up/down 一键编排
- 项目拆分:后端分层(入口 main / 客户端 llm_client / 服务 rag_service),把 RAG/大模型能力服务化并容器化
- 安全:key 从环境变量读、零硬编码、.env 不入库、.dockerignore 排除、compose env_file 注入
- 【超前】识别项(不要求掌握):Kubernetes、CI/CD、Nginx 反向代理、HTTPS/域名/备案(第14周)、多阶段构建、compose healthcheck 就绪探测、gunicorn 多 worker、WebSocket 集群/心跳重连

下周预告(第14周day92-98):云端部署(云服务器/域名/HTTPS/备案)、Linux 基础与部署运维,把本周容器化的全链路搬到公网;**day98 为阶段5 闸门**(作品公网可点开:前端→FastAPI→LLM/RAG 全链路在线可用,含 HTTPS)。注:据 2026 市场修订版,项目1/项目2 需公网可访问且 README 含架构图与成本数据;国内可访问 demo 需备案(第7周已提交,本周确认下号),云服务器约 50-100 元/月。
