# 第09周 · Agent + Tool + Memory + LangGraph 入门 + MCP(认知)

> 与主计划的差异说明:本周严格对应修订版路线图「阶段3后段」(17周映射第09周,day57-63),**day63 为阶段3闸门**(量化标准以骨架第09周/里程碑表为准:个人知识库问答系统对 10 个测试问题 ≥7 个回答合理且引用正确)。据《00_主计划_2026市场修订版》,Agent 工程化被列为**第一优先**(智联《2026人工智能产业人才发展报告》:AI 智能体开发需求同比 +244%),本周主题为 Agent(ReAct)/Tool/Memory/LangGraph 入门/MCP(认知级),与 reference 日程表第09周首教清单完全一致。Day22 已过,第三方库解禁,本周可在 venv 内 pip 安装 langchain/langgraph(须写 requirements.txt)。MCP 本周仅作认知(识别概念/用途/生态,不动手实现协议)。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第09周/dayN/.py;跟练统一命名 extra_*.py 放入 学习产物/第09周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。产物 .py 一律由学习者本人盲写,AI 不代写(讲解代码块仅为教学演示,非产物答案)。

## 本周概览

- 主题:让大模型从"只会说"升级为"会做事"——用 ReAct 循环规划、注册并调用工具、加多轮记忆,并用 LangGraph 把流程编排成状态图;同时建立对 MCP 协议的认知。
- 为什么对拿 offer 有用:Agent 是当前最热门、招聘需求同比 +244% 的方向(智联 2026 报告),是"用模型"而非"造模型"岗位的核心能力;Tool 调用直接复用你第06周已学的 Function Calling,是它的进阶;LangGraph 已成为多智能体/复杂工作流编排的主流框架,是 JD 高频加分项;MCP 是新兴的"模型接工具"标准化协议,能讲清它是什么、解决什么问题就是面试认知加分;本周产物直接支撑差异化项目「Agent 执行可视化面板(规划→调用→观察→结果)」与旗舰项目1「商品知识库导购问答」上线。
- 教材使用策略:主教材/视频 尚硅谷 LangChain 从入门到实战(Agent 章节,A级)+ LangGraph 官方中文文档 + MCP 官方文档;大模型工具调用复习用阿里云百炼/DeepSeek/智谱官方文档(A级);Prompt 与 RAG 综合回顾用 Datawhale。英文文档借翻译工具精读(计入每日英语 0.5h),LangGraph/MCP 部分优先看官方 overview 建立骨架再抠细节。
- 本周结束时应能做到:
  1. 独立搭建最小 ReAct Agent:实现"规划→调用工具→观察→再规划"循环,带最大步数护栏,并打印可读执行轨迹。
  2. 定义多个带 schema 的本地工具并注册,让 Agent 根据问题自主选择工具;为 Agent 加入多轮对话记忆(buffer+窗口上限)。
  3. 用 LangGraph StateGraph 编排一个含节点/边/条件路由的多节点流程并跑通;能说清 MCP 是什么、与 Function Calling 的关系(认知级)。
  4. day63 阶段3闸门:45 分钟内独立盲写一个"≥2 工具 + 对话记忆 + RAG 引用标注"的知识库问答 Agent,对 10 个测试问题 ≥7 个回答合理且引用正确、一次跑通、≤180 行。

## 前置知识点闭包(截至第08周已学,本周可直接用)

基础类型(int/float/str/bool/None)、print/input、f-string、if/elif/else、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、random/datetime、def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器;OOP(class/继承/多态/魔术方法)、文件读写(with/open/模式/encoding)、异常 try/except/else/finally 全体系、isinstance/type、raise、自定义异常;venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio;大模型 SDK 调用、环境变量读 key(零硬编码)、Chat API、Prompt 工程、JSON Mode 结构化输出(json);流式 Streaming、**Function Calling/工具调用**、多轮上下文管理;LangChain/LCEL、文档加载与切分、embedding、向量数据库(Chroma/Milvus/Faiss)、检索器、**RAG 全链路**、Dify/Coze 入门;**引用标注、rerank 重排、RAG 评测方法(命中率/召回)**。

本周新增(首教,与 reference 日程表第09周一致):Agent(ReAct:规划→调用工具→观察→循环,带步数护栏)、Tool(工具定义与注册:名称/用途/参数 schema、注册表、让 Agent 自主选择)、Memory(对话记忆 buffer+窗口上限、实体记忆)、LangGraph 入门(StateGraph 状态图/节点/边/条件路由/compile)、MCP(认知级:协议是什么、解决什么问题、与 Function Calling 的关系、生态)。
【超前】预警:多智能体协作、复杂图编排(子图/并行分支/人工审核中断)、向量长期记忆持久化、MCP 动手实现(真实 server/client SDK 与协议握手)本周均不深入;MCP 仅停留在"能识别概念、能讲清用途"的认知级,若产物需要相关片段一律标【超前】(见 Day60/Day62)。

---

## Day57(周一,7h)· Agent 基础:ReAct 循环(规划→调用→观察→再规划)

今天正式进入 Agent。你在第06周已学 Function Calling——那是"模型说它想调用哪个函数",今天把它升级成一个**自主循环**:模型先思考要干什么、调用工具、看观察结果、再决定下一步,直到能回答。这就是 ReAct(Reasoning + Acting)。产出:一个能多步完成一个问题、并打印完整执行轨迹的最小 ReAct Agent。

💡 JS 开发者速读:ReAct 循环 ≈ 你在事件循环里写的"决策→发起异步调用→拿到结果→再决策"的重试/轮询逻辑,只是"决策"这一步交给模型;Tool ≈ 你注册给模型、由模型决定何时回调的函数(第06周 FC 的进阶);循环护栏(max_steps)≈ 你给轮询设的最大重试次数,防止死循环。

### 学习内容

- Agent 与普通 Chat/Function Calling 的区别(自主多步 vs 单次调用)
- ReAct 循环四步:规划(思考)→行动(调用工具)→观察(读结果)→再规划,直到 done
- 循环护栏:最大步数 max_steps,超限安全兜底(不死循环)
- 执行轨迹(trace)打印:每一步思考/调用/观察可观测
- 环境变量读 key(复习第05周,零硬编码)

### 讲解

结论先行:Agent 的本质是"把 Function Calling 包进一个 while/for 循环",每轮把上一步的观察结果拼回上下文,让模型自己决定下一步是继续调用工具还是给出最终答案;护栏(最大步数)是生产级 Agent 的必备,防止无限循环烧 token。下面的骨架只演示"循环怎么转",具体 think() 的模型决策与工具实现由你自己在产物里盲写。

```python
# ReAct 循环骨架(教学演示):思考→调用工具→观察→再思考,直到能回答
def react_loop(question, tools, max_steps=5):
    obs = ""                              # 上一步的观察结果
    for step in range(max_steps):         # 护栏:最多循环 max_steps 次
        thought = think(question, obs)    # ① 规划:模型决定下一步(占位)
        if thought["done"]:               # 判断是否已可作答
            return thought["answer"]
        name, args = thought["action"]    # ② 选择工具名与参数
        obs = tools[name](**args)         # ③ 调用工具 → 得到观察结果
        print(f"[step{step}] 调用 {name} → 观察: {obs}")
    return "超出最大步数,未得出结论"        # 循环护栏兜底,不崩溃
```

### 教材与章节

- 主教材/视频:尚硅谷 LangChain 从入门到实战(Agent 章节,A级):(https://www.atguigu.com/video/346/)
- 工具调用复习(A级):阿里云百炼 通义千问 Function Calling:(https://help.aliyun.com/zh/model-studio/qwen-function-calling)
- 搜索词:"Agent ReAct 原理"、"ReAct 思考 行动 观察 循环 中文"、"LangChain Agent 入门 教程"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | ReAct 原理/Agent 与 FC 区别/循环护栏 精读+看视频 Agent 章节 |
| 练习 | 2h | 编写 react_agent.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读 LangGraph/Agent 官方英文 overview 一段 |
| 输出 | 1h | 整理"ReAct 循环"博客素材、GitHub commit |
| 复盘 | 0.5h | 补 index.md,自检闭包合规,列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第09周/day57/react_agent.py:最小 ReAct Agent(≤120 行)
  - 实现"规划→调用工具→观察→再规划"的自主循环,处理一个需要多步才能完成的问题(如"先算一个数,再根据结果查询 mock 数据")
  - 至少定义 1 个本地工具(如简单计算或查询一份写死的 mock 字典数据),Agent 能自主决定何时调用它
  - 必须设置循环护栏(最大步数),超出步数时安全兜底返回提示、程序不崩溃、不死循环
  - 完整打印每一步执行轨迹:第几步、模型的思考/决策、调用了哪个工具及参数、观察到了什么、最终答案
  - 模型 key 从环境变量读取,零硬编码
  - 所用知识点清单:Agent(ReAct 循环)、Tool 调用、函数、for/while、if、dict、print、f-string、环境变量读 key、第06周 Function Calling
- [ ] 补记 学习产物/第09周/day57/index.md:覆盖全部学习内容(代码块纯 Python 可运行,禁混 JS 语法)

### JS→Python对照笔记

- JS 轮询/重试循环 while(!done && n++ str:        # 真实实现(此处 mock)
    return f"{city} 晴 26℃"

REGISTRY = {"get_weather": get_weather}   # 名称→函数,供 Agent 按名调用
```

### 教材与章节

- 主教材/视频:尚硅谷 LangChain(Agent/Tool 章节,A级):(https://www.atguigu.com/video/346/)
- 工具/参数 schema(A级):阿里云百炼 Function Calling:(https://help.aliyun.com/zh/model-studio/qwen-function-calling) ;DeepSeek API 文档(function calling/tool 定义):(https://platform.deepseek.com/api-docs/zh-cn/)
- 搜索词:"LangChain Tool 自定义工具 教程"、"大模型 工具 参数 schema 中文"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | Tool schema/注册表/参数校验/description 写法 精读+示例 |
| 练习 | 2.5h | 编写 multi_tool_agent.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读 DeepSeek/百炼 英文 tool 定义片段 |
| 输出 | 1h | GitHub commit、整理"工具注册与路由"笔记 |
| 复盘 | 0.5h | 补 index.md,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第09周/day58/multi_tool_agent.py:多工具 Agent(≤120 行)
  - 定义 ≥3 个本地工具(如计算器、天气 mock 查询、单位换算),每个工具都带一份 schema(名称 + 用途 description + 参数说明 properties/required)
  - 建立工具注册表(名称→函数 的 dict 映射),Agent 通过注册表按名调用工具
  - Agent 能根据用户问题自主选择合适工具,并打印"选择理由"(为什么选这个工具)
  - 演示对 ≥3 个不同问题分别路由到不同工具,逐个打印调用参数与返回结果
  - 处理必填参数缺失/类型错误的情况(结合第03周异常或返回提示),程序不崩溃
  - 模型 key 环境变量读取,零硬编码
  - 所用知识点清单:Tool 定义与 schema、工具注册表(dict)、Agent 自主选择、函数、dict、if/elif、类型提示 typing、异常处理、print、f-string、Function Calling
- [ ] 补记 学习产物/第09周/day58/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS OpenAPI/JSON Schema 描述接口参数 → Python tool 的 parameters schema(properties/required/type)
- JS { event: handler } 路由映射 → Python REGISTRY = {"工具名": 函数}
- JS switch(type) 分发 → Agent 由模型判断选工具(非硬编码 if)
- JS function f(city:string) → Python def get_weather(city: str)(类型提示第04周已学)

### 跟练清单(放extra/)

- extra_tool_schema.py:为一个工具补全参数 schema(含 ≥2 个参数、其中 1 个必填),并写一个校验函数检查调用时必填参数是否齐全、类型是否匹配,缺失时给出提示。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| Tool schema/注册表/自主选择/参数校验 | 尚硅谷-Tool;百炼/DeepSeek-Function Calling | multi_tool_agent.py | Tool schema、注册表 dict、函数、if/elif、typing、异常、print、f-string |

【超前】标注集中区:工具的并行调用、工具嵌套调用(一个工具内部再调另一个 Agent)属【超前】,本周仅做"单轮选一个工具"的顺序调用。
硬约束复查:仅用 day58 闭包知识点 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day59(周三,7h)· Memory:让 Agent 记住多轮上下文

前两天的 Agent 每次提问都"失忆"。今天给它加记忆:把历史对话按序存起来,每轮拼进上下文,让模型能引用之前说过的话。这是多轮对话/客服/Copilot 类应用的地基。产出:带对话记忆(buffer+窗口上限)的 Agent,连续多轮对话时后一轮能引用前一轮信息。

💡 JS 开发者速读:Memory ≈ 前端的状态管理/sessionStorage——把历史消息维护成一个数组,每次请求带上;窗口上限 ≈ 你做的"只保留最近 N 条"的滚动列表,防止状态无限膨胀(对应 token 上限);实体记忆 ≈ 你从表单里抽出的 key-value 存进一个 store,后续直接读,不必每次翻全量历史。

### 学习内容

- 对话记忆 buffer:按序保存 messages(role+content),每轮拼入 prompt
- 记忆窗口上限:只保留最近 N 轮,防止上下文无限增长(控 token 成本)
- 实体记忆(可选):抽取并保存对话中的关键实体(如用户名/偏好)为 key-value
- 记忆如何与 Agent 循环/工具调用协同(每步都能读到历史)
- 用类封装 Memory(复用第03周 OOP)

### 讲解

结论先行:最朴素也最常用的记忆就是"对话缓冲 buffer"——一个按时间顺序存 {role, content} 的列表,每次调模型前把它作为 messages 传进去;但历史不能无限长(会超 token、会烧钱),所以要设窗口上限,只保留最近若干轮。下面演示 buffer 的结构与窗口裁剪思路,具体如何抽取实体、如何拼进 Agent 循环由你在产物里盲写。

```python
## 对话记忆:把历史消息按序存起来,每轮拼进 messages,让模型有上下文
class BufferMemory:
    def __init__(self, max_turns=6):
        self.history = []                 # [{"role":..,"content":..}, ...]
        self.max_turns = max_turns
    def add(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > self.max_turns * 2:   # 一轮=一问一答两条
            self.history = self.history[-self.max_turns * 2:]  # 只留最近若干轮
    def to_messages(self):
        return self.history               # 直接作为 messages 传给模型
```

### 教材与章节

- 主教材/视频:尚硅谷 LangChain(Memory/多轮对话章节,A级):(https://www.atguigu.com/video/346/)
- 多轮上下文复习(A级):智谱 GLM 文档:(https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
- 搜索词:"LangChain Memory 对话记忆 教程"、"ConversationBufferMemory 窗口 中文"、"大模型 多轮上下文 管理"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | buffer/窗口上限/实体记忆/记忆与循环协同 精读+示例 |
| 练习 | 2.5h | 编写 agent_memory.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读 LangChain Memory 英文文档一段 |
| 输出 | 1h | GitHub commit、整理"记忆窗口与 token 成本"笔记 |
| 复盘 | 0.5h | 补 index.md,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第09周/day59/agent_memory.py:带记忆的 Agent(≤120 行)
  - 用类实现对话记忆 buffer:按序保存多轮 messages(role+content),每轮调用模型前把历史拼进上下文
  - 实现记忆窗口上限:只保留最近 N 轮(N 可配),超出后自动裁剪最旧的消息,并打印当前保留的历史条数
  - (加分,可选)实现最小实体记忆:从对话里抽取并保存关键实体(如用户报出的名字/偏好)为 key-value,后续轮次能直接读到
  - 演示连续 ≥3 轮对话,让后一轮明确引用前一轮出现过的信息(体现上下文保持),打印每轮的历史轮次
  - 模型 key 环境变量读取,零硬编码
  - 所用知识点清单:Memory(对话/实体记忆)、类(class/__init__)、list/dict、切片、多轮上下文、for、if、print、f-string
- [ ] 补记 学习产物/第09周/day59/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS sessionStorage/状态数组存历史 → Python self.history 列表存 messages
- JS arr.slice(-n) 只留最近 n 条 → Python self.history[-n:] 窗口裁剪
- JS store 里的 key-value → Python 实体记忆 dict
- JS class Memory{} → Python class BufferMemory:(结构一致,复用第03周 OOP)

### 跟练清单(放extra/)

- extra_entity_memory.py:实现一个最小实体记忆,从几句模拟对话里抽取"实体名→实体值"(如 name→张三、city→杭州)存进 dict,并在后续提问时读出对应实体打印,练习"抽取+存取"。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| buffer/窗口上限/实体记忆/记忆与循环协同 | 尚硅谷-Memory;智谱-多轮上下文 | agent_memory.py | Memory、class、list/dict、切片、多轮上下文、for/if、print |

【超前】标注集中区:向量长期记忆(把历史 embedding 存向量库再检索)、跨会话持久化记忆属【超前】,本周仅做进程内的 buffer+窗口记忆。
硬约束复查:仅用 day59 闭包知识点 ✓ 第三方库合规 ✓ key 零硬编码 ✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day60(周四,7h)· LangGraph 入门:状态图 / 节点 / 边 / 条件路由

前三天的 Agent 是"一个循环里模型自己决定下一步",流程不可控也难可视化。今天换一种范式:用 LangGraph 把流程显式画成一张**状态图**——节点是处理步骤,边是流转,条件边根据状态决定走哪条分支。这是复杂工作流/多智能体编排的主流框架,也是差异化项目「Agent 执行可视化面板」的技术底座。产出:一个含节点/边/条件路由的多节点流程图并跑通。

💡 JS 开发者速读:LangGraph 状态图 ≈ 有限状态机 / 工作流编排,和 XState 的 machine(states + transitions)几乎同构;节点(node)≈ 状态里的一个 state + 它的 entry action;边(edge)≈ transition;条件路由(conditional edge)≈ XState 里根据 guard/条件选择下一个 state;State ≈ 你在整台机器里流转的 context 对象。

### 学习内容

- LangGraph 核心概念:StateGraph、State(状态)、Node(节点=函数)、Edge(边)
- 用 TypedDict 定义在图中流转的状态
- add_node / add_edge / set_entry_point / compile 的编排流程
- 条件路由(conditional edge):根据状态决定走哪条分支
- 打印节点流转顺序,观察状态如何被逐步读写

### 讲解

结论先行:LangGraph 把"流程"显式建模成图——先定义一个 State(在图里流转的数据),每个节点是一个"读状态、返回状态增量"的函数,边规定节点间的先后,条件边让流程能分叉;最后 compile 成可运行对象。相比黑盒循环,它的最大好处是流程可控、可可视化。下面是一个最小可运行的两节点线性图,条件路由与更多节点由你在产物里盲写。

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):            # 在图中流转的状态
    question: str
    docs: str
    answer: str

def retrieve(s: State):            # 节点=函数,读状态、返回状态增量
    return {"docs": f"检索到关于[{s['question']}]的资料"}
def answer(s: State):
    return {"answer": f"根据资料回答:{s['docs']}"}

g = StateGraph(State)
g.add_node("retrieve", retrieve)
g.add_node("answer", answer)
g.set_entry_point("retrieve")
g.add_edge("retrieve", "answer")   # 边=节点间流转
g.add_edge("answer", END)
app = g.compile()                  # 编译成可运行对象
```

### 教材与章节

- 官方文档(主):LangGraph 中文 overview:(https://docs.langchain.org.cn/oss/python/langgraph/overview)
- 视频(A级):尚硅谷 LangChain(LangGraph/编排章节):(https://www.atguigu.com/video/346/)
- 搜索词:"LangGraph 状态图 入门 教程"、"LangGraph StateGraph 节点 边 条件路由"、"LangGraph 条件边 中文"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | StateGraph/State/Node/Edge/条件路由/compile 精读官方 overview+示例 |
| 练习 | 2h | venv 装 langgraph、编写 langgraph_flow.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读 LangGraph 官方英文 quickstart 一段 |
| 输出 | 1h | 写 requirements.txt、GitHub commit、整理"图编排 vs 循环"笔记 |
| 复盘 | 0.5h | 补 index.md,自检闭包合规 |

### 当日产出

- [ ] 编写 学习产物/第09周/day60/langgraph_flow.py:LangGraph 多节点流程(≤120 行)
  - 用 LangGraph StateGraph 编排一个多节点流程(如 检索 → 判断 → 回答)
  - 用 TypedDict 定义在图中流转的状态 State(含 ≥3 个字段)
  - 定义 ≥2 个节点(函数),节点读状态并返回状态增量
  - 定义节点间的边,并至少包含 1 个条件路由(根据状态字段决定走哪条分支,如"资料是否充分"分别走"直接回答"或"再检索/兜底")
  - compile 后运行,打印节点的流转顺序与每一步的状态变化
  - 在 venv 内 pip install langgraph,写 requirements.txt;涉及模型的 key 环境变量读取,零硬编码
  - 所用知识点清单:LangGraph 入门(StateGraph/State/Node/Edge/条件路由/compile)、TypedDict、第三方库 langgraph、函数、if、dict、print、f-string、requirements.txt
- [ ] 补记 学习产物/第09周/day60/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS XState createMachine({states, ...}) → Python StateGraph(State) + add_node/add_edge
- JS state 的 entry action → Python 节点函数(读 state 返回增量)
- JS transition/guard 条件跳转 → Python 条件路由(conditional edge)
- JS machine.context → Python TypedDict 定义的 State
- JS npm install → Python venv 内 pip install + requirements.txt(第04周已学)

### 跟练清单(放extra/)

- extra_linear_graph.py:用 LangGraph 编排一个**不含条件路由**的线性两节点图(如 输入处理 → 输出格式化),compile 后运行并打印流转顺序,先吃透最小图再加条件边。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| StateGraph/State/Node/Edge/条件路由/compile | LangGraph 官方 overview;尚硅谷-编排 | langgraph_flow.py | LangGraph 入门、TypedDict、langgraph 库、函数、if、dict、print、requirements.txt |

【超前】标注集中区:子图(subgraph)、并行分支、多智能体图、人工审核中断(interrupt/human-in-the-loop)属【超前】,本周仅入门"单张图 + 顺序边 + 一个条件路由"。
硬约束复查:仅用 day60 闭包知识点 ✓ 第三方库合规(langgraph 在 venv 内、写 requirements.txt)✓ key 零硬编码 ✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day61(周五,7h)· 综合项目日:带工具 + 记忆的最小 Agent

今天是项目日,把本周四天(ReAct 循环 + 多工具 + 记忆 + 图编排思路)拧成一个能真正多步完成任务的最小 Agent,并接上第07-08周的 RAG 与引用标注——这是 day63 阶段3闸门与旗舰项目1的直接预演,也是差异化项目「Agent 执行可视化面板」的后端内核。产出:mini_agent_project.py,能就一个多步任务自主"规划→调用工具→观察→给出带引用的答案",并打印完整执行轨迹。

💡 JS 开发者速读:整体分层 ≈ 你写过的"service 层(工具)+ store(记忆)+ controller(编排循环)+ 日志(轨迹)"的前端小应用;执行轨迹打印 ≈ 你给关键流程埋的 console/埋点日志,后续可视化面板就是把这份轨迹渲染成时间线;答案带引用 ≈ 你给列表项挂 source 链接,点击可溯源。

### 学习内容(综合复用,无全新理论)

- 分层设计:工具层(≥2 工具)+ 记忆层(多轮)+ 编排层(ReAct 循环)+ 轨迹层(trace 打印)
- 结合第07-08周 RAG:检索资料并让答案带引用标注(可溯源)
- 循环护栏 + 异常兜底(工具报错/检索为空时不崩溃)
- 执行轨迹结构化(便于后续可视化面板消费)
- 用类组织 Agent(复用第03周 OOP)

### 讲解

结论先行:综合项目的关键是"分层解耦"——工具层只管干活、记忆层只管存历史、编排层只管跑 ReAct 循环、轨迹层只管把每步记录下来。答案要带引用(复用第08周引用标注),轨迹要结构化打印(为可视化面板铺路)。下面只演示"分层骨架与轨迹记录长什么样",各层的真实实现与 RAG 引用逻辑由你在产物里盲写。

```python
## 综合 Agent 分层(教学演示):工具层+记忆层+编排层(ReAct)+轨迹打印
class MiniAgent:
    def __init__(self, tools, memory):
        self.tools, self.memory = tools, memory
        self.trace = []                            # 结构化执行轨迹
    def log(self, step, detail):                   # 每步可观测(供可视化面板消费)
        self.trace.append({"step": step, "detail": detail})
        print(f"[轨迹] {step} → {detail}")
    def run(self, task):
        self.memory.add("user", task)
        # 规划→选工具→调用→观察→循环,直到得出"带引用"的答案
        # (工具报错/检索为空需 try/except 兜底,不崩溃)
        return {"answer": "...(含引用来源)", "trace": self.trace}
```

### 教材与章节

- 主教材/视频:尚硅谷 LangChain(Agent + RAG 综合案例,A级):(https://www.atguigu.com/video/346/)
- RAG/图编排复习:LangGraph 官方 overview:(https://docs.langchain.org.cn/oss/python/langgraph/overview) ;Datawhale LLM 入门教程:(https://datawhalechina.github.io/llm-cookbook/)
- 搜索词:"Agent RAG 引用标注 综合 案例"、"LangChain Agent 工具 记忆 项目"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画分层结构、想清工具/记忆/编排/轨迹/RAG 引用如何拼接 |
| 项目实战 | 3h | 编写 mini_agent_project.py |
| 英语 | 0.5h | 借工具精读一段 Agent 综合案例英文说明 |
| 输出 | 1h | GitHub commit、整理"Agent 执行轨迹"博客素材(可视化面板预备) |
| 复盘 | 0.5h | 补 index.md,自检闭包合规,列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第09周/day61/mini_agent_project.py:带工具+记忆的最小 Agent(项目日,≤150 行)
  - 分层实现:工具层(≥2 个工具,如检索工具 + 计算/时间工具)+ 记忆层(多轮 buffer)+ 编排层(ReAct 循环)+ 轨迹层(每步打印)
  - Agent 能就一个需要多步的任务自主"规划→调用工具→观察→再规划",最终给出答案
  - 结合第07-08周 RAG:答案带引用标注(标明信息来源),可溯源
  - 循环护栏(最大步数)+ 异常兜底:工具报错或检索为空时 try/except 处理,程序不崩溃
  - python mini_agent_project.py 一次跑通,完整打印执行轨迹(每步思考/调用/观察)与最终带引用的答案
  - 模型 key 环境变量读取,零硬编码;用到的第三方库写进 requirements.txt
  - 所用知识点清单:Agent(ReAct)、Tool、Memory、RAG 全链路、引用标注、class、函数、异常处理、循环护栏、dict/list、print、f-string、环境变量读 key
- [ ] 补记 学习产物/第09周/day61/index.md:覆盖设计思路(分层)与全部学习内容

### JS→Python对照笔记

- JS service 层 + store + controller 分层 → Python 工具层 + 记忆层 + 编排层
- JS 关键流程埋点日志/console → Python self.trace + log() 打印轨迹
- JS 列表项挂 source 链接可溯源 → Python 答案带引用标注(第08周)
- JS class Agent{} 组织状态与方法 → Python class MiniAgent(复用第03周 OOP)

### 跟练清单(放extra/)

- extra_agent_trace.py:把 mini_agent_project 打印的执行轨迹,额外整理导出成一份结构化、可读的文本(如每步一行"步骤|动作|结果"),为后续「Agent 执行可视化面板」准备数据形态。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| Agent+Tool+Memory+RAG 引用 综合应用 | 尚硅谷-Agent/RAG 综合;LangGraph 官方;Datawhale | mini_agent_project.py | Agent(ReAct)、Tool、Memory、RAG、引用标注、class、异常、循环护栏、print |

【超前】标注集中区:本日无全新超前内容(综合复用已学);若引入人工审核流/多 Agent 协作属【超前】,仅识别不要求实现。
硬约束复查:仅用 day61 闭包知识点 ✓ 第三方库合规(venv+requirements.txt)✓ key 零硬编码 ✓ 项目日 ≤150 行 ✓ extra/ 命名正确 ✓

---

## Day62(周六,7h)· MCP 认知:模型接工具的标准化协议

今天不写重代码,只建立认知:MCP(Model Context Protocol)是什么、解决什么问题、和你已学的 Function Calling/Tool 是什么关系、生态现状如何。它是 JD 高频加分项,面试能讲清"为什么需要 MCP、它标准化了什么"就足够拿分——本周只要求识别概念,不要求动手实现协议。产出:用纯 Python 模拟一次 MCP"工具清单发现"握手的最小认知 demo,并在 index.md 记录认知要点。

💡 JS 开发者速读:MCP ≈ 给"模型接工具"定一套标准化协议,类比 **LSP 之于编辑器**——LSP 出现前每个编辑器要为每种语言各写一套补全/跳转,MCP 出现前每个模型/客户端要各写一套工具对接;有了统一协议,工具提供方写一次 server,任何支持 MCP 的客户端都能发现并调用,和你熟悉的"标准协议解耦两端"是同一个思想。

### 学习内容

- MCP 是什么:Model Context Protocol,标准化"模型/客户端 ↔ 工具/数据源"的连接
- MCP 解决什么问题:工具对接的 M×N 重复劳动 → 统一协议(类比 LSP)
- MCP 与 Function Calling/Tool 的关系:FC 是"模型决定调函数",MCP 是"标准化工具怎么被发现和调用"
- MCP 基本角色:Client / Server / tools(清单发现 tools/list、调用 tools/call)——仅认知
- 生态现状与何时该用(认知级判断,不动手实现)

### 讲解

结论先行:MCP 的核心价值是"标准化"——把工具的声明(有哪些工具、参数是什么)与调用方式统一成一套协议,让任何客户端都能用同样方式发现和调用任何 server 提供的工具,消除重复对接。它不是取代 Function Calling,而是给"工具从哪来、怎么统一接"定标准。下面用纯 Python 模拟一次 tools/list 握手,帮你直观理解"标准化"这件事(不安装、不使用真实 MCP SDK)。

```python
## MCP 认知:用纯 Python 模拟"工具清单发现"握手,理解协议标准化了什么
import json                                 # json 第05周 JSON Mode 已学

def mcp_server_tools_list():                # 服务端:标准化声明自己有哪些工具
    return {"tools": [
        {"name": "read_file",
         "description": "读取指定路径的文件内容",
         "inputSchema": {"type": "object",
                         "properties": {"path": {"type": "string"}},
                         "required": ["path"]}},
    ]}

request = {"jsonrpc": "2.0", "method": "tools/list", "id": 1}   # 客户端请求
response = mcp_server_tools_list()          # 任何 MCP 客户端都按同一格式发现工具
print("请求:", request["method"])
print("返回工具清单:", json.dumps(response, ensure_ascii=False))
```

### 教材与章节

- 官方文档(主):MCP 官方站:(https://modelcontextprotocol.io)
- 工具调用关系复习(A级):阿里云百炼 Function Calling:(https://help.aliyun.com/zh/model-studio/qwen-function-calling) ;智谱 GLM:(https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
- 搜索词:"MCP 协议 是什么"、"Model Context Protocol 介绍 中文"、"MCP 与 Function Calling 区别"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 读 MCP 官方 overview、搞清 Client/Server/tools 角色与"标准化"价值 |
| 练习 | 2.5h | 编写 mcp_concept.py 认知 demo + extra 跟练 + 整理认知记录 |
| 英语 | 0.5h | 借工具精读 MCP 官方英文介绍一段(MCP 文档以英文为主) |
| 输出 | 1h | 在 index.md 写"MCP 认知要点"、GitHub commit |
| 复盘 | 0.5h | 自检:能否脱稿讲清 MCP 是什么/解决什么/与 FC 关系 |

### 当日产出

- [ ] 编写 学习产物/第09周/day62/mcp_concept.py:MCP 认知最小 demo(认知级,≤120 行)
  - 用纯 Python(dict + json,第05周已学)模拟 MCP 的"工具清单发现"握手:客户端发一个 tools/list 请求、服务端按统一格式返回工具清单(名称/描述/inputSchema)
  - 明确注释这是**概念模拟**,不安装、不使用真实 MCP SDK,不实现完整协议(仅识别概念)
  - 打印模拟的客户端请求与服务端返回的工具清单,直观体现"标准化"
  - 在 index.md 记录认知要点:MCP 是什么、解决什么问题、与 Tool/Function Calling 的关系、Client/Server/tools 角色、生态现状与何时用
  - 所用知识点清单:MCP(认知级)、dict、json(第05周 JSON Mode)、print、f-string、注释
- [ ] 补记 学习产物/第09周/day62/index.md:覆盖 MCP 认知要点(能脱稿讲清"是什么/解决什么/与 FC 关系")

### JS→Python对照笔记

- JS 熟悉 LSP 统一编辑器与语言服务 → MCP 统一"模型/客户端 ↔ 工具/数据源"
- JS 标准协议解耦两端(如 OpenAPI) → MCP 让工具写一次 server、多客户端复用
- JS fetch 一个 JSON 清单 → Python 模拟 tools/list 返回 dict/json
- JS JSON.stringify → Python json.dumps(ensure_ascii=False 保中文)

### 跟练清单(放extra/)

- extra_mcp_notes.py:打印一份"MCP vs Function Calling vs 自定义 Tool"的对照表(用 dict/格式化字符串输出三者在"谁决定调用、工具怎么声明、解决什么问题"上的差异),强化认知。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| MCP 概念/角色/与 FC 关系/生态(认知级) | MCP 官方;百炼/智谱-Function Calling | mcp_concept.py + index.md 认知记录 | MCP(认知)、dict、json、print、f-string、注释 |

【超前】标注集中区:MCP 动手实现(安装真实 SDK、写完整 MCP server/client、跑通真实协议握手与传输层)属【超前】,本周仅停留在认知级模拟与概念记录,不要求实现。
硬约束复查:仅用 day62 闭包知识点 ✓ 第三方库合规(认知 demo 用纯标准库,不引入真实 MCP SDK)✓ key 零硬编码(本日不调模型)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day63(周日,7h)· 周检测 / 阶段3闸门 + 对账

今天是本周闸门,也是**阶段3闸门**(里程碑表 day63)。目标是限时独立完成一个综合 Agent,验证本周 ReAct/Tool/Memory 与前序 RAG/引用标注已内化为肌肉记忆。通过后即完成阶段3(RAG 与 Agent 工程化),平稳进入第10周阶段4前端线;同时项目1「商品知识库导购问答」应于本周上线(公网可访问 + README 含架构图与成本数据)。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第09周/day63/kb_agent_check.py:

1. 实现一个最小知识库问答 Agent,包含 **≥2 个工具**(如:一个检索工具从写死的 mock 知识库/本地文档取资料,一个辅助工具如计算或时间查询)。
2. 加入**对话记忆**(多轮 buffer),使连续提问时后一轮能引用前一轮上下文。
3. Agent 能就一个多步任务自主"规划→调用工具→观察→再规划"(ReAct 循环,带最大步数护栏),并最终给出**带引用标注**的答案(标明信息来源,复用第08周引用标注)。
4. 完整打印执行轨迹(每步思考/调用哪个工具/观察到什么)与最终答案。
5. 针对 **10 个测试问题**运行,统计并打印"回答合理且引用正确"的数量。

通过标准(须全部满足,量化口径以骨架第09周/里程碑表为准):

- 45 分钟内完成,python kb_agent_check.py **一次跑通**、无未捕获异常;
- Agent 能**自主多步调用工具**(ReAct 循环真实运转,非硬编码单次调用),且**有记忆**(多轮上下文生效);
- 对 10 个测试问题 **≥7 个回答合理且引用正确**(引用可溯源到检索来源);
- 有循环护栏与基本异常兜底(工具报错/检索为空不崩溃);
- 模型 key 零硬编码(环境变量读取),仅用截至 day63 的闭包知识点,第三方库合规(langchain/langgraph 在 venv 内、写 requirements.txt),**≤180 行**(周末检测放宽)。

未通过补救方案:

- 仅个别错误(如引用格式/记忆窗口写错)→ 当天用缓冲 1h 对照 Day58/Day59 讲解订正,次日重盲写一次(≤45min);
- Agent 循环/工具调用不通(不会自主多步、选错工具)→ 重做 Day57 + Day58;记忆不生效 → 重做 Day59;引用不正确 → 回顾第08周引用标注;
- 严重超时(>90min)或结构混乱 → 本周降级:第10周(阶段4)前 2 天先补 Agent/Tool/Memory 欠账,再进入前端线,**阶段3闸门顺延但不取消**。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day57/react_agent.py ☐ day57/extra/extra_simple_tool.py ☐ day57/index.md ☐
   - day58/multi_tool_agent.py ☐ day58/extra/extra_tool_schema.py ☐ day58/index.md ☐
   - day59/agent_memory.py ☐ day59/extra/extra_entity_memory.py ☐ day59/index.md ☐
   - day60/langgraph_flow.py ☐ day60/extra/extra_linear_graph.py ☐ day60/index.md ☐ day60/requirements.txt ☐
   - day61/mini_agent_project.py ☐ day61/extra/extra_agent_trace.py ☐ day61/index.md ☐
   - day62/mcp_concept.py ☐ day62/extra/extra_mcp_notes.py ☐ day62/index.md(含 MCP 认知记录)☐
   - day63/kb_agent_check.py(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5/卡点/补救,并记录**阶段3闸门达成情况**(10 问 ≥7 合理且引用正确 是否达成)与**项目1上线状态**(公网 URL + README 架构图/成本数据是否齐备)。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第10周前 2 天改补 Agent/Tool/Memory 欠账,闸门顺延不取消。
4. 验收:每个 .py 必须 python xxx.py 跑通;kb_agent_check.py 需实际跑出"≥7/10 合理且引用正确"的统计结果方可判定阶段3闸门通过。

## 周尾附录:完整知识点累计清单(截至第09周day63)

第01-08周(已有):基础类型、print/input、f-string、控制流、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、切片进阶、生成器表达式、random/datetime、def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器;OOP(class/继承/多态/魔术方法)、文件读写(with/open/模式/encoding)、异常 try/except/else/finally 全体系、isinstance/type、raise、自定义异常;venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio;大模型 SDK、环境变量读 key、Chat API、Prompt 工程、JSON Mode(json);流式 Streaming、Function Calling、多轮上下文;LangChain/LCEL、文档加载与切分、embedding、向量数据库、检索器、RAG 全链路、Dify/Coze;引用标注、rerank 重排、RAG 评测方法。

第09周(本周新增):

- Agent:ReAct 循环(规划→调用工具→观察→再规划)、循环护栏(最大步数)、执行轨迹(trace)、Agent 与 Function Calling 的区别
- Tool:工具三要素(name/description/参数 schema)、工具注册表(dict:名称→函数)、Agent 自主选择工具、参数校验、多工具路由
- Memory:对话记忆 buffer(messages 按序存)、记忆窗口上限(裁剪控 token)、实体记忆(key-value)、记忆与循环协同
- LangGraph 入门:StateGraph、State(TypedDict)、Node(节点=函数)、Edge(边)、条件路由(conditional edge)、compile
- MCP(认知级):MCP 是什么、解决什么问题(M×N→统一协议,类比 LSP)、Client/Server/tools 角色、tools/list 发现、与 Function Calling 的关系、生态现状
- 【超前】识别项(不要求掌握):多智能体协作、子图/并行分支/人工审核中断(interrupt)、向量长期记忆持久化、MCP 动手实现(真实 SDK/协议握手)

下周预告(第10周day64-70):进入阶段4前端线——TS SSE、EventSource/fetch 流、流式渲染、打字机效果、流式 Markdown、中断控制(充分发挥你 10 年 JS/TS/React 优势);周末闸门:流式 demo 三要素(打字机 + 流式 Markdown + 中断)可演示。同步启动"前端×LLM 交互层"差异化叙事整理,把本周 Agent 执行轨迹接到前端可视化面板。
