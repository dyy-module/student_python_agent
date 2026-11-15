# 第11周 · Vercel AI SDK + LangChain.js + 工具调用可视化

> 与主计划的差异说明:本周对应修订版路线图「阶段4中段」(17周映射第11周,day71-77)。在第10周手写 SSE/流式渲染的基础上,改用成熟 SDK(Vercel AI SDK / LangChain.js)大幅简化流式对话前端工程,并做出工具调用可视化,直接支撑差异化项目「Agent 执行可视化面板」。据主计划:Vercel AI SDK / LangChain.js 的「前端护城河」定位属**自选加分项、暂无权威 JD 佐证**,主叙事仍是「懂业务能交付」(10年前端 + 即时零售商品/营销域 + AI 应用落地),不夸大为求职硬通货。阶段4无可信中文视频直出,教材一律用官方文档 + 中文搜索词,严禁编造 BV 号。前端不硬编码 key,一律经服务端 route handler / 代理(第13周 FastAPI 或 Next API route)注入。产物为 .tsx/.ts,由学习者盲写,AI 不代写。闸门为 day77 周检测(组件接入真实后端流式可用),阶段4闸门在 day84。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第11周/dayN/<文件名>.tsx|.ts;跟练统一命名 extra_*.tsx / extra_*.ts 放入 学习产物/第11周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。

## 本周概览

- 主题:用 Vercel AI SDK / LangChain.js 把流式对话前端工程化,并把工具调用过程可视化。
- 为什么对拿offer有用:AI SDK 大幅简化流式对话前端——把你第10周手写的 fetch 流/SSE/打字机封装成 useChat/streamText,省下大量样板;工具调用可视化直接支撑差异化项目「Agent 执行可视化面板」,是「前端×LLM 交互层」叙事的核心实证。**如实标注**:据主计划,Vercel AI SDK / LangChain.js 属自选加分项、暂无权威 JD 佐证,主叙事仍是「懂业务能交付」,本周成果用于强化差异化,而非当作求职硬门槛。
- 教材使用策略:阶段4无可信中文视频直出,一律官方文档 + 中文搜索词——Vercel AI SDK 官方文档(主)+ LangChain.js 官方文档 + Chrome 中文实操(A级);严禁编造 BV 号或视频链接。
- 本周结束时应能做到:
  1. 用 useChat 搭出接入真实后端、流式逐字返回的对话组件(key 在服务端,前端零硬编码)。
  2. 用 streamText 消费服务端流式增量并绑定到 UI、支持中断;用 LangChain.js 组织一条前端侧链式调用。
  3. 做出工具调用可视化(工具名/入参/状态/结果 渲染为卡片/时间线),并整合进消息组件与会话状态管理。
  4. day77 闸门:45 分钟内独立盲写「接入真实后端的流式对话组件 + 至少一次工具调用可视化」,TS 类型完整。

## 前置知识点闭包(截至第10周已学,本周可直接用)

Python 全基础与工程技能(语法/函数模块闭包/OOP/文件/异常/venv/requests/re/typing/asyncio)、大模型 API 调用/Prompt/JSON Mode/流式 Streaming/Function Calling、LangChain/LCEL/向量库/RAG 全链路/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP 认知;前端线(第10周已学):TS SSE、EventSource/fetch 流、打字机效果、流式 Markdown 渲染、中断控制、自定义流式对话 hook 与 demo。既有前端能力(10 年 JS/TS/React,语法映射式加速,不重讲基础):组件化、hooks/状态管理(useState/useReducer/context)、TS 类型系统(联合类型/泛型/类型收窄)、fetch/async、列表与条件渲染、BFF/网关调用模式。

本周新增(首教):Vercel AI SDK(useChat/useCompletion/streamText)、LangChain.js、工具调用可视化(前端渲染 tool call 过程与结果)。
【超前】预警:Agent 交互模式(规划/调用/观察/结果)、React 流式对话组件库级、生成式UI(JSON→动态渲染)属第12周内容,其中生成式UI 为【超前·加分】;本周不作正式教学,若产物需要仅以【超前】最小片段出现并标注(见 Day74/Day75)。

---

## Day71(周一,7h)· Vercel AI SDK 入门:useChat

今天把第10周你手写的流式对话 hook 换成成品——Vercel AI SDK 的 useChat。它把"增量拼接、消息状态、loading、发送"这些样板一次性封装好,你只需连自己的后端 route 并渲染消息列表。关键前提:前端永远不碰 key,请求打到 /api/chat,由服务端 route handler 持有密钥再转发给模型。产出:UseChatDemo.tsx,一个可流式收发的对话组件。

💡 前端开发者速读:useChat ≈ 你手写的流式对话 hook 的成品版(messages/input/handleSubmit/isLoading 都替你管好);它内部消费的就是你第10周写过的 fetch 流/数据流,只是不用你手动 ReadableStream 拼接;前端只连 /api/chat ≈ 你熟悉的"前端调 BFF/网关",key 留服务端。

### 学习内容

- Vercel AI SDK 是什么(前端流式对话的成品封装,省样板)
- useChat hook 的返回:messages / input / handleInputChange / handleSubmit / isLoading
- 后端 route handler(/api/chat)承载 key,前端只连自己的后端(零硬编码)
- 把 useChat 的消息列表按 role(user/assistant)渲染成对话 UI
- 与第10周手写 fetch 流/SSE 的对比(SDK 封装了增量拼接与状态)

### 讲解

结论先行:useChat 帮你把"发消息→流式收增量→更新消息列表→loading 态"全打包。你只要给它一个 api 地址(自己的后端 route),它返回的 messages 就是随流式实时增长的数组,直接 map 渲染即可。密钥绝不能出现在前端,而是放在 /api/chat 这个服务端 handler 里,由它代持并转发——这与你既有的 BFF 模式完全一致。

```tsx
// 教学演示:useChat 最小骨架(非产物答案)
"use client";
import { useChat } from "ai/react";

export function ChatDemo() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } =
    useChat({ api: "/api/chat" });   // key 在服务端 route handler,前端不硬编码
  return (
    <div>
      {messages.map((m) => <div key={m.id}>{m.role}: {m.content}</div>)}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit" disabled={isLoading}>发送</button>
      </form>
    </div>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK https://ai-sdk.dev/docs/introduction (useChat / UI Runtimes 章节)
- 实操参考(A级):Chrome 中文 Prompt UI / ai-elements https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 中文搜索词:"Vercel AI SDK useChat 流式对话 教程"、"useChat api route handler key 服务端"(阶段4无可信中文视频,不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | useChat API / route handler 承载 key 精读官方文档 |
| 练习 | 2.5h | 编写 UseChatDemo.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 AI SDK 英文文档片段 |
| 输出 | 1h | GitHub commit + 博客"Agent 工具调用可视化"素材归档 |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检 |

### 当日产出

- [ ] 编写 学习产物/第11周/day71/UseChatDemo.tsx:useChat 流式对话组件(≤120行)
  - 用 useChat 接入自己的后端 /api/chat,实现流式收发的对话组件
  - 渲染消息列表(按 role 区分 user/assistant 样式)、受控输入框、发送按钮、loading 态
  - 流式增量实时显示(消息随流逐字/逐块增长)
  - 前端不硬编码 key:key 在服务端 route handler(第13周 FastAPI 或 Next API route)注入
  - 必须覆盖:空输入禁用发送、请求失败的错误提示、消息 id 作为列表 key
  - 所用知识点清单:Vercel AI SDK(useChat)、React 组件/hooks、TS 类型、fetch/route、条件渲染、列表渲染
- [ ] 补记 学习产物/第11周/day71/index.md:覆盖全部学习内容(代码块纯 TS/TSX 可运行)

### 既有前端能力 → AI集成新用法(对照笔记)

- 你手写的流式对话 hook → useChat 成品版(增量拼接/状态/loading 都封装好)
- 你熟悉的受控 input + form onSubmit → 直接映射 handleInputChange / handleSubmit
- 前端只连自己后端 /api/chat ≈ 你既有的"前端调 BFF/网关"模式,key 留服务端

### 跟练清单(放extra/)

- extra_UseChatLoading.tsx:给对话加"正在输入…"占位气泡与自动滚动到底部,练习流式 UX 细节。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| useChat / route handler 承载 key / 消息列表渲染 | Vercel AI SDK-useChat;Chrome 中文实操 | UseChatDemo.tsx | Vercel AI SDK(useChat)、React hooks、TS 类型、条件/列表渲染、fetch/route |

【超前】标注集中区:useCompletion、生成式UI 属后续/加分内容,本日不深入;仅认知 useChat 是 AI SDK 的对话 hook。
硬约束复查:仅用 day71 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(服务端 route)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day72(周二,7h)· streamText 与流式 UI 绑定

昨天用 useChat 打通了收发,今天看清"流从哪来":服务端用 streamText 生成数据流,前端 useChat 消费它,把增量实时绑定到 UI。这一步把你第10周手写的 ReadableStream 拼接、打字机、流式 Markdown 全接上,并补齐"中断(stop)"能力。产出:StreamTextChat.tsx,前端消费服务端流式增量并逐字渲染、可中断。

💡 前端开发者速读:streamText ≈ 第10周你手写 fetch 流的"服务端封装版"——它 toDataStreamResponse 出来的正是你手动消费过的那种数据流;前端 useChat 消费它 ≈ 你既有的"边收边渲染";stop() ≈ 你第10周写过的 AbortController 中断,SDK 替你封装了。

### 学习内容

- streamText(服务端流式生成)与前端如何消费其数据流(toDataStreamResponse)
- 把流式 token 增量绑定到 UI(逐字渲染,衔接第10周打字机)
- isLoading / 流式中状态处理与中断 stop()
- 流式 Markdown 渲染衔接(第10周已学,增量渲染为富文本)
- 整体数据流:route handler 里 streamText → 前端 useChat 消费

### 讲解

结论先行:流式对话是"两端配合"——服务端 route 用 streamText 把模型输出以数据流返回(toDataStreamResponse),前端 useChat 自动消费这个流并把 messages 实时更新。你要做的是把增量渲染好(逐字/流式 Markdown)并提供中断(stop)。key 与模型配置只在服务端 route,前端拿到的只是数据流,天然不泄密。

```ts
// 教学演示:服务端 route 用 streamText,前端 useChat 消费(非产物答案)
// app/api/chat/route.ts —— key 从服务端环境变量读,前端不接触
import { streamText } from "ai";

export async function POST(req: Request) {
  const { messages } = await req.json();
  const result = streamText({
    model: /* 服务端配置的模型(国产优先:通义千问/DeepSeek/GLM) */,
    messages,
    apiKey: process.env.MODEL_API_KEY,   // 仅在服务端,零硬编码到前端
  });
  return result.toDataStreamResponse();  // 以数据流返回给前端 useChat
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK https://ai-sdk.dev/docs/introduction (streamText / Data Stream 章节)
- 实操参考(A级):Chrome 中文 https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 中文搜索词:"Vercel AI SDK streamText 教程"、"streamText toDataStreamResponse useChat"、"AI SDK 流式 Markdown 前端"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | streamText / 数据流 / 中断 精读官方文档 |
| 练习 | 2.5h | 编写 StreamTextChat.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 AI SDK streamText 英文文档 |
| 输出 | 1h | GitHub commit + 博客素材(流式增量绑定) |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检 |

### 当日产出

- [ ] 编写 学习产物/第11周/day72/StreamTextChat.tsx:流式增量绑定组件(≤120行)
  - 前端消费服务端 streamText 的数据流,把增量实时绑定到 UI 逐字渲染
  - 支持流式中 loading、流式结束态、中断(stop)并清理状态
  - 复用第10周流式 Markdown 渲染,把增量渲染为富文本
  - key 在服务端 route,前端不硬编码
  - 必须覆盖:中断后状态清理、空流/错误流的兜底提示、TS 类型完整
  - 所用知识点清单:Vercel AI SDK(streamText/useChat)、流式渲染、打字机、中断控制、流式 Markdown、TS 类型、React 状态
- [ ] 补记 学习产物/第11周/day72/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 第10周手写 fetch 流 + ReadableStream 拼接 → streamText/useChat 封装了数据流生成与增量消费
- 你既有的打字机 / 流式 Markdown 组件 → 直接复用,只是数据源换成 useChat 的 messages
- stop() ≈ 你写过的 AbortController 中断,SDK 已封装

### 跟练清单(放extra/)

- extra_StreamStop.tsx:加一个"停止生成"按钮,练习中断流式并保留已生成内容、复位 loading。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| streamText / 数据流消费 / 流式绑定 UI / 中断 | Vercel AI SDK-streamText;Chrome 中文 | StreamTextChat.tsx | streamText/useChat、流式渲染、打字机、中断控制、流式 Markdown、TS 类型 |

【超前】标注集中区:ai-elements 流式 UI 组件库的深度定制属【加分·超前】,本日用基础渲染即可,不深入。
硬约束复查:仅用 day72 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(服务端 route)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day73(周三,7h)· LangChain.js 基础:链与模型封装

今天认识 Vercel AI SDK 之外的另一条前端侧路线:LangChain.js——就是你第07周学的 Python 版 LangChain 的 TS/JS 版。用 PromptTemplate + ChatModel 通过 LCEL 的 pipe 组织一条链,概念与 Python 版一一对应,你的 TS 能力可直接迁移。产出:LangChainBridge.ts,用 LangChain.js 组织一次(可流式的)链式调用的服务端桥接。

💡 前端开发者速读:LangChain.js ≈ LangChain 的 TS 版,PromptTemplate/ChatModel/pipe 与 Python 版同名同义;LCEL 的 prompt.pipe(model) ≈ 你熟悉的函数组合/管道;.stream() 返回的异步迭代 ≈ 你用 for await 消费流;它常跑在 Node/服务端,key 同样放服务端环境变量。

### 学习内容

- LangChain.js 是什么(LangChain 的 TS/JS 版,概念对应 Python 版)
- 模型封装(ChatModel)与提示词模板(PromptTemplate)
- 用 LCEL 风格的链(pipe)组织一次调用
- 前端/Node 侧流式(.stream)与 for await 消费
- 国产模型优先(通义千问/DeepSeek/GLM),key 在服务端环境变量

### 讲解

结论先行:LangChain.js 的核心心智与 Python 版一致——把"提示词模板 → 模型"用 pipe 串成一条链,invoke 拿完整结果、stream 拿增量。它通常运行在服务端(Node/route),因此 key 放服务端环境变量,前端只调你自己的桥接接口。对你而言新的是包名与 API 形态,不是概念。

```ts
// 教学演示:LangChain.js 用 LCEL 组织一条链(非产物答案)
import { PromptTemplate } from "@langchain/core/prompts";
import { ChatOpenAI } from "@langchain/openai";   // 示意;换成国产模型对应的 ChatModel

const prompt = PromptTemplate.fromTemplate(
  "把下面的商品描述改写成一句导购话术:{desc}"
);
const model = new ChatOpenAI({ apiKey: process.env.MODEL_API_KEY }); // 服务端,零硬编码到前端
const chain = prompt.pipe(model);            // LCEL:提示词 → 模型

const res = await chain.invoke({ desc: "纯棉圆领短袖,透气" });
console.log(res.content);
```

### 教材与章节

- 官方文档:LangChain.js https://js.langchain.com (Tutorials / LCEL 章节)
- 官方文档(A级,对比):Vercel AI SDK https://ai-sdk.dev/docs/introduction
- 中文搜索词:"LangChain.js 入门"、"LangChain.js LCEL pipe 教程"、"LangChain.js 流式 stream"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | LangChain.js 模型/模板/LCEL/流式 精读官方文档 |
| 练习 | 2.5h | 编写 LangChainBridge.ts + extra 跟练 |
| 英语 | 0.5h | 借工具精读 LangChain.js 英文文档 |
| 输出 | 1h | GitHub commit + 博客素材(AI SDK vs LangChain.js 取舍) |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检 |

### 当日产出

- [ ] 编写 学习产物/第11周/day73/LangChainBridge.ts:LangChain.js 链式调用桥接(≤120行)
  - 用 LangChain.js 组织一次链式调用(PromptTemplate → ChatModel),支持流式输出增量
  - 封装成可被前端调用的服务端桥接函数/route,逐块返回增量结果
  - key 在服务端环境变量,前端不硬编码;国产模型优先(通义千问/DeepSeek/GLM)
  - 必须覆盖:调用异常兜底(try/catch)、空输入处理、TS 类型完整(链的输入/输出有类型)
  - 所用知识点清单:LangChain.js、LCEL/pipe、PromptTemplate、ChatModel、流式(.stream/for await)、TS 类型、async/await、异常处理
- [ ] 补记 学习产物/第11周/day73/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- Python 版 LangChain(第07周)PromptTemplate/chain/LCEL → LangChain.js 概念一一对应,只是 TS 语法
- 你既有的 async/await、for await 消费流、TS 泛型 → 直接可用于链的输入输出类型化
- 链跑在服务端、key 放环境变量 ≈ 你既有的 BFF/网关模式

### 跟练清单(放extra/)

- extra_LangChainStream.ts:把 .invoke 换成 .stream,用 for await 逐块返回增量,练习流式链。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| LangChain.js 模型/模板/LCEL/流式 | LangChain.js 官方文档;AI SDK 对比 | LangChainBridge.ts | LangChain.js、LCEL/pipe、PromptTemplate、ChatModel、流式、TS 类型、异常 |

【超前】标注集中区:LangChain.js 的 Agent/Tool 编排属第12周及以后,本日只做"链 + 模型封装",不深入智能体编排。
硬约束复查:仅用 day73 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(服务端环境)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day74(周四,7h)· 工具调用可视化:把 tool call 渲染成时间线

今天是本周差异化叙事的核心。模型在回答时可能"请求调用工具"(tool call):给出工具名、入参,执行后拿回结果。把这个过程渲染成可见的卡片/时间线,就是"Agent 执行可视化面板"的雏形——正是你区别于纯后端选手的前端×LLM 护城河。产出:ToolCallView.tsx,把一次或多次工具调用的工具名/入参/状态/结果渲染为 UI。

💡 前端开发者速读:工具调用可视化 ≈ 把 tool call 的生命周期渲染成时间线/卡片;call→result 两个状态 ≈ 你熟悉的请求 pending/success 状态机;入参是 JSON ≈ 你用 `<pre>{JSON.stringify(args)}</pre>` 或代码块组件展示;整件事就是"列表渲染 + 卡片组件 + 状态徽章",你的老本行。

### 学习内容

- 什么是 tool call(模型请求调用工具:工具名 / 入参 / 结果)
- useChat 消息里的 tool invocations / parts 结构(工具调用生命周期:call → result)
- 把 tool call 渲染成 UI 时间线/卡片(工具名、入参、状态、结果)
- 工具调用状态(pending/call vs result)的可视化区分
- 与差异化项目「Agent 执行可视化面板」的关系

### 讲解

结论先行:工具调用可视化的本质是"给 tool call 定义清晰的 TS 类型,再按状态渲染"。一条 tool call 至少有工具名、入参、状态(调用中/已返回)、结果四要素;从 useChat 的消息里把这些信息提取出来,交给一个卡片/时间线组件按状态渲染即可。工具的真正执行在服务端(route),前端只负责把过程与结果可视化,不接触 key。

```tsx
// 教学演示:把一次 tool call 渲染成卡片(非产物答案)
type ToolCall = { toolName: string; args: Record<string, unknown>; state: "call" | "result"; result?: string };

function ToolCallCard({ tc }: { tc: ToolCall }) {
  return (
    <div className="tool-card">
      <strong>🔧 {tc.toolName}</strong>
      <span>{tc.state === "call" ? "调用中…" : "已返回"}</span>
      <pre>{JSON.stringify(tc.args)}</pre>
      {tc.result && <p>结果:{tc.result}</p>}
    </div>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK https://ai-sdk.dev/docs/introduction (Tool Calling / useChat tool invocations 章节)
- 实操参考(A级):Chrome 中文 https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 中文搜索词:"AI 工具调用 可视化 前端"、"useChat tool invocations 渲染"、"Vercel AI SDK tool calling"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | tool call 结构 / invocations 提取 / 状态渲染 精读文档 |
| 练习 | 2.5h | 编写 ToolCallView.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 AI SDK tool calling 英文文档 |
| 输出 | 1h | GitHub commit + 博客"Agent 工具调用可视化"核心素材 |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检 |

### 当日产出

- [ ] 编写 学习产物/第11周/day74/ToolCallView.tsx:工具调用可视化组件(≤120行)
  - 定义 tool call 的 TS 类型(工具名 / 入参 / 状态 / 结果)
  - 把一次或多次工具调用渲染为 UI 时间线/卡片列表:展示工具名、入参、状态(调用中/已返回)、结果
  - 从 useChat 消息里提取工具调用信息作为 props 传入组件
  - key 在服务端(工具执行在后端 route),前端不硬编码
  - 必须覆盖:无工具调用时不渲染或占位、结果未返回时的 pending 态、入参 JSON 安全渲染
  - 所用知识点清单:工具调用可视化、TS 类型/interface、React 组件、条件渲染、列表渲染、JSON 展示、useChat 消息结构
- [ ] 补记 学习产物/第11周/day74/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你既有的"列表渲染 + 卡片组件 + 状态徽章"能力 → 直接用于渲染 tool call 生命周期
- tool call 的 call/result ≈ 你熟悉的请求 pending/success 状态机
- 入参 JSON 展示 ≈ 你用 `<pre>`/代码块组件渲染调试信息的老套路

### 跟练清单(放extra/)

- extra_ToolTimeline.tsx:把多个 tool call 按时间顺序渲染成纵向时间线,标注每步状态(可含耗时占位),练习可视化编排。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| tool call 结构 / invocations 提取 / 卡片时间线渲染 | Vercel AI SDK-Tool Calling;Chrome 中文 | ToolCallView.tsx | 工具调用可视化、TS 类型、React 组件、条件/列表渲染、useChat 消息结构 |

【超前】标注集中区:生成式UI(把 tool 返回的 JSON 动态渲染成表单/图表)属第12周【超前·加分】,本日只做固定卡片/时间线渲染,不实现动态渲染。
硬约束复查:仅用 day74 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(工具执行在服务端)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day75(周五,7h)· 消息组件与状态管理

今天把零散能力收拢成"像样的对话应用":组件化拆分消息、管理会话状态。一个真实对话产品要支持多会话切换、历史保持、流式增量高效更新——这些都是你 10 年 React 状态管理的老本行,只是数据模型换成了"消息 + 工具调用"。产出:MessageList.tsx,组件化的消息列表 + 会话状态管理。

💡 前端开发者速读:消息组件化 ≈ 你拆 MessageBubble/MessageList/Composer 的日常;会话状态管理 ≈ useState/useReducer/context 你闭眼能写;消息 + 工具调用的联合类型 ≈ TS discriminated union(按 role 收窄);流式增量 append 到最后一条 assistant ≈ 你处理"实时更新列表末项"的性能套路。

### 学习内容

- 对话消息的组件化拆分(MessageBubble / MessageList / Composer)
- 会话状态管理:多会话切换、历史消息保持(useState/useReducer,既有能力)
- 消息 + 工具调用的统一状态模型(TS 联合类型,按 role 收窄)
- 流式过程中状态更新(增量 append 到末条 assistant)与性能(避免整列表重渲染)
- 生成式UI 概念认知(标【超前·加分】,本日不实现)

### 讲解

结论先行:把对话应用拆成三层——展示层(消息气泡/工具卡片)、状态层(会话与消息的统一模型)、输入层(Composer)。状态模型用 TS 联合类型区分 user/assistant 消息,assistant 消息可携带 tool calls。流式更新时只定位到末条 assistant 消息做增量 append,避免整列表重渲染——这些正是你既有 React 状态管理与性能优化能力的直接迁移。

```tsx
// 教学演示:消息 + 工具调用的统一状态模型(非产物答案)
type Msg =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "assistant"; text: string; tools?: ToolCall[] };

function MessageList({ msgs }: { msgs: Msg[] }) {
  return (
    <ul>
      {msgs.map((m) => (
        <li key={m.id}>
          <span>{m.role}</span>: {m.text}
          {m.role === "assistant" && m.tools?.map((t, i) => <ToolCallCard key={i} tc={t} />)}
        </li>
      ))}
    </ul>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK https://ai-sdk.dev/docs/introduction (消息结构 / 状态章节)
- 实操参考(A级):Chrome 中文 https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 中文搜索词:"React 对话 消息组件 状态管理"、"useChat 多会话 历史"、"生成式UI LLM JSON 动态渲染"(认知,不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 消息组件化 / 会话状态模型 / 流式更新性能 精读 |
| 练习 | 2.5h | 编写 MessageList.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 AI SDK 消息结构英文文档 |
| 输出 | 1h | GitHub commit + 博客素材(对话状态模型设计) |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检 |

### 当日产出

- [ ] 编写 学习产物/第11周/day75/MessageList.tsx:消息组件与会话状态管理(≤120行)
  - 把对话拆成可复用消息组件(MessageList / MessageBubble / Composer)
  - 会话状态管理:支持多会话切换,每个会话保持自己的历史消息与工具调用
  - 统一消息状态模型(user/assistant 消息 + 关联 tool calls),用 TS 联合类型约束并按 role 收窄
  - 流式增量更新时高效更新状态(定位末条 assistant 消息 append,避免整列表重渲染)
  - key 在服务端,前端不硬编码
  - 必须覆盖:空会话占位、切换会话不丢历史、TS 类型完整(无 any 滥用)
  - 所用知识点清单:会话状态管理、React 组件/hooks/useReducer、TS 联合类型/类型收窄、列表渲染、条件渲染、流式增量更新
- [ ] 补记 学习产物/第11周/day75/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你既有的 React 状态管理(useState/useReducer/context)与组件拆分能力 → 直接迁移到对话应用
- 消息联合类型 discriminated union ≈ 你熟悉的 TS 类型收窄(按 role 分支)
- 流式 append 到末条 ≈ 你处理"实时更新列表末项"的性能套路(key 稳定、局部更新)

### 跟练清单(放extra/)

- extra_SessionSwitch.tsx:加会话列表侧栏,支持新建/切换/删除会话并持久化历史,练习状态管理。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 消息组件化 / 会话状态模型 / 流式更新性能 | Vercel AI SDK-消息结构;Chrome 中文 | MessageList.tsx | 会话状态管理、React hooks/useReducer、TS 联合类型/收窄、列表/条件渲染 |

【超前】标注集中区:生成式UI(把模型返回的 JSON 动态渲染成表单/图表/卡片)属第12周【超前·加分】,本日仅认知概念,不实现动态渲染。
硬约束复查:仅用 day75 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(服务端)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day76(周六,7h)· 综合项目日:流式对话 + 工具调用可视化

今天是项目日,把本周能力拧成一个完整应用:useChat/streamText 流式对话 + LangChain.js(可选)+ 工具调用可视化 + 消息与会话状态管理,并接入真实后端联调,流式逐字返回可用。这正是差异化项目「Agent 执行可视化面板」的第一版可运行形态,也是过本周闸门(day77 检测)的能力预演。产出:StreamToolChatApp.tsx(≤150行)。

💡 前端开发者速读:整体架构就是你搭过的"展示层(消息/工具卡片)+ 状态层(会话)+ 服务层(调后端 route)"前端应用,只是服务层换成 AI 对话;工具执行放服务端 ≈ 你既有的 BFF 模式;把 useChat 的 messages 分流成"文本消息"与"工具调用"两路渲染 ≈ 你按类型分发渲染的常规操作。

### 学习内容(综合复用,无全新理论)

- 把 useChat + streamText + 工具调用可视化 + 消息/会话状态管理整合成一个应用
- 组件接入真实后端(第13周 FastAPI 或 Next API route),流式逐字返回可用
- 至少展示一次工具调用的可视化时间线(工具名/入参/状态/结果)
- 分层组织(展示层/状态层/服务层),为「Agent 执行可视化面板」打底

### 讲解

结论先行:综合项目的关键是"分层 + 一条清晰的流式数据通路"。服务层用 useChat 连后端 route(route 内用 streamText/工具执行,key 在服务端);状态层把 messages 与会话统一管理;展示层分成文本消息与工具调用时间线两路渲染。这样任何一层都能单独替换或调优,也让 day77 的限时盲写有清晰骨架可循。

```tsx
// 教学演示:综合流式对话 + 工具可视化的组件骨架(非产物答案)
"use client";
import { useChat } from "ai/react";

export function StreamToolChat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading, stop } =
    useChat({ api: "/api/chat" });          // key/工具执行都在服务端
  const tools = extractToolCalls(messages);  // 从消息里汇总工具调用(自行实现)
  return (
    <div>
      <MessageList msgs={messages} />
      <ToolTimeline tools={tools} />
      <Composer value={input} onChange={handleInputChange} onSubmit={handleSubmit} />
      {isLoading && <button onClick={stop}>停止</button>}
    </div>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK https://ai-sdk.dev/docs/introduction (综合 / Tool Calling 章节)
- 官方文档:LangChain.js https://js.langchain.com (可选链式调用)
- 实操参考(A级):Chrome 中文 https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 中文搜索词:"Vercel AI SDK 流式对话 工具调用 综合"、"AI 对话应用 前端 集成"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 1.5h | 画分层结构、想清流式数据通路与工具可视化布局 |
| 项目实战 | 3.5h | 编写 StreamToolChatApp.tsx + 接入真实后端联调 |
| 英语 | 0.5h | 借工具精读 AI SDK 综合示例英文文档 |
| 输出 | 1h | GitHub commit + 项目成果沉淀为差异化项目素材 |
| 复盘 | 0.5h | 补 index.md、闭包与类型自检、列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第11周/day76/StreamToolChatApp.tsx:流式对话+工具可视化综合应用(项目日,≤150行)
  - 用 Vercel AI SDK(useChat/streamText)做流式对话组件,接入真实后端 route,流式逐字返回可用
  - 集成 day74 工具调用可视化:至少展示一次 tool call 的工具名/入参/状态/结果时间线
  - 集成 day75 消息组件与会话状态管理;支持中断(stop)、loading、错误提示
  - key 在服务端 route handler,前端零硬编码;第三方 npm 包(ai sdk / langchain.js)在 package.json 登记
  - 必须覆盖:流式中断后状态清理、无工具调用时的降级展示、TS 类型完整
  - 所用知识点清单:Vercel AI SDK(useChat/streamText)、工具调用可视化、会话状态管理、LangChain.js(可选)、React 组件/hooks、TS 类型、fetch 流/route、异常处理
- [ ] 补记 学习产物/第11周/day76/index.md:覆盖设计思路(分层)与全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你搭过的"组件容器 + 状态管理 + 服务层调用"前端应用架构 → 直接映射到 AI 对话应用
- 工具执行放服务端、前端只连 route ≈ 你既有的 BFF/网关模式,key 不出服务端
- messages 分流成"文本 + 工具调用"两路渲染 ≈ 你按数据类型分发渲染的常规操作

### 跟练清单(放extra/)

- extra_AgentPanel.tsx:把工具调用时间线升级为「Agent 执行可视化面板」雏形(规划→调用→观察→结果 分栏),作为差异化项目素材。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| AI SDK 流式对话 + 工具可视化 + 状态管理综合 | Vercel AI SDK-综合/Tool Calling;LangChain.js | StreamToolChatApp.tsx | useChat/streamText、工具调用可视化、会话状态管理、React、TS 类型、fetch 流/route |

【超前】标注集中区:生成式UI(把工具返回 JSON 动态渲染成表单/图表)属第12周【超前·加分】,本综合日只做固定卡片/时间线可视化,不实现动态渲染。
硬约束复查:仅用 day76 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(服务端 route)✓ 项目日 ≤150行 ✓ extra 命名正确 ✓

---

## Day77(周日,7h)· 周检测 + 对账

今天是本周闸门。目标是限时独立完成一个"接入真实后端的流式对话组件 + 至少一次工具调用可视化",验证本周 AI SDK/工具可视化能力已内化。通过后即可平稳进入第12周(Agent 交互模式 + React 流式对话组件 + 生成式UI 加分)。本周非阶段闸门(阶段4闸门在 day84:流式逐字输出 + 中断 + 工具调用可视化,TS 类型完整)。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第11周/day77/AiSdkChatCheck.tsx:

1. 用 Vercel AI SDK(useChat)实现一个流式对话组件,接入后端 route(/api/chat),消息可流式逐字返回。
2. 渲染消息列表(区分 user/assistant),含输入框、发送、loading、中断(stop)。
3. 能把至少一次工具调用的过程与结果可视化(工具名 / 入参 / 状态 / 结果,卡片或时间线)。
4. TS 类型完整(消息与工具调用都有类型定义,无 any 滥用)。
5. key 在服务端,前端不硬编码;第三方包在 package.json 登记。

通过标准(须全部满足):

- 45 分钟内完成,组件可运行、流式对话可跑通(从真实后端逐字返回);
- 工具调用可视化可见(至少一次 tool call 的工具名/入参/结果被渲染出来);
- TS 类型完整,tsc 无类型错误;
- key 不硬编码(前端不出现任何密钥,一律走服务端 route);
- 仅用截至 day77 的闭包知识点;≤180行(周末检测放宽)。

未通过补救方案:

- 仅个别错误(useChat 字段 / 工具调用类型)→ 当天用缓冲 1h 对照 Day71/Day74 讲解订正,次日重盲写一次(≤45min);
- 流式/联调不通(前端收不到流或工具不触发)→ 重做 Day72(streamText 消费)+ Day76(后端联调),再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第12周前 2 天先补 AI SDK 欠账,再进入 Agent 交互模式;day84 阶段4闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项✅/❌/⚠️):
   - day71/UseChatDemo.tsx ☐ day71/extra/extra_UseChatLoading.tsx ☐ day71/index.md ☐
   - day72/StreamTextChat.tsx ☐ day72/extra/extra_StreamStop.tsx ☐ day72/index.md ☐
   - day73/LangChainBridge.ts ☐ day73/extra/extra_LangChainStream.ts ☐ day73/index.md ☐
   - day74/ToolCallView.tsx ☐ day74/extra/extra_ToolTimeline.tsx ☐ day74/index.md ☐
   - day75/MessageList.tsx ☐ day75/extra/extra_SessionSwitch.tsx ☐ day75/index.md ☐
   - day76/StreamToolChatApp.tsx ☐ day76/extra/extra_AgentPanel.tsx ☐ day76/index.md ☐
   - day77/AiSdkChatCheck.tsx(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5(功能完整性/闭包合规/行数与命名/代码质量四维)/卡点/补救。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第12周前 2 天改补欠账。
4. 验收:每个组件能运行 / tsc 类型通过;把本周成果沉淀为博客「Agent 工具调用可视化」素材(验证规则求职级 5-8 篇之一)。**简历诚信复述**:头衔写真实的「前端开发工程师」,「即时零售 SaaS / 商品营销域」放业务描述而非头衔,AI 项目置顶;背调可核对社保/前雇主职位,不一致可被撤回 offer。

## 周尾附录:完整知识点累计清单(截至第11周day77)

第01-10周(已有):Python 全基础与工程技能(语法/函数模块闭包/OOP/文件/异常/venv/requests/re/typing/asyncio)、大模型 API/Prompt/JSON Mode/流式 Streaming/Function Calling、LangChain/LCEL/向量库/RAG 全链路/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP 认知;前端线(第10周):TS SSE、EventSource/fetch 流、打字机效果、流式 Markdown 渲染、中断控制、自定义流式对话 hook 与 demo;既有 JS/TS/React 能力(组件化/hooks/状态管理/TS 类型/fetch/BFF 模式)。

第11周(本周新增):

- Vercel AI SDK:useChat(messages/input/handleInputChange/handleSubmit/isLoading/stop)、useCompletion(认知)、streamText(服务端流式生成)、toDataStreamResponse、后端 route handler 承载 key(前端零硬编码)。
- LangChain.js:ChatModel 封装、PromptTemplate、LCEL/pipe 链、.invoke/.stream(for await 消费)、与 Python 版 LangChain 概念对应、国产模型优先。
- 工具调用可视化:tool call 结构(工具名/入参/状态/结果)、从 useChat 消息提取 tool invocations、渲染为卡片/时间线、pending(call)与 result 状态区分。
- (会话状态管理为既有 React 能力的应用,非新语言点。)
- 【超前】识别项(不要求掌握):Agent 交互模式(规划/调用/观察/结果,第12周)、React 流式对话组件库级(第12周)、生成式UI(JSON→动态渲染,第12周【超前·加分】)。

下周预告(第12周day78-84):Agent 交互模式(规划/调用/观察/结果)、React 流式对话组件(库级)、生成式UI(JSON→动态渲染,加分);把本周工具调用可视化升级为完整 Agent 交互与动态 UI,完成组件库级流式对话 demo,项目2「营销活动配置 Copilot」开发。day84 为阶段4闸门:流式逐字输出 + 中断 + 工具调用可视化,TS 类型完整。
