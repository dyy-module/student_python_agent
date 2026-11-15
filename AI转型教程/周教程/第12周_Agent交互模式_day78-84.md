# 第12周 · Agent 交互模式 + React 流式对话组件(阶段4闸门)

> 与主计划的差异说明:本周严格对应修订版路线图「阶段4后段」(17周映射第12周,day78-84),**day84 为阶段4闸门**(量化标准以骨架第12周/里程碑表为准:流式逐字输出 + 中断 + 工具调用可视化三项齐备,且 TS 类型完整)。据《00_主计划_2026市场修订版》,差异化在"前端×LLM 交互层"——本周把第09周后端 Agent 与第10-11周前端流式打通,收口成组件库级 React 流式对话组件,并落地差异化项目「Agent 执行可视化面板(规划→调用→观察→结果)」。**生成式 UI(JSON→动态渲染表单/图表/卡片)为【超前·加分·选做】**:骨架将其列为差异化项目加分项,但非 reference 日程表第12周首次教学点,本周不强制,做了标注加分。阶段4为前端 TS/React 产物,前端不硬编码 key(经后端代理/服务端注入)。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第12周/dayN/<文件名>.tsx|.ts;跟练统一命名 extra_*.tsx / extra_*.ts 放入 学习产物/第12周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。产物一律由学习者本人盲写,AI 不代写(讲解代码块仅为教学演示,非产物答案)。

## 本周概览

- 主题:把后端 Agent 的执行过程"前端化"——用可辨识的类型建模 Agent 交互轨迹(规划→调用→观察→结果),沉淀一套组件库级 React 流式对话组件(消息/流式文本/工具卡片/对话容器),最终整合成可演示的「Agent 执行可视化面板」。
- 为什么对拿 offer 有用:本周是"前端×LLM 交互层"差异化叙事的收口——它把你第09周做的后端 Agent(ReAct/Tool/Memory/LangGraph)与第10-11周的前端流式(SSE/打字机/useChat/工具调用可视化)打通,形成一个能当场演示的完整作品「Agent 执行可视化面板」,这正是主计划列的差异化项目;一套可复用的流式对话组件是 AI 前端岗最直接的 Portfolio 作品(JD 高频:流式对话、生成式 UI、Agent 交互可视化),也是项目2「营销活动配置 Copilot」的组件底座。
- 教材使用策略:阶段4无可信中文视频直出,一律用官方文档 + 中文搜索词——主教材 Vercel AI SDK 官方文档(useChat/流式)+ Chrome 中文实操(Prompt UI / ai-elements)+ LangChain.js 官方文档;流式底层复习 MDN SSE 中文文档。英文文档借翻译工具精读(计入每日英语 0.5h),先看 overview 建立骨架,再抠组件封装与类型细节。绝不杜撰 BV 号或视频链接。
- 本周结束时应能做到:
  1. 用 TS 可辨识联合建模 Agent 交互四类节点(规划/调用/观察/结果),并前端渲染成执行轨迹时间线。
  2. 用 useReducer 管理对话消息状态(流式逐字追加 + 中断 + 自动滚动),封装成可复用 React 流式对话组件(props/回调/插槽定制)。
  3. 整合出完整可演示的「Agent 执行可视化面板」:流式对话 + 中断 + 工具/Agent 调用可视化,全链路 TS 类型完整。
  4. day84 阶段4闸门:45 分钟内独立盲写一个组件库级流式对话组件——流式逐字输出 + 可中断 + 至少一次工具/Agent 调用可视化 + TS 类型完整(无 any 滥用)、≤180 行。

## 前置知识点闭包(截至第11周已学)

Python 全基础(类型/控制流/函数/推导式)、OOP/文件/异常全体系、venv/pip/requirements.txt、requests/re/typing/asyncio;大模型 API、环境变量读 key、Prompt 工程、JSON Mode、流式 Streaming、Function Calling、多轮上下文;LangChain/LCEL、向量数据库、RAG 全链路、Dify/Coze;引用标注、rerank、RAG 评测;**Agent(ReAct:规划→调用→观察→循环)、Tool(工具定义/注册/schema)、Memory(对话/实体记忆)、LangGraph 入门(StateGraph/节点/边/条件路由)、MCP(认知级)**。前端线:**TS SSE、EventSource/fetch 流、打字机效果、流式 Markdown 渲染、中断控制、Vercel AI SDK(useChat)、LangChain.js、工具调用可视化、会话状态管理**。既有前端能力(10 年 JS/TS/React):组件/props/插槽、hooks(useState/useEffect/useReducer/useRef)、事件处理、条件与列表渲染、状态管理、Webpack/RN、TS 类型系统(联合/接口/泛型/类型收窄)。

本周新增(首教,与 reference 日程表第12周一致):Agent 交互模式(前端呈现"规划→调用→观察→结果"的执行轨迹,用可辨识类型建模并渲染)、React 流式对话组件(组件库级完整封装:消息/流式文本/工具卡片/对话容器,可复用可定制)。
【超前】预警:生成式 UI(把模型返回的 JSON 动态渲染为表单/图表/卡片)为【超前·加分·选做】,骨架列为差异化项目加分项但非日程表首教点,本周不强制;XState 级复杂状态机编排、React Server Components 服务端流式渲染本周不深入,若产物涉及一律标【超前】(见 Day83)。

---

## Day78(周一,7h)· Agent 交互模式:用 TS 类型建模执行轨迹

今天进入阶段4收官周。第09周你在后端做了会"规划→调用工具→观察→再规划"的 Agent,并打印了执行轨迹;今天把这套交互模式**搬到前端**——第一步是用 TypeScript 把轨迹的四类节点(规划/调用/观察/结果)建模成清晰、可收窄的类型,这是整周可视化面板的地基。产出:一份 Agent 交互模式的 TS 类型定义文件。

💡 前端开发者速读:Agent 交互模式 ≈ 把后端 agent 的执行轨迹渲染成一条时间线/一组步骤卡片;四类节点用**可辨识联合(discriminated union)**建模最合适——就像你处理 Redux action 时用 `type` 字段分流、TS 自动收窄每个分支的字段;结果节点带 citations ≈ 你给列表项挂 source 溯源链接。

### 学习内容

- Agent 交互模式四阶段:规划(plan)→调用(tool_call)→观察(observation)→结果(answer)
- 用可辨识联合(kind 字段)建模轨迹节点,让 TS 在 switch 中自动收窄类型
- 工具调用状态类型(running/done/error)与消息角色类型(user/assistant)
- Record/可选属性/泛型在轨迹类型中的应用
- 类型导出与复用(供后续组件 import)

### 讲解

结论先行:前端可视化 Agent 的第一步不是画 UI,而是把"轨迹节点"用类型定死——用可辨识联合(discriminated union),每个节点带一个 `kind` 字面量字段,渲染时用 switch 按 kind 分流,TS 会自动收窄出各分支独有字段,既安全又免 any。下面演示这套建模思路(教学用),完整的类型文件由你在产物里盲写。

```tsx
// Agent 执行轨迹四类节点:用可辨识联合(discriminated union)建模
type TraceNode =
  | { kind: "plan"; thought: string }                                  // 规划
  | { kind: "tool_call"; name: string; args: Record<string, unknown> } // 调用
  | { kind: "observation"; result: string }                            // 观察
  | { kind: "answer"; content: string; citations: string[] };          // 结果(带引用)

// 渲染时按 kind 收窄,TS 自动推断各分支字段(免 any、免强转)
function label(n: TraceNode): string {
  switch (n.kind) {
    case "plan":        return `规划:${n.thought}`;
    case "tool_call":   return `调用工具 ${n.name}`;
    case "observation": return `观察到:${n.result}`;
    case "answer":      return `答案:${n.content}(引用 ${n.citations.length})`;
  }
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — 消息/工具调用类型:https://ai-sdk.dev/docs/introduction
- 官方文档:LangChain.js(Agent/工具调用结构):https://js.langchain.com/docs/introduction/
- 搜索词:"Agent 交互模式 规划 调用 观察 结果"、"TypeScript 可辨识联合 discriminated union"、"Agent 执行过程 可视化 前端"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | Agent 交互模式四阶段 + 可辨识联合/类型收窄 精读官方类型章节 |
| 练习 | 2h | 编写 agentTraceTypes.ts + extra 跟练 |
| 英语 | 0.5h | 借工具精读 Vercel AI SDK 英文类型文档一段 |
| 输出 | 1h | GitHub commit、整理"Agent 轨迹类型建模"笔记 |
| 复盘 | 0.5h | 补 index.md,自检类型完整无 any |

### 当日产出

- [ ] 编写 学习产物/第12周/day78/agentTraceTypes.ts:Agent 交互模式 TS 类型(≤120 行)
  - 用可辨识联合定义轨迹节点四类:规划 plan、调用 tool_call、观察 observation、结果 answer,每类带 `kind` 字面量字段与各自字段(结果节点须含 citations 引用数组)
  - 定义工具调用状态类型(running/done/error)与消息角色类型(user/assistant)
  - 定义一个 AgentTrace(轨迹节点数组)与一次工具调用的入参类型(用 Record 或泛型)
  - 所有类型显式导出,供后续组件 import 复用;保证关键接口有类型、无 any 滥用
  - 附一段纯类型层的 mock 轨迹数据(常量数组)以验证类型正确(能通过 tsc/构建编译)
  - 本日为纯类型文件,不涉及 key 与网络请求
  - 所用知识点清单:Agent 交互模式、TS 类型(可辨识联合/interface/type)、字面量类型、Record/泛型、可选属性、类型收窄、export/import
- [ ] 补记 学习产物/第12周/day78/index.md:覆盖全部学习内容(代码块纯 TS/TSX 可编译,禁混 JS 无类型写法)

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:Redux action 用 type 分流 → 新用法:Agent 轨迹节点用 kind 可辨识联合分流
- 既有:接口响应类型定义 → 新用法:把"规划/调用/观察/结果"这套 Agent 语义建成前端类型
- 既有:给列表项挂 source 链接 → 新用法:answer 节点带 citations 引用(呼应第08周引用标注)
- 既有:TS 类型收窄/guard → 新用法:switch(kind) 后安全读取各分支独有字段

### 跟练清单(放extra/)

- extra_traceGuard.ts:为 TraceNode 写一组类型守卫函数(如 isPlanNode / isToolCallNode / isAnswerNode),用它们在不用 switch 的情况下安全收窄并读取对应字段,练习类型守卫。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| Agent 交互模式四阶段 / 可辨识联合 / 类型收窄 | Vercel AI SDK 类型;LangChain.js;搜索词 | agentTraceTypes.ts | Agent 交互模式、可辨识联合、字面量类型、Record/泛型、类型收窄、export |

【超前】标注集中区:生成式 UI 所需的"JSON Schema → 组件"映射类型属【超前·加分·选做】,本日不要求,仅先建好 Agent 轨迹类型地基。
硬约束复查:仅用 day78 闭包知识点 ✓ TS 类型完整(无 any 滥用)✓ key 不硬编码(本日不涉及)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day79(周二,7h)· 对话组件状态管理:消息列表 / 流式追加 / 滚动

有了轨迹类型,今天解决对话组件的"状态心脏":如何管理一个消息列表,在流式返回时逐字追加到当前 assistant 消息、支持中断、并自动滚动到底部。你在第10-11周已用 useChat 体验过流式,今天深入它背后的状态管理模式,自己用 useReducer 实现一遍,才能封装出真正可控的组件。产出:一个对话消息状态管理 hook。

💡 前端开发者速读:对话状态 ≈ 一个消息列表 reducer——"追加新消息 / 流式增量 append / 中断 stop"就是三类 action,和你写购物车/通知列表的 reducer 同构;流式逐字追加 ≈ 按 id 定位那条消息、把 delta 拼到 content 尾部(注意 immutability,别直接改原对象);自动滚动 ≈ 你在聊天窗做的"内容变高就 scrollTop=scrollHeight,用户上滑时暂停"。

### 学习内容

- 用 useReducer 集中管理消息状态(add / append / stop 三类 action)
- 流式逐字追加:按消息 id 定位并拼接 delta(不可变更新)
- 中断:把当前消息标记 done,停止追加
- 自动滚动到底部(useRef + 内容变化时滚动,用户上滑可暂停)
- 消息类型(id/role/content/done)与全链路 TS 类型完整

### 讲解

结论先行:流式对话的状态管理核心是"把每条消息当成可被增量更新的对象"——用 reducer 把"新增消息、流式追加、中断"收敛成三类 action,append 时按 id 定位并用不可变方式拼接 delta,这样 UI 会随状态更新自然逐字刷新。下面演示 reducer 骨架(教学用),完整 hook(含自动滚动、mock 流)由你在产物里盲写。

```tsx
// 对话消息状态:用 reducer 集中管理"追加消息 / 流式增量 / 中断"
type Msg = { id: string; role: "user" | "assistant"; content: string; done: boolean };
type Action =
  | { type: "add"; msg: Msg }
  | { type: "append"; id: string; delta: string }   // 流式逐字追加
  | { type: "stop"; id: string };                    // 中断:标记完成

function reducer(state: Msg[], action: Action): Msg[] {
  switch (action.type) {
    case "add":    return [...state, action.msg];
    case "append": return state.map(m =>
      m.id === action.id ? { ...m, content: m.content + action.delta } : m);
    case "stop":   return state.map(m =>
      m.id === action.id ? { ...m, done: true } : m);
  }
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — useChat / 流式状态:https://ai-sdk.dev/docs/introduction
- 官方文档:MDN Server-sent events(中文,流式底层):https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events
- 搜索词:"React useReducer 消息列表 流式追加"、"聊天 自动滚动 到底部 React"、"React 流式对话组件 封装"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | useReducer 状态模式 / 流式追加 / 中断 / 自动滚动 精读+示例 |
| 练习 | 2.5h | 编写 useChatMessages.ts + extra 跟练 |
| 英语 | 0.5h | 借工具精读 Vercel AI SDK 英文 useChat 状态文档一段 |
| 输出 | 1h | GitHub commit、整理"流式消息 reducer"笔记 |
| 复盘 | 0.5h | 补 index.md,自检类型完整与不可变更新 |

### 当日产出

- [ ] 编写 学习产物/第12周/day79/useChatMessages.ts:对话消息状态管理 hook(≤120 行)
  - 用 useReducer 实现对话消息状态:支持 add(新增消息)、append(按 id 流式逐字追加 delta)、stop(中断,标记 done)三类操作
  - 消息含 id/role/content/done 字段;append 用不可变方式更新(不直接改原对象)
  - 提供自动滚动到底部的能力(暴露容器 ref,内容变化时滚到底;可选:用户上滑时暂停自动滚动)
  - 配一个最小 mock 流(用定时器分段产出 delta)演示逐字追加与中断路径,无需真实后端
  - 全链路 TS 类型完整(Msg/Action 类型明确,无 any 滥用);导出 hook 供组件使用
  - 若接真实后端,endpoint 走后端代理,key 不硬编码在前端
  - 所用知识点清单:React 流式对话组件、useReducer、useState、useRef、不可变更新、消息列表状态、流式追加、中断、自动滚动、TS 类型
- [ ] 补记 学习产物/第12周/day79/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:购物车/通知列表 reducer → 新用法:对话消息 add/append/stop 三类 action
- 既有:列表项不可变更新(map + 展开) → 新用法:流式 delta 按 id 拼接到 content
- 既有:scrollTop=scrollHeight 自动滚动 → 新用法:流式增量触发时保持贴底
- 既有:AbortController 取消请求 → 新用法:中断流式输出并标记 done

### 跟练清单(放extra/)

- extra_autoScroll.ts:实现一个 useAutoScroll hook——新消息或流式增量到来时自动滚到底部,但当用户主动上滑查看历史时暂停自动滚动,滑回底部后恢复,练习滚动与用户意图判断。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| useReducer / 流式追加 / 中断 / 自动滚动 | Vercel AI SDK useChat;MDN SSE;搜索词 | useChatMessages.ts | useReducer/useRef、不可变更新、流式追加、中断、滚动、TS 类型 |

【超前】标注集中区:本日无超前内容(生成式 UI 不涉及);如需引入 XState 级状态机管理复杂对话流属【超前】,本周仅用 useReducer。
硬约束复查:仅用 day79 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(经后端代理)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day80(周三,7h)· 可复用 React 流式对话组件(封装)

昨天做了状态 hook,今天把它连同第11周的 useChat 一起封装成一个**可复用组件**——通过 props 定制后端地址、通过回调暴露工具调用、通过插槽允许自定义消息渲染。组件化封装是"组件库级 demo"与"一次性脚本"的分水岭,也是 AI 前端岗作品可复用性的体现。产出:一个受控的 StreamChat 流式对话组件。

💡 前端开发者速读:封装可复用组件 ≈ 你平时做的"受控组件 + props 配置 + render props/插槽"三件套;endpoint 作为 prop 传入、key 留在服务端代理 ≈ 你从不把密钥写进前端 bundle 的老规矩;onToolCall 回调 ≈ 你给组件留的"事件钩子",外层用它去驱动可视化;renderMessage 插槽 ≈ 你熟悉的 children/render prop 自定义渲染。

### 学习内容

- 受控组件封装:props(endpoint / 回调 / 插槽)驱动行为与外观
- 复用第11周 Vercel AI SDK useChat 做流式收发,组件内只关心编排与渲染
- 流式逐字显示 + 中断按钮(loading 时可点)
- onToolCall 回调(为工具可视化预留钩子)与 renderMessage 插槽(自定义气泡)
- props 类型完整、组件可被外层复用(默认导出 + 类型导出)

### 讲解

结论先行:可复用的关键在"把变化点抽成 props/插槽/回调,把不变的流式逻辑封在内部"——endpoint 让调用方决定接哪个后端代理(key 在服务端注入,前端永不碰),onToolCall 让外层能接管工具可视化,renderMessage 让外层能自定义气泡外观。下面演示这套封装契约(教学用),完整组件由你在产物里盲写。

```tsx
// 可复用流式对话组件:把"流式收发/中断/渲染"封成受控组件,靠 props 定制
type StreamChatProps = {
  endpoint: string;                                       // 后端代理地址(key 服务端注入)
  onToolCall?: (name: string, args: unknown) => void;     // 工具调用回调(可视化钩子)
  renderMessage?: (m: Msg) => React.ReactNode;            // 自定义消息渲染(插槽)
};

export function StreamChat({ endpoint, onToolCall, renderMessage }: StreamChatProps) {
  const { messages, isLoading, stop } = useChat({ api: endpoint });  // 复用第11周 SDK
  return (
    <div className="stream-chat">
      {messages.map(m => renderMessage ? renderMessage(m) : <div key={m.id}>{m.content}</div>)}
      <button onClick={stop} disabled={!isLoading}>中断</button>
    </div>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — useChat / UI 组件:https://ai-sdk.dev/docs/introduction
- 实操(A级):Chrome 中文 — Prompt UI / ai-elements:https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 搜索词:"React 流式对话组件 封装 可复用"、"ai-elements 组件 中文"、"React render props 插槽 自定义渲染"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 受控组件封装 / props-回调-插槽 / useChat 复用 精读+看 ai-elements |
| 练习 | 2.5h | 编写 StreamChat.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 ai-elements / Vercel AI SDK 英文一段 |
| 输出 | 1h | GitHub commit、整理"流式对话组件封装契约"笔记 |
| 复盘 | 0.5h | 补 index.md,自检 props 类型完整 |

### 当日产出

- [ ] 编写 学习产物/第12周/day80/StreamChat.tsx:可复用 React 流式对话组件(≤120 行)
  - 封装一个受控流式对话组件:通过 props 接收 endpoint(后端代理地址)、onToolCall 回调、renderMessage 插槽
  - 复用第11周 Vercel AI SDK useChat 接入后端做流式收发;endpoint 指向后端代理,**key 在服务端注入,前端不硬编码**
  - 支持流式逐字显示消息;提供中断按钮(仅在 loading/流式进行中可点),点击能停止输出
  - onToolCall 在发生工具调用时触发(把工具名与入参抛给外层,供后续可视化);renderMessage 允许外层自定义气泡渲染,未传时用默认渲染
  - props 与消息类型完整(复用 day78/day79 类型),无 any 滥用;组件与类型显式导出以便复用
  - 所用知识点清单:React 流式对话组件、Vercel AI SDK useChat、props/回调/插槽(render prop)、条件渲染、列表渲染 + key、中断、TS 类型完整性
- [ ] 补记 学习产物/第12周/day80/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:受控组件 + props 配置 → 新用法:endpoint/回调/插槽定制流式对话组件
- 既有:children / render prop 自定义渲染 → 新用法:renderMessage 插槽自定义消息气泡
- 既有:组件对外抛事件(onChange 等) → 新用法:onToolCall 把工具调用抛给外层驱动可视化
- 既有:密钥只放服务端/环境变量 → 新用法:前端只接后端代理 endpoint,key 服务端注入

### 跟练清单(放extra/)

- extra_chatSlots.tsx:给 StreamChat 传入一个自定义 renderMessage 插槽,渲染带头像、角色标签与时间戳的消息气泡,验证"不改组件本体即可换外观"的插槽能力。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 受控组件封装 / props-回调-插槽 / useChat 复用 | Vercel AI SDK;Chrome ai-elements;搜索词 | StreamChat.tsx | React 流式对话组件、useChat、props/回调/插槽、条件与列表渲染、中断、TS 类型 |

【超前】标注集中区:本日无超前内容;若把插槽升级为"JSON Schema 驱动的动态渲染"即进入生成式 UI,属【超前·加分·选做】,留待 Day83 选做。
硬约束复查:仅用 day80 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(后端代理)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day81(周四,7h)· 工具 / Agent 结果卡片渲染

Agent 的价值在于"会调用工具",而工具调用过程如果不可见,用户就无法信任与调试。今天把一次工具调用(工具名/入参/结果/状态)渲染成一张清晰的卡片——这是第11周"工具调用可视化"的组件化沉淀,也是执行面板的核心原子件。产出:一个可复用的 ToolCallCard 工具调用卡片组件。

💡 前端开发者速读:工具卡片 ≈ 你写过的"接口请求状态卡/任务卡"——running 转圈、done 打勾、error 标红,和你处理异步请求三态的 UI 完全一致;入参用格式化 JSON 展示 ≈ 你在 devtools 里看的 payload;结果区 ≈ 响应预览。把这套三态卡片复用到"Agent 调工具"上即可。

### 学习内容

- 工具调用可视化:工具名 / 入参 / 结果 / 状态(running/done/error)四要素
- 按状态呈现不同视觉(颜色/图标/文案),复用既有异步三态 UI 经验
- 入参格式化 JSON 展示、结果长文本截断/展开
- 复用 day78 的类型定义,保证 props 类型完整
- 卡片作为原子件被上层面板(day82)组合复用

### 讲解

结论先行:工具卡片的本质是"把一次异步调用的三态可视化"——你早已熟悉 running/done/error 的 UI 语言,现在把它套到 Agent 的工具调用上:标题放工具名与状态,主体放入参(格式化 JSON)与观察结果。下面演示卡片结构(教学用),完整样式、截断展开与多卡片渲染由你在产物里盲写。

```tsx
// 工具调用卡片:把"工具名 / 入参 / 结果 / 状态"渲染成可见卡片
type ToolCall = {
  name: string; args: Record<string, unknown>;
  result?: string; status: "running" | "done" | "error";
};
const statusText = { running: "调用中…", done: "已完成", error: "出错" } as const;

export function ToolCallCard({ call }: { call: ToolCall }) {
  return (
    <div className={`tool-card tool-${call.status}`}>
      <header>🔧 {call.name} · {statusText[call.status]}</header>
      <pre>{JSON.stringify(call.args, null, 2)}</pre>       {/* 入参 payload */}
      {call.result && <output>{call.result}</output>}        {/* 观察结果 */}
    </div>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — tool calling / 工具结果:https://ai-sdk.dev/docs/introduction
- 实操(A级):Chrome 中文 — ai-elements(卡片/组件):https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 搜索词:"工具调用 可视化 前端 卡片"、"Agent 工具调用 展示 入参 结果"、"React 异步状态 三态 UI"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 工具调用可视化四要素 / 三态 UI / JSON 展示 精读+看 ai-elements |
| 练习 | 2.5h | 编写 ToolCallCard.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读 Vercel AI SDK 英文 tool calling 一段 |
| 输出 | 1h | GitHub commit、整理"工具调用可视化"博客素材 |
| 复盘 | 0.5h | 补 index.md,自检卡片 props 类型完整 |

### 当日产出

- [ ] 编写 学习产物/第12周/day81/ToolCallCard.tsx:工具/Agent 结果卡片组件(≤120 行)
  - 实现一个可复用卡片组件,把一次工具调用的 工具名 / 入参 / 结果 / 状态(running/done/error)渲染出来
  - 按状态呈现不同视觉(如颜色/图标/文案区分调用中、已完成、出错)
  - 入参用格式化 JSON 展示;结果区展示观察输出,长文本支持截断 + 展开(点击切换)
  - 复用 day78 的类型定义(工具调用/状态类型),props 类型完整、无 any 滥用
  - 提供一段 mock 工具调用列表,渲染多张卡片验证三态与截断展开
  - 卡片作为原子件导出,供 day82 面板组合;不涉及 key
  - 所用知识点清单:工具调用可视化、React 组件、props、条件渲染、列表渲染 + key、JSON 格式化展示、useState(展开态)、TS 类型完整性、day78 类型复用
- [ ] 补记 学习产物/第12周/day81/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:异步请求三态 UI(loading/success/error) → 新用法:工具调用 running/done/error 卡片
- 既有:devtools 看请求 payload → 新用法:卡片里格式化 JSON 展示工具入参
- 既有:文本截断 + 展开更多 → 新用法:工具结果长文本折叠
- 既有:原子组件复用 → 新用法:ToolCallCard 被 Agent 执行面板组合

### 跟练清单(放extra/)

- extra_resultDiff.tsx:给 ToolCallCard 增加一个"结果对比"视图,传入同一工具的两次调用结果,并排展示差异(如前后数值/文本变化),练习把可视化扩展到多结果对照。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 工具调用可视化四要素 / 三态 UI / JSON 展示 | Vercel AI SDK tool calling;Chrome ai-elements | ToolCallCard.tsx | 工具调用可视化、React 组件、条件与列表渲染、JSON 展示、useState、TS 类型 |

【超前】标注集中区:把工具结果进一步用"JSON Schema 动态渲染成图表/表单卡片"属生成式 UI,为【超前·加分·选做】,本日仅做结构化字段渲染,不强制动态渲染。
硬约束复查:仅用 day81 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(本日不涉及)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day82(周五,7h)· 差异化项目「Agent 执行可视化面板」起步

今天把前三天的成果(轨迹类型 + 状态管理 + 工具卡片)组装成差异化项目的主体——「Agent 执行可视化面板」:把 Agent 的规划→调用→观察→结果按顺序渲染成一条可读的时间线,让用户直观看到"Agent 是怎么一步步想、一步步做的"。这是主计划列明的差异化项目,也是你面试时最能讲出故事的作品。产出:一个 Agent 执行轨迹时间线面板。

💡 前端开发者速读:执行面板 ≈ 你做过的"流程步骤条 / 时间线 / 日志追踪视图"(如 CI 构建步骤、订单流转时间线);按节点 kind 分发到不同子视图 ≈ 你写的一个 switch 渲染器,每种 step 类型对应一个子组件;当前进行中高亮 ≈ 步骤条的 active 态。把 agent 轨迹当成"一次任务的执行步骤条"来渲染即可。

### 学习内容

- 把 Agent 轨迹(TraceNode[])渲染成时间线/步骤卡片(有序、带步骤序号)
- 按节点 kind 分发到不同子视图(规划文本 / 调用嵌 ToolCallCard / 观察 / 结果带引用)
- 轨迹逐步追加时的可读呈现(进行中高亮、自动滚动跟随)
- 复用 day78 类型、day81 卡片,组件组合与数据流
- 面板作为差异化项目主体,为 day83 整合对话做铺垫

### 讲解

结论先行:面板 = "一条按 kind 分流渲染的时间线"——遍历 TraceNode 数组,给每步一个序号,再用一个分发渲染器按 kind 决定这步长什么样(规划显示思考、调用嵌入工具卡片、结果显示答案与引用)。下面演示时间线骨架与分发思路(教学用),完整的进行中高亮、引用展示与滚动跟随由你在产物里盲写。

```tsx
// Agent 执行可视化面板:把轨迹节点渲染成时间线(规划→调用→观察→结果)
export function AgentTracePanel({ trace }: { trace: TraceNode[] }) {
  return (
    <ol className="agent-trace">
      {trace.map((node, i) => (
        <li key={i} className={`trace-step trace-${node.kind}`}>
          <span className="step-index">{i + 1}</span>
          <NodeView node={node} />   {/* 按 kind 分发到不同子视图 */}
        </li>
      ))}
    </ol>
  );
}
// NodeView 内部:switch(node.kind) → plan 文本 / tool_call 用 <ToolCallCard/> / answer 带引用
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — 消息/步骤渲染:https://ai-sdk.dev/docs/introduction
- 实操(A级):Chrome 中文 — ai-elements(布局/卡片):https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 搜索词:"Agent 执行过程 可视化 前端 时间线"、"React 步骤条 时间线 组件"、"Agent 交互模式 规划 调用 观察 结果"

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 时间线/步骤条渲染 + 按 kind 分发 精读+看 ai-elements 布局 |
| 练习 | 2.5h | 编写 AgentTracePanel.tsx + extra 跟练 |
| 英语 | 0.5h | 借工具精读一段 Agent 可视化英文资料 |
| 输出 | 1h | GitHub commit、整理"Agent 执行可视化面板"博客素材 |
| 复盘 | 0.5h | 补 index.md,自检类型收窄与组件复用 |

### 当日产出

- [ ] 编写 学习产物/第12周/day82/AgentTracePanel.tsx:Agent 执行可视化面板(≤120 行)
  - 把 Agent 轨迹节点数组(TraceNode[])按顺序渲染成时间线/步骤卡片,每步带序号
  - 按节点 kind 分发到不同子视图:规划显示思考文本、调用嵌入 day81 的 ToolCallCard、观察显示结果、结果显示答案并列出 citations 引用
  - 支持轨迹逐步追加时的可读呈现:最新/进行中的步骤高亮,面板可随新步骤滚动跟随
  - 复用 day78 类型与 day81 卡片组件;分发渲染用类型收窄(switch kind),TS 类型完整、无 any 滥用
  - 提供 mock trace 数据渲染一条完整时间线验证四类节点都能正确呈现
  - 面板组件导出,供 day83 整合;不涉及 key
  - 所用知识点清单:Agent 交互模式、React 组件、列表渲染 + key、按类型分发渲染、类型收窄、组件复用与组合、条件渲染、TS 类型完整性
- [ ] 补记 学习产物/第12周/day82/index.md:覆盖全部学习内容与设计思路

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:CI 步骤条 / 订单流转时间线 → 新用法:Agent 规划→调用→观察→结果 时间线
- 既有:switch(type) 渲染不同 step 子组件 → 新用法:按 TraceNode.kind 分发子视图
- 既有:步骤条 active 高亮 → 新用法:进行中/最新轨迹步骤高亮
- 既有:列表项挂 source 链接 → 新用法:answer 节点展示 citations 引用可溯源

### 跟练清单(放extra/)

- extra_traceFilter.tsx:给 AgentTracePanel 加一个筛选 toggle(全部 / 只看工具调用 / 只看规划),用数组 filter 后渲染,练习在不改数据源的前提下做视图筛选。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 时间线渲染 / 按 kind 分发 / 组件复用 | Vercel AI SDK;Chrome ai-elements;搜索词 | AgentTracePanel.tsx | Agent 交互模式、列表渲染、分发渲染、类型收窄、组件组合、TS 类型 |

【超前】标注集中区:本日无超前内容(聚焦轨迹可视化);把结果节点升级为"JSON 动态渲染卡片/图表"属生成式 UI,为【超前·加分·选做】,留待 Day83。
硬约束复查:仅用 day82 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(本日不涉及)✓ ≤120 行 ✓ extra/ 命名正确 ✓

---

## Day83(周六,7h)· 综合项目日:整合成完整可演示的 Agent 执行面板

今天是项目日,把整周五天的成果拧成一个能当场演示的完整作品:流式对话收发 + 中断 + Agent 执行轨迹时间线 + 工具调用卡片。这就是差异化项目「Agent 执行可视化面板」的可演示形态,也是 day84 阶段4闸门的直接预演、项目2「营销活动配置 Copilot」的组件底座。产出:整合面板 AgentChatPanel.tsx。

💡 前端开发者速读:整合 ≈ 你熟悉的"容器组件编排若干展示组件"——StreamChat 管收发、AgentTracePanel 管轨迹、ToolCallCard 管工具卡,容器只负责状态编排与数据流(把 onToolCall 的结果塞进 trace);这套"容器 + 展示组件"分层你写了十年,难点只在把流式/中断/轨迹三条数据流接顺。

### 学习内容(综合复用,无全新理论)

- 容器组件编排:StreamChat(收发)+ AgentTracePanel(轨迹)+ ToolCallCard(工具卡)组合
- 三条数据流接顺:流式消息 / 中断 / 工具调用→轨迹追加
- onToolCall 回调把工具调用喂进 trace 状态,驱动面板实时更新
- 前端不硬编码 key(经后端代理/服务端注入);TS 类型完整
- (选做)生成式 UI:把模型返回的 JSON 动态渲染为卡片/表单

### 讲解

结论先行:综合项目的关键仍是"分层组合"——容器只管编排状态与数据流,把已有展示组件拼起来:用 useChat 拿流式消息、用 onToolCall 把每次工具调用追加进 trace、把 trace 交给 AgentTracePanel 渲染,中断按钮接到 stop。下面演示容器的编排骨架(教学用),完整的状态接线、错误兜底与样式由你在产物里盲写。

```tsx
// 综合面板分层:输入区 + 流式对话 + Agent 轨迹时间线 + 工具卡片(整合复用)
export function AgentChatPanel({ endpoint }: { endpoint: string }) {
  const { isLoading, stop } = useChat({ api: endpoint });   // key 服务端注入
  const [trace, setTrace] = useState<TraceNode[]>([]);       // Agent 执行轨迹
  const addCall = (name: string, args: unknown) =>
    setTrace(t => [...t, { kind: "tool_call", name, args: args as Record<string, unknown> }]);
  return (
    <section className="agent-panel">
      <StreamChat endpoint={endpoint} onToolCall={addCall} />
      <AgentTracePanel trace={trace} />
      <button onClick={stop} disabled={!isLoading}>中断</button>
    </section>
  );
}
```

### 教材与章节

- 官方文档(A级):Vercel AI SDK — useChat / 综合示例:https://ai-sdk.dev/docs/introduction
- 实操(A级):Chrome 中文 — Prompt UI / ai-elements:https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn
- 搜索词:"Agent 执行过程 可视化 前端"、"React 流式对话组件 封装"、"生成式UI JSON 动态渲染"(选做)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画容器分层、理清流式/中断/轨迹三条数据流如何接线 |
| 项目实战 | 3h | 编写 AgentChatPanel.tsx,整合复用本周组件 |
| 英语 | 0.5h | 借工具精读一段 Vercel AI SDK 综合示例英文说明 |
| 输出 | 1h | GitHub commit、整理面板 README/演示录屏脚本 |
| 复盘 | 0.5h | 补 index.md,自检类型完整与 key 不硬编码,列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第12周/day83/AgentChatPanel.tsx:完整可演示的 Agent 执行可视化面板(项目日,≤150 行)
  - 容器组件整合本周成果:流式对话收发(StreamChat)+ Agent 执行轨迹时间线(AgentTracePanel)+ 工具调用卡片(ToolCallCard)
  - 接顺三条数据流:流式逐字消息、中断(stop)、工具调用经 onToolCall 追加进 trace 并实时驱动面板
  - 具备阶段4闸门三要素:流式逐字输出可见、可中断、至少一次工具/Agent 调用可视化呈现
  - **前端不硬编码 key**(endpoint 指向后端代理,密钥服务端注入);npm 可用第三方包(Vercel AI SDK 等),能 npm run dev 跑通演示
  - 全链路 TS 类型完整(复用 day78-82 类型),无 any 滥用;错误/空轨迹有基本兜底不白屏
  - (选做,【超前·加分】)生成式 UI:若学有余力,尝试把模型返回的一段 JSON(schema)动态渲染为卡片/表单,不强制
  - 所用知识点清单:Agent 交互模式、React 流式对话组件、工具调用可视化、容器组件编排与复用、Vercel AI SDK useChat、useState、TS 类型完整性
- [ ] 补记 学习产物/第12周/day83/index.md:覆盖设计思路(容器分层/数据流)与全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 既有:容器组件 + 展示组件分层 → 新用法:AgentChatPanel 编排 StreamChat/TracePanel/ToolCallCard
- 既有:父组件下传回调收集子组件事件 → 新用法:onToolCall 把工具调用汇入 trace 状态
- 既有:npm run dev 本地演示 → 新用法:面板作为差异化项目可当场演示
- 既有:密钥只走服务端 → 新用法:endpoint 接后端代理,前端零 key

### 跟练清单(放extra/)

- extra_generativeUI.tsx:(【超前·加分·选做】)把一段模型返回的 JSON(如 { type:"form", fields:[...] } 或 { type:"card", ... })按 type 动态渲染为对应组件(表单/卡片),体验"JSON Schema 驱动动态渲染"的生成式 UI 思路,不做也可。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 容器编排 / 三条数据流 / 组件整合复用 | Vercel AI SDK;Chrome ai-elements;搜索词 | AgentChatPanel.tsx | Agent 交互模式、React 流式对话组件、工具调用可视化、组件组合、useChat、TS 类型 |

【超前】标注集中区:生成式 UI(JSON→动态渲染表单/图表/卡片)属【超前·加分·选做】,骨架列为差异化项目加分项但非日程表首教点,本日不强制;若实现请在 index.md 标注【超前·加分】并说明 JSON→组件的映射方式。
硬约束复查:仅用 day83 闭包知识点 ✓ TS 类型完整 ✓ key 不硬编码(后端代理)✓ 项目日 ≤150 行 ✓ extra/ 命名正确 ✓

---

## Day84(周日,7h)· 周检测 / 阶段4闸门 + 对账

今天是本周闸门,也是**阶段4闸门**(里程碑表 day84)。目标是限时独立盲写一个组件库级流式对话组件,验证"流式逐字 + 中断 + 工具调用可视化 + TS 类型完整"已内化。通过后即完成阶段4(TS+AI 前端集成),平稳进入第13周阶段5工程化(FastAPI/Docker);本周的「Agent 执行可视化面板」应作为差异化项目沉淀进作品集与博客。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第12周/day84/ChatLibCheck.tsx:

1. 一个完整的流式对话组件:发送消息后能**流式逐字输出** assistant 回复(可用真实后端代理,或最小 mock 流分段产出 delta)。
2. 提供**可中断**能力:流式进行中点击中断能停止输出,并把当前消息标记完成。
3. 至少呈现**一次工具/Agent 调用可视化**:把一次工具调用(工具名/入参/结果/状态)渲染为可见卡片或轨迹步骤。
4. **TS 类型完整**:消息、动作、工具调用、props 均有明确类型,用可辨识联合/接口建模,无 any 兜底、无 @ts-ignore。
5. 组件结构清晰(容器 + 展示),可被复用;消息列表用不可变方式更新。

通过标准(须全部满足,对齐骨架 day84 阶段4闸门):

- 45 分钟内完成,组件能构建/运行(npm run dev 或 tsc 通过)、无运行时报错;
- **流式逐字可见**(回复随 delta 增量刷新,而非一次性出现);
- **可中断**(中断后停止追加,状态一致不残留 loading);
- **工具调用可视化呈现**(至少一次,工具名/入参/结果/状态可见);
- **TS 类型完整**(关键接口有类型,无 any 滥用/无 @ts-ignore);
- **key 不硬编码**(经后端代理/服务端注入),仅用截至 day84 的闭包知识点,npm 第三方包合规,**≤180 行**(周末检测放宽)。

未通过补救方案:

- 仅个别错误(如类型标注不全、中断后状态残留)→ 当天用缓冲 1h 对照 Day79/Day80 讲解订正,次日重盲写一次(≤45min);
- 流式逐字/中断不通 → 重做 Day79(状态管理)+ Day80(组件封装);工具可视化不呈现 → 重做 Day81 + Day82;
- 严重超时(>90min)或结构混乱 → 本周降级:第13周(阶段5)前 2 天先补前端流式/可视化欠账,再进入 FastAPI/Docker,**阶段4闸门顺延但不取消**。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day78/agentTraceTypes.ts ☐ day78/extra/extra_traceGuard.ts ☐ day78/index.md ☐
   - day79/useChatMessages.ts ☐ day79/extra/extra_autoScroll.ts ☐ day79/index.md ☐
   - day80/StreamChat.tsx ☐ day80/extra/extra_chatSlots.tsx ☐ day80/index.md ☐
   - day81/ToolCallCard.tsx ☐ day81/extra/extra_resultDiff.tsx ☐ day81/index.md ☐
   - day82/AgentTracePanel.tsx ☐ day82/extra/extra_traceFilter.tsx ☐ day82/index.md ☐
   - day83/AgentChatPanel.tsx ☐ day83/extra/extra_generativeUI.tsx(选做)☐ day83/index.md ☐
   - day84/ChatLibCheck.tsx(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5/卡点/补救,并记录**阶段4闸门达成情况**(流式逐字 + 中断 + 工具调用可视化 + TS 类型完整 四项是否齐备);把「Agent 执行可视化面板」作为**差异化项目写入作品集**(附演示录屏/在线地址),并整理为博客素材(如"Agent 工具调用可视化")。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第13周前 2 天改补前端流式/可视化欠账,闸门顺延不取消。
4. 验收:每个 .tsx/.ts 必须能构建/运行(tsc 或 npm run dev 通过);ChatLibCheck.tsx 需实际演示出"流式逐字 + 中断 + 工具可视化 + 类型完整"方可判定阶段4闸门通过。

## 周尾附录:完整知识点累计清单(截至第12周day84)

第01-11周(已有):Python 全基础、OOP/文件/异常全体系、venv/pip/requirements.txt、requests/re/typing/asyncio;大模型 API、环境变量读 key、Prompt、JSON Mode、流式 Streaming、Function Calling、多轮上下文;LangChain/LCEL、向量数据库、RAG 全链路、Dify/Coze;引用标注、rerank、RAG 评测;Agent(ReAct)、Tool、Memory、LangGraph 入门、MCP(认知);前端线:TS SSE、EventSource/fetch 流、打字机、流式 Markdown、中断控制、Vercel AI SDK(useChat)、LangChain.js、工具调用可视化、会话状态管理;既有 JS/TS/React 能力。

第12周(本周新增):

- Agent 交互模式:前端呈现"规划(plan)→调用(tool_call)→观察(observation)→结果(answer)"执行轨迹、用可辨识联合建模节点、按 kind 类型收窄分发渲染、执行轨迹时间线/步骤卡片、进行中高亮、结果带 citations 引用
- React 流式对话组件(组件库级):useReducer 消息状态(add/append/stop)、流式逐字追加(不可变更新)、中断、自动滚动、受控组件封装(props/回调 onToolCall/插槽 renderMessage)、工具调用卡片(工具名/入参/结果/三态)、容器组件编排(StreamChat + AgentTracePanel + ToolCallCard)、全链路 TS 类型完整性

【超前】识别项(不要求掌握):生成式 UI(JSON→动态渲染表单/图表/卡片,加分选做)、XState 级复杂状态机编排、React Server Components 服务端流式渲染

下周预告(第13周day85-91):进入阶段5工程化——FastAPI(路由/依赖注入/Pydantic、SSE/WebSocket 服务化)、Docker、docker-compose,把本周前端对接的后端 Agent/RAG 服务化并容器化,目标"本地一键起全链路(前端→FastAPI→LLM/RAG)";同步推进项目2「营销活动配置 Copilot」上线与云服务器采购。
