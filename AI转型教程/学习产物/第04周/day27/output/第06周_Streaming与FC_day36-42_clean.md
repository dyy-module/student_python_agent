# 第06周 · 流式 Streaming + Function Calling

> 与主计划的差异说明:本周对应修订版路线图「阶段2后段」(17周映射第06周),主题为流式Streaming、Function Calling,承接第05周国产大模型API(通义千问/DeepSeek/GLM)。**day42 为阶段2闸门**(里程碑口径:限时1h写「AI作文批改器」,含类+类型提示+流式,45分钟内完成);本周在此基线上并入 Function Calling 工具调用与回填,使闸门产物同时覆盖「流式+FC」两大阶段2核心能力,与主计划单一事实源保持一致。骨架固定产物「流式聊天机器人/FC助手/AI客服demo」映射为 stream_chat.py、fc_executor.py 与 multi_tools.py、assistant_cli.py。Day22 已解禁第三方库,本周产物使用 OpenAI 兼容 SDK(如 openai)与 requests,均为合规依赖;**所有 API key 一律从环境变量读取,零硬编码**。
> 变更记录:首版(基于2026市场修订版生成)
> 本周产物约定:固定产物置于 学习产物/第06周/dayN/.py;跟练 extra_*.py 放 学习产物/第06周/dayN/extra/;index.md 同目录;严禁混放。

## 本周概览

- 主题:让大模型应用「边生成边输出」、并能「回头调用你的本地函数」——即流式 Streaming 与 Function Calling 两大阶段2核心能力。
- 为什么对拿offer有用:Streaming 是 AI 应用体验的核心(打字机式逐字输出、首字延迟),第10周前端流式渲染(ReadableStream/SSE)直接复用、第13周 FastAPI SSE 服务化再深化;Function Calling 是 Agent/工具调用的基石,锚定第07周 RAG(把检索封装成工具)、第09周 Agent(Tool 编排/ReAct)、第12周工具调用可视化。两者是 JD 高频「大模型接入/Agent 开发/智能体」的直接考点,也是你「前端×LLM 交互层」差异化叙事的底层原理。
- 教材使用策略:三家官方中文文档(DeepSeek / 阿里云百炼 / 智谱 GLM)的流式与 Function Calling 章节为主(60%)+ Datawhale llm-cookbook 与廖雪峰生成器速查(25%)+ 官方文档英文段与中文搜索词补漏(15%)。全程用 10 年 JS/TS 经验做映射式理解:Streaming≈ReadableStream/SSE/EventSource、逐块 yield≈JS 生成器/for-await、工具 schema≈TS 类型定义、Function Calling≈模型回调你注册的函数。
- 本周结束时应能做到:
  1. 用 `stream=True` 逐块接收并拼接大模型流式响应,读懂 delta、finish_reason 与结束标志。
  2. 用生成器(yield)封装流,实现逐字打印与中途中断,理解「消费方驱动」的惰性求值。
  3. 定义工具 JSON schema,识别 tool_calls,解析 arguments → 本地函数执行 → role=tool 回填 → 二次请求拿到自然语言答复,并可用注册表分派多工具。
  4. day42 阶段2闸门:限时盲写一个「类 + 类型提示 + 流式输出 + 至少一个 Function Calling 工具调用并回填」的综合程序(AI 作文批改器)。

## 前置知识点闭包(截至第05周已学,本周可直接用)

基础类型(int/float/str/bool/None)、print/input、f-string、if/elif/else、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、生成器表达式、random、datetime、def/docstring、参数全体系(含 *args/**kwargs)、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念(周01-02);class/继承/super/多态/魔术方法/isinstance/type、open/with/文件模式、try/except/else/finally/raise/自定义异常(周03);venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio 认知(周04);大模型 SDK(OpenAI 兼容客户端)、环境变量读 key(os.environ,零硬编码)、Chat API(messages 多轮上下文/system-user-assistant 角色)、Prompt 工程、结构化输出 JSON Mode、json.loads/json.dumps(周05)。

本周新增(首教):**流式 Streaming**(stream=True 开启、逐块 chunk 接收、delta.content 提取、拼接完整回复、生成器 yield 封装与消费、打字机式 print(end="", flush=True)、结束标志 finish_reason/[DONE]、中断 break);**Function Calling**(tools 的 JSON schema 定义、function 的 name/description/parameters、tool_calls 识别、json.loads 解析 arguments、role=tool 回填、二次请求、多工具注册表分派、参数校验)。

【超前】预警:多工具**并行调用**(一次返回多个 tool_calls 并行执行)、**tool_choice** 强制指定(required/锁定某函数)、**Agent 循环**(ReAct 规划-调用-观察多轮自动迭代,第09周才教)、**SSE/前端流式渲染**(EventSource/fetch 流,第10周才教)、**async 异步流式**(asyncio + async for,第13周 FastAPI 服务化时深化)——本周仅作认知或【超前】最小片段出现并标注,不作正式教学,产物不得依赖。

---

## Day36(周一,7h)· 流式 Streaming 基础:stream=True 逐块接收与拼接

今天把「一次性等全部结果」升级为「边生成边看」。你在 JS 里熟悉 fetch 的 ReadableStream 与 EventSource,大模型的流式输出是同构心智:服务端把回复切成一块块 chunk 陆续推来,客户端逐块消费、实时打印。今天是流式的地基,只做两件事:开启 stream、逐块拿到并拼接。产出:一个能实时打印大模型回复的流式问答脚本。

💡 JS开发者速读:`stream=True` ≈ 给 fetch 响应体挂上 `getReader()` 逐块读;`for chunk in resp` ≈ `for await (const chunk of stream)`;每块的 `delta.content` ≈ SSE 里一个 data 事件的增量片段;`print(end="", flush=True)` ≈ 前端把增量 append 到 DOM 而不换行。差异:Python SDK 已把 SSE 解析成一个可迭代对象,你直接 for 即可,不用手写 reader。

### 学习内容

- `stream=True` 开启流式(与非流式一次性返回的对比)
- 逐块 chunk 接收:`for chunk in resp`
- 增量提取:`chunk.choices[0].delta.content`(首块/末块可能为空或 None)
- 拼接完整回复(边打印边累加到一个字符串)
- 结束标志认知:finish_reason 与流自然结束

### 讲解

结论先行:流式的本质是「服务端分块推送、客户端逐块消费」。开启 `stream=True` 后,`create()` 不再返回一个完整对象,而返回一个可迭代的流;每个 chunk 携带一小段增量文本(delta),你 `for` 遍历它、把 delta 实时打印,同时累加即可得到完整回复。key 必须从环境变量读,严禁写死。

```python
import os
from openai import OpenAI   # 国产模型多兼容 OpenAI SDK

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],   # 从环境变量读,零硬编码
    base_url="(https://api.deepseek.com",)
)
resp = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "用一句话讲讲什么是流式输出"}],
    stream=True,                       # 关键:开启流式
)
full = ""
for chunk in resp:                     # 逐块到达
    piece = chunk.choices[0].delta.content or ""
    full += piece
    print(piece, end="", flush=True)   # 边收边打印,不换行不缓冲
print("\n---完整回复长度:", len(full))
```

### 教材与章节

- 主教材:DeepSeek API 文档 — 流式输出(stream / SSE):(https://platform.deepseek.com/api-docs/zh-cn/)
- 官方补充:智谱 GLM — HTTP 接口(流式说明):(https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
- 概念补充:Datawhale llm-cookbook — 大模型 API 调用:(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"大模型 流式输出 stream python"、"DeepSeek stream True 逐块"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习 | 3h | stream=True / 逐块 chunk / delta 提取 / 拼接 精读+敲示例 |
| 练习 | 2h | 编写固定产物 stream_chat.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读英文 API 文档 streaming/SSE 段 |
| 输出 | 1h | GitHub 提交当日产物,整理学习笔记为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第06周/day36/stream_chat.py:流式问答脚本(≤120行)
  - 从环境变量读取 API key(如 `os.environ["DEEPSEEK_API_KEY"]`),**严禁在代码里写死 key**;缺失时 print 友好提示并退出
  - 用 OpenAI 兼容客户端指向一家国产大模型(DeepSeek / 通义千问 / 智谱 GLM 任选其一),配好 base_url
  - 向模型提一个开放问题,`stream=True` 逐块接收:每块 delta 实时 `print(end="", flush=True)`,同时累加到完整字符串
  - 流结束后另起一行 print 完整回复的字符数;用 try/except 捕获网络或鉴权异常并 print(不崩溃)
  - 必须覆盖行为:①首字到达即开始打印(体现流式)②空 delta 不报错③异常有兜底
  - 所用知识点清单:os.environ、OpenAI 兼容 SDK、messages、stream=True、for chunk 迭代、delta.content 提取、字符串拼接、len()、print(end/flush)、try/except、f-string、if
- [ ] 补记 学习产物/第06周/day36/index.md:覆盖全部学习内容(代码块纯 Python 可运行)

### JS→Python对照笔记

- JS `fetch(...).body.getReader()` 逐块读 → Python `stream=True` + `for chunk in resp`
- JS `for await (const c of stream)` → Python `for chunk in resp`(SDK 已封装异步)
- JS SSE `event.data` 增量 → Python `chunk.choices[0].delta.content`
- JS `process.stdout.write(x)` 不换行 → Python `print(x, end="", flush=True)`
- JS `process.env.KEY` → Python `os.environ["KEY"]`(都从环境变量读,零硬编码)

### 跟练清单(放extra/)

- extra_stream_count.py:在流式接收基础上,统计并 print 收到的 chunk 总数、非空 chunk 数、完整回复字符数,体会「分块粒度」。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| stream=True / 逐块 chunk / delta 提取 / 拼接 | DeepSeek-流式输出;智谱-HTTP;Datawhale | stream_chat.py | os.environ、SDK、messages、stream、for-chunk、delta、拼接、try/except、print |

【超前】标注集中区:本日无超前内容(async 异步流式、SSE 前端不涉及)。
硬约束复查:仅用 day36 闭包 ✓ 第三方库合规(openai SDK,Day22 后允许)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名 ✓

---

## Day37(周二,7h)· 流式进阶:生成器 yield 逐字打印与中断

今天把「裸 for 循环」升级为「可复用的流式生成器」。生成器是流式消费的最佳载体:它惰性产出一块块文本,消费方用 for 驱动、可随时 break 中断——这正是 JS 生成器 `function*` + `for-await` 的翻版。你还要理解打字机式输出为何天然「逐字」,以及如何在满足条件时优雅打断。产出:一个用生成器封装、支持中途打断的流式打印器。

💡 JS开发者速读:`def gen(): yield x` ≈ `function* gen(){ yield x }`;`for piece in gen()` ≈ `for (const piece of gen())`;中途 `break` 会停止驱动生成器(≈ 提前 return 迭代器);流式本身逐块到达,天然就是打字机效果,不需要 `setTimeout` 人为延迟。差异:Python 生成器被 for 消费时才惰性执行,和 JS 迭代器协议一致。

### 学习内容

- 用生成器函数(`def ... yield`)封装流式响应,产出一块块文本
- 消费方 `for piece in gen()` 惰性驱动,可 `break` 中断
- 打字机式逐字/逐块打印(依赖流本身的分块,无需人为 sleep)
- 中断场景:命中关键词/长度上限即停止
- 生成器与直接 for 循环的差异(可复用、可组合、惰性)

### 讲解

结论先行:把「拿流」这件事包进生成器,消费与生产就解耦了——生成器只管 yield 增量,消费方决定打印到哪、何时 break。惰性求值意味着不 for 就不产出,和 JS 生成器完全同构。中断只需在消费循环里 break,底层流随之停止被拉取。

```python
def stream_text(client, prompt):
    """把流式响应封装成生成器:每来一块就 yield(≈ JS function*)"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in resp:
        piece = chunk.choices[0].delta.content or ""
        if piece:
            yield piece          # 逐块产出,交给消费方决定怎么用

for piece in stream_text(client, "写一首关于秋天的两行小诗"):
    print(piece, end="", flush=True)
    if "。" in piece:            # 演示中断:命中句号就停
        print("\n[已手动中断]")
        break
```

### 教材与章节

- 主教材:廖雪峰 Python — 生成器 / yield:(https://liaoxuefeng.com/books/python/)
- 官方补充:DeepSeek API 文档 — 流式输出:(https://platform.deepseek.com/api-docs/zh-cn/)
- 语法速查:菜鸟教程 Python3 生成器:(https://www.runoob.com/python3/)
- 中文搜索词:"Python 生成器 yield 流式 逐块"、"大模型 stream 生成器 封装"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习 | 3h | 生成器 yield / 惰性消费 / 中断 break / 打字机打印 精读+实验 |
| 练习 | 2h | 编写固定产物 stream_generator.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读英文 generator / streaming 文档段 |
| 输出 | 1h | GitHub 提交当日产物,整理学习笔记为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第06周/day37/stream_generator.py:生成器封装的流式打印器(≤120行)
  - 从环境变量读 key,零硬编码;复用 Day36 的客户端初始化
  - 定义生成器函数(如 `stream_text(prompt)`):内部 `stream=True` 请求,`for chunk` 逐块 `yield` 非空 delta
  - 主流程用 `for piece in stream_text(...)` 消费,打字机式 `print(end="", flush=True)`
  - 支持中断:命中某关键词(如"。"或"停止")或累计字符超过上限即 `break`,并 print 中断原因
  - 必须覆盖行为:①生成器可被完整消费到底②中断后程序正常结束不报错③空 delta 被跳过
  - 所用知识点清单:def、yield 生成器、for 消费、break、if、字符串 in 判断、len()、stream=True、delta 提取、print(end/flush)、os.environ、try/except、f-string
- [ ] 补记 学习产物/第06周/day37/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `function* g(){ yield x }` → Python `def g(): yield x`
- JS `for (const p of g())` → Python `for p in g()`
- JS 迭代器惰性、被 next 才产出 → Python 生成器被 for 才产出
- JS 循环内 `break` 提前结束迭代 → Python `break` 停止拉取底层流
- JS 打字机需 setInterval 逐字 → Python 流式分块天然逐字,无需人为延迟

### 跟练清单(放extra/)

- extra_stream_join.py:用生成器产出增量,消费方把它们累加成完整文本并统计块数,最后一次性 print 全文与统计,对比「实时打印」与「先攒后打」两种消费方式。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 生成器 yield / 惰性消费 / 中断 / 打字机打印 | 廖雪峰-生成器;DeepSeek-流式;菜鸟 | stream_generator.py | def、yield、for、break、if、len、stream、delta、print、os.environ、try/except |

【超前】标注集中区:`async for` 异步流式消费属【超前】(第13周深化),本日仅用同步生成器,不要求 async。
硬约束复查:仅用 day37 闭包 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名 ✓

---

## Day38(周三,7h)· Function Calling 入门:工具 schema 定义与 tool_calls 识别

今天让模型「学会喊你的函数」。Function Calling 不是模型自己执行代码,而是:你用 JSON schema 声明有哪些工具、模型判断该不该用、用哪个、传什么参数,然后把「我想调用 X 函数,参数是 Y」返回给你。这是 Agent、RAG 工具化、第09周编排的最底层机制。今天只做「声明 + 识别」,不执行。产出:一个能声明工具、并识别模型是否想调用它的脚本。

💡 JS开发者速读:工具的 `parameters`(JSON Schema)≈ 你写 TS 的 `interface`/类型定义,告诉模型入参长什么样;`description` ≈ JSDoc,模型靠它决定何时调用;`tool_calls` ≈ 模型给你一个「请回调这个已注册函数」的事件对象,`function.name`/`arguments` ≈ 事件里的方法名与 payload。整体像事件驱动:你注册工具,模型派发调用意图。

### 学习内容

- tools 参数结构:`{"type":"function","function":{name, description, parameters}}`
- parameters 的 JSON Schema(type/properties/required)——≈ TS 类型定义
- description 写清楚,模型据此判断何时调用
- 请求带上 tools,读回 `resp.choices[0].message.tool_calls`
- tool_calls 为 None(直接答复)vs 非空(要求调用工具)的分支识别

### 讲解

结论先行:Function Calling 的第一步是「用 JSON schema 把工具描述给模型」。模型不会执行,它只在需要时返回一个 tool_calls,里面写着想调用的函数名和参数(JSON 字符串)。今天的目标就是:声明工具 → 发请求 → 判断 tool_calls 是否存在 → 打印模型的调用意图。key 仍从环境变量读。

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气",  # 描述清晰,模型据此决定何时调用
            "parameters": {                        # ≈ TS 接口的类型定义
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名,如 杭州"}
                },
                "required": ["city"],
            },
        },
    }
]
resp = client.chat.completions.create(
    model="deepseek-chat", messages=msgs, tools=tools
)
tool_calls = resp.choices[0].message.tool_calls   # None 表示模型直接答复、不调用工具
```

### 教材与章节

- 主教材:阿里云百炼 通义千问 — Function Calling:(https://help.aliyun.com/zh/model-studio/qwen-function-calling)
- 官方补充:DeepSeek API 文档 — Function Calling / tools:(https://platform.deepseek.com/api-docs/zh-cn/)
- 概念补充:Datawhale llm-cookbook:(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"Function Calling 工具调用 教程"、"大模型 tools schema 定义 python"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习 | 3h | tools schema 结构 / JSON Schema / tool_calls 识别 精读+敲示例 |
| 练习 | 2h | 编写固定产物 fc_schema.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读英文 Function Calling / tools schema 文档 |
| 输出 | 1h | GitHub 提交当日产物,整理学习笔记为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第06周/day38/fc_schema.py:工具声明与调用意图识别(≤120行)
  - 从环境变量读 key,零硬编码
  - 定义 1 个工具的 JSON schema(如 get_weather,含 name/description/parameters,parameters 内含 required)
  - 构造一条明显需要工具的用户消息(如"杭州今天天气怎么样")与一条不需要工具的消息(如"你好"),分别带 tools 发请求
  - 读取 `message.tool_calls`:非空时 print 出模型想调用的 function.name 与 arguments(原始 JSON 字符串);为 None 时 print 模型的直接文本答复
  - 必须覆盖行为:①两种消息都测到②能区分「要调工具」与「直接答」③arguments 原样打印(本日不解析、不执行)
  - 所用知识点清单:os.environ、SDK、messages、tools 的 dict/JSON schema、message.tool_calls 识别、if 分支、print、f-string、dict 取值
- [ ] 补记 学习产物/第06周/day38/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS/TS `interface Args { city: string }` → Python 工具的 `parameters`(JSON Schema)
- JS JSDoc `@description` → Python 工具 `description`(模型据此选工具)
- JS 事件对象 `{ type, payload }` → Python `tool_calls[0]`(含 id/function.name/arguments)
- JS `obj?.field` 可选链 → Python `if msg.tool_calls:` 先判空再取
- JS `JSON.parse(str)` → Python `json.loads(str)`(明天执行时用)

### 跟练清单(放extra/)

- extra_tool_def.py:再定义 2 个工具 schema(如 get_time、calculate),组成 tools 列表并逐个 print 其结构,体会 schema 的写法规范。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| tools schema / JSON Schema / tool_calls 识别 | 阿里云百炼-FC;DeepSeek-tools;Datawhale | fc_schema.py | os.environ、SDK、messages、tools dict、tool_calls 识别、if、print、dict 取值 |

【超前】标注集中区:`tool_choice`(强制/锁定调用某工具)属【超前】,本日仅识别 tool_calls,不要求指定调用策略。
硬约束复查:仅用 day38 闭包 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名 ✓

---

## Day39(周四,7h)· Function Calling 执行:解析 tool_calls → 本地执行 → 回填 → 二次请求

今天闭合 Function Calling 的完整回路。昨天模型只是「喊」出调用意图,今天你要真正接住它:解析 arguments、路由到本地函数执行、把结果以 `role="tool"` 回填进 messages、再发一次请求让模型用自然语言总结。这套「解析-执行-回填-再问」的四步,就是第09周 Agent 循环的最小内核。产出:一个跑通单工具调用闭环的脚本。

💡 JS开发者速读:整条链路 ≈ 一次「事件回调 + 二次渲染」:模型派发调用意图(事件)→ 你执行 handler(本地函数)→ 把返回值回填(setState)→ 再触发一次渲染(二次请求得到最终答复)。`json.loads(arguments)` ≈ `JSON.parse(event.payload)`;`role="tool"` 消息 ≈ 把异步结果塞回状态树供下一轮读取。

### 学习内容

- 解析 `tool_calls[0].function.arguments`(JSON 字符串 → `json.loads` 成 dict)
- 路由到本地真实函数执行(用 `**kwargs` 解包参数)
- 把 assistant 的 tool_calls 消息与执行结果以 `role="tool"` 回填 messages(带 tool_call_id)
- 二次请求:让模型基于工具结果生成自然语言答复(可流式)
- 完整四步闭环:声明 → 识别 → 执行回填 → 再问

### 讲解

结论先行:执行工具的关键是「参数解析 + 结果回填」。arguments 是 JSON 字符串,`json.loads` 后用 `**` 解包传给本地函数;函数返回值必须以 `role="tool"` 且带对应 `tool_call_id` 追加进 messages,模型才能在二次请求里读到它、组织成人类可读的答复。缺一步模型都会「失忆」。

```python
import json

def get_weather(city: str) -> str:      # 本地真实函数(这里用假数据演示)
    return json.dumps({"city": city, "temp": "26℃", "desc": "晴"})

msg = resp.choices[0].message
if msg.tool_calls:                       # 模型要求调用工具
    messages.append(msg)                 # 先把 assistant 的 tool_calls 消息入列
    call = msg.tool_calls[0]
    args = json.loads(call.function.arguments)   # 参数是 JSON 字符串,需解析
    result = get_weather(**args)         # 解包参数,路由到本地函数
    messages.append({                    # 结果以 role="tool" 回填
        "role": "tool",
        "tool_call_id": call.id,
        "content": result,
    })
    final = client.chat.completions.create(   # 二次请求 → 自然语言答复
        model="deepseek-chat", messages=messages
    )
```

### 教材与章节

- 主教材:阿里云百炼 通义千问 — Function Calling(执行与回填):(https://help.aliyun.com/zh/model-studio/qwen-function-calling)
- 官方补充:智谱 GLM — 工具调用 / HTTP 接口:(https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
- 官方补充:DeepSeek API 文档 — Function Calling:(https://platform.deepseek.com/api-docs/zh-cn/)
- 中文搜索词:"Function Calling tool_calls 回填 role tool python"、"大模型 工具调用 二次请求"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习 | 3h | 解析 arguments / 本地执行 / role=tool 回填 / 二次请求 精读+实验 |
| 练习 | 2h | 编写固定产物 fc_executor.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读英文 tool_calls / tool message 文档 |
| 输出 | 1h | GitHub 提交当日产物,整理学习笔记为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第06周/day39/fc_executor.py:单工具调用完整闭环(≤120行)
  - 从环境变量读 key,零硬编码
  - 定义 1 个工具的 schema(get_weather)与对应本地函数(可用固定/随机的假天气数据,类型提示标注参数与返回)
  - 发一次带 tools 的请求 → 若返回 tool_calls:`json.loads` 解析 arguments → `**` 解包调用本地函数 → 把 assistant 消息与 `role="tool"`(带 tool_call_id)结果回填 messages
  - 二次请求让模型基于工具结果给出自然语言答复,并可流式打印最终答复(复用 Day37 生成器)
  - 必须覆盖行为:①解析 arguments 不报错②回填消息含正确 tool_call_id③二次请求拿到含工具结果的答复④用 try/except 兜住解析或网络异常
  - 所用知识点清单:os.environ、SDK、messages 多轮、tools schema、tool_calls、json.loads、`**` 解包、本地函数(类型提示)、role=tool 回填、二次请求、stream 生成器、try/except、if、print
- [ ] 补记 学习产物/第06周/day39/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `JSON.parse(call.arguments)` → Python `json.loads(call.function.arguments)`
- JS `handler(...args)` / `fn({...obj})` → Python `func(**args)`(字典解包成关键字参数)
- JS 把异步结果 setState 回状态 → Python 把结果 append 成 `role="tool"` 消息回填 messages
- JS 回调后再触发一次渲染 → Python 回填后发二次请求拿最终答复
- JS `id` 关联请求与响应 → Python `tool_call_id` 关联调用与结果

### 跟练清单(放extra/)

- extra_calc_tool.py:新增一个本地计算器工具(加减乘除,schema 含 operation/a/b),让模型触发它并完成解析-执行-回填-二次请求的完整闭环。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 解析 arguments / 本地执行 / role=tool 回填 / 二次请求 | 阿里云百炼-FC;智谱-工具调用;DeepSeek | fc_executor.py | json.loads、`**` 解包、messages、tool_calls、role=tool、二次请求、stream、try/except、类型提示 |

【超前】标注集中区:多个 tool_calls **并行执行**、Agent **多轮自动循环**属【超前】(第09周),本日止于「单工具一次闭环」,不自动迭代。
硬约束复查:仅用 day39 闭包 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名 ✓

---

## Day40(周五,7h)· 多工具与参数校验:让模型自己选对工具

今天从「单工具」升级到「多工具」。真实应用往往同时提供查天气、算数、查时间等多个函数,模型要根据用户意图自主选对那个、并给出参数。你要学会用「工具注册表(name → 函数)」做统一分派,并对模型传来的参数做校验(缺参、类型错、未知工具),这是生产级健壮性的必备。产出:一个多工具分派器。

💡 JS开发者速读:工具注册表 ≈ 一张 `{ eventName: handler }` 的路由表(像 Redux 的 reducer map 或 Express 的路由表);按 `function.name` 分派 ≈ `handlers[name](payload)`;参数校验 ≈ 你在 handler 入口用 TS 类型或 zod 校验入参。差异:调用意图由模型给出,你仍要在本地兜底校验,别信模型一定给对参数。

### 学习内容

- 定义 2-3 个工具 schema,组成 tools 列表一并发给模型
- 模型自主选择:tool_calls 里的 function.name 决定用哪个
- 工具注册表(dict:name → 本地函数)统一分派,替代冗长 if/elif
- 参数校验:未知工具、缺必填参数、类型不符时的兜底处理
- 多轮消息管理:把工具结果回填后继续对话

### 讲解

结论先行:多工具的核心是「分派 + 校验」。用一张 dict 把工具名映射到本地函数,拿到 function.name 就 `REGISTRY.get(name)` 取函数、`**args` 调用,避免一长串 if/elif。模型给的参数不可全信,调用前要校验必填项与类型,未知工具或非法参数要返回可读的错误串回填给模型,而不是让程序崩溃。

```python
def get_weather(city: str) -> str:
    return f"{city}:晴,26℃"

def add(a: float, b: float) -> float:
    return a + b

REGISTRY = {"get_weather": get_weather, "add": add}   # 工具注册表:name→函数

def dispatch(name: str, arguments: str) -> str:
    func = REGISTRY.get(name)                # 按模型给的函数名分派
    if func is None:
        return f"错误:未知工具 {name}"        # 兜底,不崩溃
    try:
        kwargs = json.loads(arguments)
        return str(func(**kwargs))           # 解包参数并调用
    except (ValueError, TypeError) as e:
        return f"错误:参数非法 {e}"
```

### 教材与章节

- 主教材:阿里云百炼 通义千问 — Function Calling(多工具):(https://help.aliyun.com/zh/model-studio/qwen-function-calling)
- 概念补充:Datawhale llm-cookbook:(https://datawhalechina.github.io/llm-cookbook/)
- 官方补充:DeepSeek API 文档 — tools:(https://platform.deepseek.com/api-docs/zh-cn/)
- 中文搜索词:"大模型 多工具 Function Calling 注册表 分派"、"tool_calls 参数校验 python"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习 | 3h | 多工具 schema / 注册表分派 / 参数校验 精读+实验 |
| 练习 | 2h | 编写固定产物 multi_tools.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读英文 multiple tools / dispatch 文档 |
| 输出 | 1h | GitHub 提交当日产物,整理学习笔记为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 JS→Python 对照,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第06周/day40/multi_tools.py:多工具分派器(≤120行)
  - 从环境变量读 key,零硬编码
  - 定义 2-3 个本地工具函数(如 get_weather、add、get_today 用 datetime)与对应 schema,组成 tools 列表
  - 用 dict 构建工具注册表(name → 函数);写一个 dispatch(name, arguments) 做统一分派
  - 参数校验:未知工具返回错误串、缺必填/类型不符用 try/except 兜住并返回可读错误(不崩溃)
  - 用几条不同意图的用户消息(问天气/算数/问日期)分别请求,让模型自主选择工具,执行并把结果回填、二次请求打印最终答复
  - 必须覆盖行为:①模型对不同问题选对不同工具②非法参数不崩溃③错误信息回填给模型
  - 所用知识点清单:os.environ、SDK、messages、多 tools schema、tool_calls、dict 注册表、dict.get、`**` 解包、json.loads、try/except(ValueError/TypeError)、datetime、if、print、类型提示
- [ ] 补记 学习产物/第06周/day40/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `{ evt: handler }` 路由表 → Python `REGISTRY = {name: func}`
- JS `handlers[name]?.(payload)` → Python `REGISTRY.get(name)` 后判空调用
- JS zod/TS 校验入参 → Python try/except + 必填项判断
- JS 抛错要 try/catch → Python except (ValueError, TypeError) 兜底
- JS 返回错误信息给上游 → Python 把错误串回填成 tool 消息给模型

### 跟练清单(放extra/)

- extra_tool_registry.py:把 3 个工具用注册表模式统一管理,遍历打印「工具名 → 描述」清单,并模拟一次错误工具名的分派,验证兜底不崩溃。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 多工具 schema / 注册表分派 / 参数校验 | 阿里云百炼-FC 多工具;Datawhale;DeepSeek | multi_tools.py | dict 注册表、dict.get、`**` 解包、json.loads、try/except、datetime、tool_calls、messages、类型提示 |

【超前】标注集中区:一次返回**多个 tool_calls 并行执行**、`tool_choice` 强制指定工具属【超前】,本日仅演示模型单选/顺序处理,不要求并行与强制策略。
硬约束复查:仅用 day40 闭包 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名 ✓

---

## Day41(周六,7h)· 综合项目日:带工具调用的流式命令行助手

今天是项目日,把本周的流式 + Function Calling + 多轮上下文拧成一个可持续对话的命令行助手——它就是骨架里的「AI 客服 demo / 流式 FC 助手」,也是第09周 Agent、第13周 FastAPI 服务化的能力预演。助手要能:记住多轮对话、判断是否需要调用本地工具、执行并回填、最后流式打印答复。产出:assistant_cli.py,一个 while 循环驱动、能查天气/算数并流式回答的助手。

💡 JS开发者速读:整体结构 ≈ 你写过的一个 CLI 版「聊天组件 + 本地工具中间件」:messages 数组 ≈ React 的会话 state,while+input ≈ 事件循环,工具分派 ≈ 中间件拦截,流式打印 ≈ 逐块 append 到界面。差异在于状态维护在一个 messages 列表里手动 append,没有框架帮你管。

### 学习内容(综合复用,无全新理论)

- 用 messages 列表维护多轮上下文(system + 历史 user/assistant/tool)
- while + input 命令行主循环(复用 break 退出)
- 每轮:带 tools 请求 → 若 tool_calls 则执行本地工具并回填 → 流式打印最终答复
- 分层:工具层(注册表 + 本地函数)/ 调度层(dispatch)/ 交互层(循环 + 流式打印)
- 健壮性:异常兜底、空输入处理、退出指令

### 讲解

结论先行:综合助手的关键是「一轮对话的完整状态机」——把用户输入 append 进 messages,带 tools 请求;若模型要调工具就执行回填再请求一次;最后把答复流式打印,并把 assistant 答复也 append 回 messages 供下一轮使用。下面是**结构骨架示意(非产物答案)**,其中工具 schema、dispatch、流式打印函数都由你本人实现。

```python
messages = [{"role": "system", "content": "你是带工具的助手"}]
while True:
    user = input("你> ")
    if user == "exit":
        break
    messages.append({"role": "user", "content": user})
    resp = client.chat.completions.create(
        model="deepseek-chat", messages=messages, tools=tools
    )
    msg = resp.choices[0].message
    if msg.tool_calls:
        run_tools(messages, msg)          # 执行并回填(见 Day39/Day40,你来实现)
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=messages, tools=tools, stream=True
        )
    print_stream(resp)                    # 流式打印最终答复(见 Day37,你来实现)
```

### 教材与章节

- 主教材:阿里云百炼 通义千问 — Function Calling(综合):(https://help.aliyun.com/zh/model-studio/qwen-function-calling)
- 官方补充:DeepSeek API 文档 — 流式 + tools:(https://platform.deepseek.com/api-docs/zh-cn/)
- 综合回顾:廖雪峰 Python — 生成器 / 类 / 异常:(https://liaoxuefeng.com/books/python/)
- 中文搜索词:"流式 Function Calling 命令行助手 python"、"大模型 多轮对话 messages 工具调用"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 学习/设计 | 2.5h | 画分层结构、想清一轮对话的状态流转与异常场景 |
| 项目实战 | 3h | 编写 assistant_cli.py |
| 英语 | 0.5h | AI 辅助精读英文 multi-turn + tools 文档 |
| 复盘 | 1h | 补 index.md,自检闭包合规,列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第06周/day41/assistant_cli.py:带工具调用的流式命令行助手(项目日,≤150行)
  - 从环境变量读 key,零硬编码;可用类封装(如 Assistant 类,含 messages 与 tools,类型提示标注)
  - 定义至少 2 个本地工具(如查天气、算数)及其 schema,用注册表分派并做参数校验
  - while + input 命令行主循环:支持多轮对话(维护 messages 历史)、输入 exit 退出、空输入不崩溃
  - 每轮:带 tools 请求 → 若 tool_calls 则执行本地工具并以 role=tool 回填 → 二次请求以 stream=True **流式打印**最终答复 → 把 assistant 答复 append 回 messages
  - 用 try/except 兜住网络/解析/鉴权异常,程序不崩溃;每步有清晰 print 提示(如"[调用工具] get_weather")
  - 必须覆盖行为:①多轮上下文被记住②至少一次工具被正确触发并回填③最终答复逐块流式可见④异常兜底
  - 所用知识点清单:class、类型提示、os.environ、SDK、messages 多轮、tools schema、tool_calls、dict 注册表、`**` 解包、json.loads、role=tool 回填、二次请求、stream 生成器、while/input/break、try/except、if、print、f-string
- [ ] 补记 学习产物/第06周/day41/index.md:覆盖设计思路与全部学习内容

### JS→Python对照笔记

- JS 会话 state 数组 → Python messages 列表(手动 append 维护多轮)
- JS readline/事件循环 → Python while + input()
- JS 中间件拦截处理 → Python 工具注册表 dispatch
- JS 逐块 append 到界面 → Python 生成器 for + print(end="", flush=True)
- JS class + 类型注解 → Python class + typing 类型提示

### 跟练清单(放extra/)

- extra_assistant_log.py:给助手加日志能力——每轮把用户输入、触发的工具、模型答复追加写入一个 txt 文件(复用周03 open/with),退出时打印日志行数。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 流式 + Function Calling + 多轮上下文综合 | 阿里云百炼-FC;DeepSeek-流式/tools;廖雪峰 | assistant_cli.py | class、类型提示、messages 多轮、tools、tool_calls、注册表分派、role=tool 回填、stream 生成器、while/input、try/except |

【超前】标注集中区:Agent 自动多轮循环(ReAct)、SSE 前端渲染属【超前】(第09/10周),本日为手动单层「一轮一工具」,不自动迭代规划。
硬约束复查:仅用 day41 闭包 ✓ 第三方库合规 ✓ key 零硬编码 ✓ 项目日 ≤150行 ✓ extra 命名 ✓

---

## Day42(周日,7h)· 周检测 / 阶段2闸门 + 对账

今天是本周闸门,也是**阶段2闸门**(里程碑:限时写「AI 作文批改器」,含类+类型提示+流式,45分钟内完成)。目标是限时独立盲写一个综合程序,把「流式输出 + Function Calling 工具调用与回填 + 类封装 + 类型提示」拧成一体,验证阶段2能力已内化为肌肉记忆。通过后即可平稳进入第07周(LangChain / RAG 全链路)。

### 周检测(限时任务)

任务:45分钟内(阶段2闸门允许最多1h),**不看教材、不看本周产物**,独立盲写 学习产物/第06周/day42/essay_grader.py:

1. 用**类**封装一个作文批改器(如 `EssayGrader`),`__init__` 里从**环境变量**读取 API key(零硬编码)并初始化 OpenAI 兼容客户端,方法用**类型提示**标注参数与返回。
2. 定义至少 1 个本地工具及其 JSON schema(如 `count_words` 统计作文字数 / `check_sensitive` 敏感词检查),工具对应一个本地函数(可用固定或简单计算逻辑)。
3. 提交一篇(可硬编码在程序内的)学生作文,先带 tools 请求模型;若模型返回 tool_calls:`json.loads` 解析 arguments → 调用本地工具 → 以 `role="tool"`(带 tool_call_id)回填 messages。
4. 二次请求,以 `stream=True` **流式**逐块打印模型给出的批改意见(打字机式 print),体现流式输出。
5. 全程用 try/except 兜住鉴权/网络/解析异常,程序不崩溃;每步有清晰 print。

通过标准(须全部满足):

- 45分钟内完成(阶段2闸门最长不超过1h),`python essay_grader.py` 一次跑通、无未捕获异常;
- 用 class 封装,且关键方法有 typing 类型提示;
- 流式输出可见:批改意见逐块打印,而非一次性返回;
- 至少一个 Function Calling 工具被正确触发、本地执行并 role=tool 回填,二次请求得到含工具结果的答复;
- API key 从环境变量读取,零硬编码;
- 仅用截至 day42 的闭包知识点,≤180行(周末检测放宽)。

未通过补救方案:

- 仅个别语法/schema 字段写错 → 当天用缓冲1h对照 Day38/Day39 讲解订正,次日重盲写一次(≤45min);
- 流式逻辑不通(拿不到 delta / 不换行打印) → 重做 Day36+Day37 的 stream 与生成器;
- Function Calling 逻辑不通(tool_calls 识别 / 回填 / 二次请求) → 重做 Day38+Day39 的声明-执行-回填闭环,再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第07周前2天先补 Streaming/FC 欠账,再进入 LangChain/RAG,闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day36/stream_chat.py ☐ day36/extra/extra_stream_count.py ☐ day36/index.md ☐
   - day37/stream_generator.py ☐ day37/extra/extra_stream_join.py ☐ day37/index.md ☐
   - day38/fc_schema.py ☐ day38/extra/extra_tool_def.py ☐ day38/index.md ☐
   - day39/fc_executor.py ☐ day39/extra/extra_calc_tool.py ☐ day39/index.md ☐
   - day40/multi_tools.py ☐ day40/extra/extra_tool_registry.py ☐ day40/index.md ☐
   - day41/assistant_cli.py ☐ day41/extra/extra_assistant_log.py ☐ day41/index.md ☐
   - day42/essay_grader.py(阶段2闸门检测产物)☐
2. 填 README 进度跟踪表:完成% / 自评1-5 / 卡点 / 补救,并**记录阶段2闸门达成情况**(是否45min内完成、流式与 FC 是否均通过)。
3. 缺产物处理:缺1-2项用缓冲日补;缺≥3项 → 第07周前2天改补 Streaming/FC 欠账,再进 LangChain/RAG。
4. 验收:每个 .py 必须 `python xxx.py` 跑通;确认 essay_grader.py 的流式逐块可见、工具被触发回填、key 零硬编码,并回归一次阶段2闸门通过标准。

## 周尾附录:完整知识点累计清单(截至第06周day42)

第01-05周(已有):基础类型、print/input、f-string、控制流、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、生成器表达式、random、datetime、def/docstring、参数全体系(*args/**kwargs)、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念;class/继承/super/多态/魔术方法/isinstance/type、open/with/文件模式/encoding、try/except/else/finally/raise/自定义异常;venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio 认知;大模型 SDK(OpenAI 兼容客户端)、环境变量读 key(零硬编码)、Chat API(messages 多轮/角色)、Prompt 工程、结构化输出 JSON Mode、json.loads/json.dumps。

第06周(本周新增):

- 流式 Streaming:stream=True、逐块 chunk 接收、delta.content 提取、拼接完整回复、生成器 yield 封装与 for 消费、打字机式 print(end="", flush=True)、结束标志 finish_reason/[DONE] 认知、中断 break。
- Function Calling:tools 的 JSON schema(name/description/parameters/required)、tool_calls 识别、json.loads 解析 arguments、`**` 解包路由到本地函数、role=tool 回填(带 tool_call_id)、二次请求、工具注册表(dict name→函数)分派、参数校验(未知工具/缺参/类型错兜底)、多轮 messages 上下文管理。
- 【超前】识别项(不要求掌握):多工具并行调用、tool_choice 强制指定、Agent 自动循环(ReAct,第09周)、SSE/前端流式渲染(第10周)、async 异步流式(async for,第13周)。

下周预告(第07周day43-49):LangChain / LCEL、文档加载与切分、embedding、向量数据库(Chroma/Milvus/Faiss)、检索器与 RAG 全链路、Dify/Coze 低代码入门 → 命令行跑通 RAG 检索链路,并**本周即提交国内可访问 demo 的备案(周期2-4周)**。本周的 Function Calling 会直接复用为 RAG 的「检索工具」,流式输出则用于问答结果的实时呈现。
