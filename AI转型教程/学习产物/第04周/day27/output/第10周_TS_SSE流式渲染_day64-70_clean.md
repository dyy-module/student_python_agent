# 第10周 · TS SSE + 流式渲染 + 打字机效果(阶段4前端线开始)

> 与主计划的差异说明:本周严格对应修订版路线图「阶段4前段」(17周映射第10周),是前端线的开始。经过前九周的 Python 全栈 + 大模型 API/RAG/Agent 打底,本周回到你的主场——用 10 年 JS/TS/React 经验做"AI 流式集成",落地主计划反复强调的差异化定位「前端×LLM 交互层」。主题为 TS SSE(EventSource/fetch 流类型化接收)、流式渲染(流式 Markdown 增量渲染 / 中断控制)、打字机效果(逐字/逐块),与 reference 日程表第10周首教项完全一致。本周以浏览器原生 SSE/fetch 流为主,Vercel AI SDK / LangChain.js 第11周才正式教(本周仅【超前】识别)。诚实标注(单一事实源):据主计划,Vercel AI SDK/LangChain.js 的"前端护城河"暂无权威 JD 佐证,列为自选加分,不作为既定事实。闸门为 day70 周检测(流式 demo 三要素可演示)。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第10周/dayN/.tsx 或 .ts;跟练统一命名 extra_*.tsx / extra_*.ts 放入 学习产物/第10周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。

## 本周概览

- 主题:用 TypeScript + React 打通"流式交互三要素"——逐字打字机、流式 Markdown 增量渲染、可中断,做出一个能现场演示的流式对话 demo。
- 为什么对拿 offer 有用:流式交互是 AI 应用体验的核心(用户看到的"AI 边想边说"就是它),直接支撑作品集旗舰项目1"商品知识库导购问答"的 React SSE 流式前端;更是你相对纯 Python 背景候选人的差异化护城河——主计划把定位钉在"前端×LLM 交互层",本周就是这条叙事的第一块实证。(诚实提醒:该护城河目前为自选加分,尚无权威 JD 一手佐证,面试时以"我能把 AI 应用的交互体验做到生产级"来陈述,而非夸大为行业硬门槛。)
- 教材使用策略:阶段4无可信中文视频直出,一律用官方文档 + 中文搜索词——MDN(SSE/EventSource/AbortController/ReadableStream 权威且中文完善)(50%)+ Vercel AI SDK 官方文档预读流式章节(30%)+ Chrome 中文实操 ai-elements(20%)。凡涉具体 API,以 MDN 官方为准,严禁依赖来路不明的 BV 号视频。
- 本周结束时应能做到:
  1. 用 EventSource 与 fetch + ReadableStream(getReader)两种方式类型化地接收 SSE/流式分块,并说清二者取舍(GET-only vs 可 POST/带 header)。
  2. 实现打字机效果(逐字/逐块渲染)与流式 Markdown 增量渲染,并保证组件卸载时清理定时器/流。
  3. 用 AbortController 实现流式接收的中断控制,正确处理 AbortError。
  4. day70 闸门:45分钟内独立盲写一个"逐字打字机 + 流式 Markdown + 可中断"三要素齐备、TS 类型完整的流式渲染 demo。

## 前置知识点闭包(截至第09周已学)

Python 全栈(基础语法/控制流/数据结构、函数与模块、OOP、文件读写、异常全体系、venv/pip/requirements、requests、正则 re、typing、asyncio);大模型 API 调用、环境变量读 key、Chat API、Prompt 工程、JSON Mode 结构化输出、流式 Streaming、Function Calling、多轮上下文;LangChain/LCEL、向量数据库(Chroma/Milvus/Faiss)、RAG 全链路(加载→切分→向量化→检索→生成)、Dify/Coze 入门;引用标注、rerank 重排、RAG 评测方法(命中率/召回);Agent、Tool、Memory、ReAct、LangGraph 入门、MCP(认知)。

既有前端能力(10 年 JS/TS/React,熟悉 Webpack/RN):本周以"语法映射式"加速——不重讲 JS/TS/React 基础(组件、hooks、状态、TypeScript 类型系统、Promise/async-await、fetch、EventSource 你已熟练),只讲这些既有能力如何对接"AI 流式集成"这一新场景。

本周新增(首教):TS SSE(EventSource / fetch 流的类型化接收)、流式渲染(流式 Markdown 增量渲染 / 中断控制)、打字机效果(逐字/逐块渲染)。

【超前】预警:Vercel AI SDK(useChat)、LangChain.js、工具调用可视化、会话状态管理第11周首教;Agent 交互模式、React 流式对话组件(组件库级)、生成式 UI 第12周首教。本周以浏览器原生 SSE/fetch 为主,不引入 ai SDK 包做正式教学;若示例偶涉,仅以【超前】最小片段出现并标注。

---

## Day64(周一,7h)· SSE 基础:EventSource / fetch 流的类型化接收

今天进入阶段4。前九周你在后端(Python)侧已把流式 Streaming 跑通,今天切到前端:如何把服务端源源不断推送的分块(chunk)类型化地接住。两条主流路径——原生 EventSource(简单但只能 GET)与 fetch + ReadableStream(可 POST、可带 header、可中断,更通用)。产出:sseClient.ts,连一个本地 mock SSE 服务,逐块接收并输出。

💡 前端开发者速读:EventSource 你早就用过(它就是浏览器原生 SSE 客户端);今天的"新"在于:①用 TS 给分块与消息类型建模,而不是 `any` 满天飞;②掌握 fetch + `res.body.getReader()` 这条更现代的路径(它能配合明天的 AbortController 中断,SSE 的 EventSource 只能 close 不能真正 abort 请求)。把 LLM 的流式输出当成"一个会持续 yield 文本片的可读流"来接即可。

### 学习内容

- SSE 协议要点:`text/event-stream`、`data:` 行、事件分块
- EventSource 的 onmessage/onerror、连接与 close
- fetch + ReadableStream:`res.body!.getReader()` + `TextDecoder` 逐块解码
- 用 TS 为分块/消息建模(接口/联合类型),避免 any
- 两种方式的取舍:EventSource(GET-only、自动重连)vs fetch 流(可 POST/带 header/可中断)
- key 安全:流式数据来自本地 mock SSE 服务或后端代理(第13周 FastAPI),前端不硬编码任何大模型 key

### 讲解

结论先行:接收流有两条路。EventSource 开箱即用但只能发 GET、无法自定义 header;fetch + ReadableStream 更通用——你手动 `getReader()` 拿到读取器,循环 `read()` 逐块取字节,再用 `TextDecoder` 解码成文本。对 AI 流式场景,fetch 流是主力(因为要 POST 提示词、要能中断)。无论哪条,都用 TS 把"分块"和"解析后的消息"类型化。数据源本周用你自己起的本地 mock SSE 服务(工具脚本,不计入闭包产物),key 一律不进前端。

```ts
// 方式一:EventSource(仅 GET,浏览器原生,自动重连)
const es = new EventSource("/mock-sse");
es.onmessage = (e) => console.log("分块:", e.data);   // e.data 是字符串
es.onerror = () => es.close();

// 方式二:fetch + ReadableStream(可 POST/带 header/可中断,主力)
const res = await fetch("/mock-sse");
const reader = res.body!.getReader();
const decoder = new TextDecoder();
while (true) {
  const { value, done } = await reader.read();
  if (done) break;
  console.log(decoder.decode(value));   // 逐块拿到文本
}
```

### 教材与章节

- 主教材/官方文档:MDN Server-Sent Events(中文,权威)— 使用 SSE:(https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events/Using_server-sent_events) ;EventSource:(https://developer.mozilla.org/zh-CN/docs/Web/API/EventSource) ;检索词"MDN Server-Sent Events 中文"、"fetch ReadableStream getReader 流式"。
- 预读(A级文档):Vercel AI SDK 官方文档(流式概念,第11周正式用):(https://ai-sdk.dev/docs/introduction) ;检索词"SSE 前端 流式渲染 教程"。
- mock 数据源:自己起一个极简本地 SSE 服务(如用一个 Node http 服务按 `text/event-stream` 每秒推一行),此为工具脚本、非闭包产物。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | SSE 协议、EventSource、fetch + ReadableStream、TS 类型建模 精读+实验 |
| 练习 | 2h | 编写固定产物 sseClient.ts + 起本地 mock SSE 服务 + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 MDN / Vercel AI SDK 英文文档流式章节 |
| 输出 | 1h | GitHub commit(向 150+ 迈进);开写"SSE 流式渲染踩坑"博客素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包与类型完整、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day64/sseClient.ts:类型化 SSE/流式接收客户端(≤120行)
  - 前置:起一个本地 mock SSE 服务(工具脚本)按 `text/event-stream` 持续推送文本分块;前端不含任何大模型 key
  - 用 TS 定义分块与解析后消息的类型(接口/联合类型),不使用 any 兜底
  - 分别用 EventSource 与 fetch + ReadableStream(getReader + TextDecoder)两条路径接收同一 mock 流,逐块打印
  - 输入:mock SSE 地址;输出:控制台/页面按到达顺序输出每个分块,并在流结束时打印"完成"
  - 必须覆盖行为:处理流结束(done)、处理连接错误(onerror / catch)、EventSource 用完 close、fetch 流读完释放 reader;每步有可见输出
  - 所用知识点清单:TS SSE、EventSource、fetch + ReadableStream(getReader/TextDecoder)、TS 类型建模、async/await、错误处理
- [ ] 补记 学习产物/第10周/day64/index.md:覆盖全部学习内容(代码块为纯 TS/TSX,禁混 Python 语法)

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会 EventSource 接推送 → 新用法:接的是 LLM 逐 token 输出,需按分块累积成完整回答
- 你已会 `fetch().then(res=>res.json())` → 新用法:`res.body.getReader()` 逐块读流,而非一次性 json
- 你已会 TS 接口建模 → 新用法:给"流分块/消息/结束信号"建类型,让流式状态可类型安全流转
- 你已会 async/await → 新用法:`while(true){ read() }` 循环消费流直到 done

### 跟练清单(放extra/)

- extra_stream_to_dom.ts:把 sseClient 收到的分块实时 append 到页面一个 ``(原生 DOM 或最小 React),体会"边收边显示"的最朴素形态,为明天打字机做铺垫。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| SSE / EventSource / fetch 流类型化接收 | MDN SSE/EventSource;Vercel AI SDK 预读 | sseClient.ts | TS SSE、EventSource、fetch+ReadableStream、TS 类型、async/await、错误处理 |

【超前】标注集中区:本日无超前内容(Vercel AI SDK/useChat 属第11周,今天只用浏览器原生 API)。
硬约束复查:仅用 day64 闭包知识点 + 既有前端能力 ✓ TS 类型完整(无 any 兜底)✓ key 不硬编码(用本地 mock/后端代理)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day65(周二,7h)· 打字机效果组件:逐字 / 逐块渲染

昨天能接住流,今天让它"好看地出现"。打字机效果是 AI 应用最具辨识度的交互——文本逐字浮现,而非整段闪现。核心是用定时器/requestAnimationFrame 按节奏推进"已显示长度",并在组件卸载或文本变化时正确清理。产出:TypewriterText.tsx,传入一段文本,逐字显示,速度可调。

💡 前端开发者速读:打字机 ≈ 你写过的 `setInterval` 逐帧推进 + `text.slice(0, i)`;差异只在"清理时机"——React 里必须放在 `useEffect` 的返回函数里 `clearInterval`,否则文本切换/组件卸载会内存泄漏或串字。对 LLM 场景,文本是"边收边增长"的,所以打字机要能应对 text 动态变长(今天的固定文本版是基础,综合日再叠加流式)。

### 学习内容

- 打字机原理:维护"已显示字符数",按节奏递增,用 slice 截取当前应显示文本
- setInterval vs requestAnimationFrame 的取舍(简单节奏 vs 平滑/可控帧)
- React useEffect 的依赖与清理函数(防泄漏、防串字)
- 速度可控(speed 参数)、可重播(text 变化时重置)
- 用 TS 为 props 建类型(text/speed/onDone 等)

### 讲解

结论先行:打字机就是"定时推进一个游标 i,渲染 text.slice(0, i)"。关键难点不在动画本身,而在生命周期管理:文本变化或组件卸载时必须清掉旧定时器,否则会出现"多段文本互相串字"或内存泄漏。把逻辑封装成自定义 hook(useTypewriter)最干净:输入 text/speed,输出"当前应显示的字符串"。

```tsx
function useTypewriter(text: string, speed = 50) {
  const [shown, setShown] = useState("");
  useEffect(() => {
    let i = 0;
    setShown("");
    const timer = setInterval(() => {
      i += 1;
      setShown(text.slice(0, i));
      if (i >= text.length) clearInterval(timer);
    }, speed);
    return () => clearInterval(timer);   // 卸载/文本变化时清理,防泄漏与串字
  }, [text, speed]);
  return shown;
}
```

### 教材与章节

- 主教材/官方文档:MDN setInterval(中文):(https://developer.mozilla.org/zh-CN/docs/Web/API/setInterval) ;requestAnimationFrame(中文):(https://developer.mozilla.org/zh-CN/docs/Web/API/requestAnimationFrame) ;检索词"React 大模型 打字机 流式渲染"、"打字机效果 useEffect 清理"。
- 实操参考(A级):Chrome 中文 Prompt UI / ai-elements:(https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn) 。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 打字机原理、setInterval/rAF、useEffect 清理与依赖 精读+实验 |
| 练习 | 2h | 编写固定产物 TypewriterText.tsx + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 MDN 定时器/rAF 英文文档 |
| 输出 | 1h | GitHub commit;把"打字机清理坑"整理进博客素材 |
| 复盘 | 0.5h | 补 index.md、自检类型完整、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day65/TypewriterText.tsx:打字机效果组件(≤120行)
  - 组件接收 text 与 speed(可选)props,逐字显示传入文本;文本变化时可重置重播
  - 用 useEffect + setInterval(或 rAF)推进已显示长度,并在清理函数中清除定时器
  - 用 TS 为 props 建类型;提供"显示完成"回调或状态(可选)
  - 输入:一段文本 + 速度;输出:页面上文本按节奏逐字浮现,结束后停在完整文本
  - 必须覆盖行为:切换 text 不串字、组件卸载不泄漏、speed 可调生效;每步在 UI 或控制台有可观察反馈
  - 所用知识点清单:打字机效果、setInterval/rAF、React useState/useEffect、清理函数、TS 类型(props)
- [ ] 补记 学习产物/第10周/day65/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会 setInterval 做轮播/倒计时 → 新用法:推进"已显示字符游标"实现逐字浮现
- 你已会 useEffect 清理副作用 → 新用法:文本动态增长时防止旧定时器串字(关键坑)
- 你已会受控组件 props 类型 → 新用法:给 text/speed/onDone 建 TS 类型
- 你已会 slice 截字符串 → 新用法:`text.slice(0, i)` 表达"当前应显示到第 i 字"

### 跟练清单(放extra/)

- extra_typewriter_cursor.tsx:在打字机末尾加一个闪烁光标(纯 CSS 动画或 state 切换),并在文本打完后隐藏光标,练习细节打磨。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 打字机效果 / 定时器 / useEffect 清理 | MDN setInterval/rAF;Chrome 中文实操 | TypewriterText.tsx | 打字机效果、setInterval/rAF、useState/useEffect、清理函数、TS 类型 |

【超前】标注集中区:本日无超前内容(流式增长的文本明天叠加,今天是固定文本打字机)。
硬约束复查:仅用 day65 闭包知识点 + 既有前端能力 ✓ TS 类型完整 ✓ key 不硬编码(本日不涉及模型调用)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day66(周三,7h)· 流式 Markdown 增量渲染

AI 回答往往带 Markdown(标题/列表/代码块)。今天让 Markdown 在流式到达时"边收边渲染",而不是等全文到齐。核心是把每次到达的分块累积进一个字符串状态,再用 Markdown 解析库整体重渲染——React 的声明式重渲染天然适配"增量累积"。产出:StreamMarkdown.tsx,接收不断增长的文本并实时渲染为富文本。

💡 前端开发者速读:流式 Markdown ≈ "累积 buffer + 每帧重新解析渲染"。你已会受控 state 驱动重渲染,这里只是让 state 随分块增长;Markdown 解析交给成熟库(如 react-markdown),你不必手写解析器。要注意的坑:流式过程中 Markdown 可能"半截"(如 ``` 代码块只来了一半),库要能容错渲染;高频 setState 可能需要节流(综合日再优化)。

### 学习内容

- 增量累积模式:`setMd(prev => prev + chunk)`,state 随分块增长
- 用 Markdown 解析库(如 react-markdown)把累积文本渲染为富文本
- 流式期间"半截 Markdown"的容错渲染(未闭合代码块/加粗等)
- 高频更新下的渲染开销与节流直觉(认知,深入优化留综合日/后续)
- 与打字机的关系:打字机控制"出现节奏",Markdown 控制"呈现格式",二者可叠加

### 讲解

结论先行:流式 Markdown 的心智是"把到达的分块不断拼进一个累积字符串,然后整体交给 Markdown 库渲染"。你不需要增量解析每个 token——React 会在 state 变化时重渲染,Markdown 库对当前累积文本整体解析即可。要点是容错:流式中途 Markdown 常常不完整(代码块只来一半),选用的库要能对残缺语法优雅降级而非报错。

```tsx
// 每收到新分块就 append 到累积文本,再整体重新解析渲染
const [md, setMd] = useState("");
function onChunk(chunk: string) {
  setMd((prev) => prev + chunk);   // 增量累积
}
// 渲染:用 Markdown 解析库把当前累积文本转成组件树
return {md};
// 关键:流式期间每次 setState 都触发重渲染,天然形成"边收边渲染"
```

### 教材与章节

- 主教材/官方文档:react-markdown 官方仓库(README 用法):(https://github.com/remarkjs/react-markdown) ;MDN 渲染性能(中文,认知节流):(https://developer.mozilla.org/zh-CN/docs/Web/API/Performance) ;检索词"流式 Markdown 增量渲染 React"、"react-markdown 流式 未闭合代码块"。
- 实操参考(A级):Chrome 中文 Prompt UI / ai-elements(含流式消息渲染):(https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn) 。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 增量累积模式、Markdown 解析库、半截语法容错、渲染开销 精读+实验 |
| 练习 | 2h | 编写固定产物 StreamMarkdown.tsx + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 react-markdown 英文 README |
| 输出 | 1h | GitHub commit;把"流式 Markdown 容错"整理进博客素材 |
| 复盘 | 0.5h | 补 index.md、自检类型完整、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day66/StreamMarkdown.tsx:流式 Markdown 渲染组件(≤120行)
  - 组件维护一个随分块增长的累积文本 state,提供一个接收新分块的入口(回调或 props)
  - 用 Markdown 解析库(如 react-markdown)把累积文本实时渲染为富文本
  - 用 TS 为 props/分块建类型;能在流式中途对"未闭合代码块/半截语法"容错渲染不崩溃
  - 输入:一串按时间到达的分块(可用 day64 的 mock 流或本地定时模拟);输出:页面上 Markdown 随分块逐步成型
  - 必须覆盖行为:分块累积正确、含标题/列表/代码块的样例能正确渲染、残缺语法不报错;每步有可见渲染结果
  - 所用知识点清单:流式渲染、流式 Markdown 增量渲染、React useState、Markdown 解析库、TS 类型;承接 day64 流接收
- [ ] 补记 学习产物/第10周/day66/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会受控 state 驱动重渲染 → 新用法:让 state 随流式分块增长,天然"边收边渲染"
- 你已会用第三方 UI/解析库 → 新用法:用 react-markdown 渲染,不手写解析器
- 你已会防抖/节流 → 新用法:高频分块下控制渲染频率(认知,深入优化后续)
- 你已会容错 UI(边界降级)→ 新用法:流式半截 Markdown 优雅降级不崩

### 跟练清单(放extra/)

- extra_md_throttle.tsx:给 StreamMarkdown 的累积更新加一个简单节流(如每 100ms 合并一次渲染),对比节流前后页面流畅度,记录结论到 index.md。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 流式 Markdown 增量渲染 / 容错 | react-markdown 官方;Chrome 中文实操 | StreamMarkdown.tsx | 流式渲染、流式 Markdown、useState、Markdown 库、TS 类型、day64 流承接 |

【超前】标注集中区:本日无超前内容(工具调用可视化/生成式 UI 属第11-12周,今天只渲染文本 Markdown)。
硬约束复查:仅用 day66 闭包知识点 + 既有前端能力 ✓ TS 类型完整 ✓ key 不硬编码(用 mock/代理)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day67(周四,7h)· 中断控制:AbortController

AI 回答有时很长或跑偏,用户需要"停止生成"。今天实现流式接收的中断——用 AbortController 给 fetch 流挂一个信号,用户点停止就 abort,reader 立刻断开并抛 AbortError,你要正确识别并收尾。产出:useAbortStream.ts,一个可中断的流式接收 hook。

💡 前端开发者速读:中断 ≈ 你已会的 `AbortController` + `fetch(url, {signal})`——这套你在取消普通请求时用过;新场景是"取消一个正在持续 yield 的流":abort 后 `reader.read()` 会以 AbortError 拒绝,记得区分"主动中断"与"真错误"(靠 `err.name === 'AbortError'`),别把用户主动停止当成异常报红。EventSource 没有 abort,只能 close(这也是为什么 AI 流式主力用 fetch 流)。

### 学习内容

- AbortController/AbortSignal 用法,给 fetch 挂 signal
- 中断后 reader.read() 抛 AbortError 的识别(err.name)与收尾
- "主动中断" vs "真实错误"的区分处理
- 把中断能力封装进 hook,对外暴露 start/stop 与流式状态(idle/streaming/aborted/done)
- EventSource.close() 与 fetch abort 的差异

### 讲解

结论先行:中断的标准做法是——发起 fetch 时传入 `controller.signal`,需要停止时调用 `controller.abort()`;此时进行中的 `read()` 会抛出名为 `AbortError` 的异常。你必须在 catch 里判断 `err.name === 'AbortError'` 走"已停止"分支,而不是当成网络错误。把 controller 存在 ref 里,让"发送"和"停止"两个动作共享同一个 controller,是封装 hook 的关键。

```ts
const controller = new AbortController();
try {
  const res = await fetch("/mock-sse", { signal: controller.signal });
  const reader = res.body!.getReader();
  // ...循环 read() 消费流
} catch (err) {
  if ((err as Error).name === "AbortError") {
    console.log("用户主动中断,正常收尾");
  } else {
    console.error("真实错误:", err);
  }
}
// 用户点"停止":controller.abort();  // 立刻断开流
```

### 教材与章节

- 主教材/官方文档:MDN AbortController(中文):(https://developer.mozilla.org/zh-CN/docs/Web/API/AbortController) ;MDN AbortSignal(中文):(https://developer.mozilla.org/zh-CN/docs/Web/API/AbortSignal) ;检索词"AbortController 取消 fetch 流 AbortError"、"SSE 中断 停止生成 前端"。
- 预读(A级):Vercel AI SDK 官方文档(useChat 的 stop 能力,第11周正式用):(https://ai-sdk.dev/docs/introduction) 。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | AbortController/Signal、AbortError 识别、状态机封装 精读+实验 |
| 练习 | 2h | 编写固定产物 useAbortStream.ts + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 MDN AbortController 英文文档 |
| 输出 | 1h | GitHub commit;把"中断=AbortError 别误报"整理进博客素材 |
| 复盘 | 0.5h | 补 index.md、自检类型完整、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day67/useAbortStream.ts:可中断的流式接收 hook(≤120行)
  - 封装一个 hook,发起可中断的 fetch 流接收,内部用 AbortController;对外暴露 start/stop 与流式状态(idle/streaming/aborted/done)
  - 中断后正确识别 AbortError 并走"已停止"分支,与真实网络错误区分处理
  - 用 TS 为状态(联合类型)与返回值建类型,不用 any
  - 输入:mock SSE 地址;输出:控制台/状态可观察到"接收中→用户中断→已停止"的完整流转
  - 必须覆盖行为:接收途中调用 stop 能立刻断开、中断不误报为错误、组件卸载时自动 abort 防泄漏;每步有可见反馈
  - 所用知识点清单:中断控制、AbortController/AbortSignal、fetch + ReadableStream(承接 day64)、TS 联合类型/状态机、错误处理;前端不含 key
- [ ] 补记 学习产物/第10周/day67/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会用 AbortController 取消普通请求 → 新用法:取消一个正在持续 yield 的流式响应
- 你已会 try/catch 错误分流 → 新用法:靠 `err.name === 'AbortError'` 区分"主动停止"与"真错误"
- 你已会 useRef 存可变实例 → 新用法:用 ref 持有 controller,让 send/stop 共享同一个
- 你已会 EventSource.close() → 对比:close 只断连接,fetch abort 才是真取消(故 AI 流式主力用 fetch)

### 跟练清单(放extra/)

- extra_stop_button.tsx:给 useAbortStream 配一个最小 UI——"开始接收/停止"两个按钮 + 状态文字(idle/streaming/aborted/done),直观验证中断链路。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 中断控制 / AbortController / AbortError | MDN AbortController/AbortSignal | useAbortStream.ts | 中断控制、AbortController/Signal、fetch 流、TS 联合类型、错误处理 |

【超前】标注集中区:本日无超前内容(useChat 的 stop 属第11周,今天用原生 AbortController 实现同等能力)。
硬约束复查:仅用 day67 闭包知识点 + 既有前端能力 ✓ TS 类型完整 ✓ key 不硬编码(mock/代理)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day68(周五,7h)· 自定义 hook 整合:useStreamChat

今天把前三天(SSE 接收 + 打字机 + 流式 Markdown + 中断)拧成一个可复用 hook:useStreamChat。它对外只暴露"消息列表 + 流式状态 + send/stop",内部封装流接收、分块累积、中断与清理——这是综合日和第11周接 useChat 的自研对照底座。产出:useStreamChat.ts。

💡 前端开发者速读:useStreamChat ≈ 你写过的自定义 hook 封装(如 useFetch),只是内部消费的是"持续到达的流"而非一次性响应。状态设计是重点:一个消息数组,最后一条消息带 `streaming` 标记;send 时新建一条流式消息并起流,每到一个分块就更新它的文本;stop 时 abort。第11周 Vercel AI SDK 的 useChat 会把这套封装成开箱即用的官方 hook——今天先自己实现一遍,明天你就懂它替你做了什么。

### 学习内容

- 自定义 hook 的封装边界:对内藏流细节,对外给简洁 API(messages/loading/send/stop)
- 消息状态建模:消息数组 + 每条的 streaming 标记(用 TS 类型描述)
- 整合 day64(流接收)+ day67(中断)+ 为 day66(Markdown)/day65(打字机)供数据
- 分块累积进"当前流式消息"的更新方式(函数式 setState)
- key 安全:hook 只连后端代理/mock,不碰大模型 key

### 讲解

结论先行:整合的关键是"清晰的状态模型 + 明确的职责边界"。useStreamChat 内部持有消息数组与一个 AbortController,`send` 负责新建流式消息并启动 fetch 流、把每个分块累积进这条消息,`stop` 负责 abort。对外只暴露 messages/loading/send/stop,消费者不关心 SSE 细节。这样第11周换成官方 useChat 时,你的组件几乎不用改——因为你早已按同样的抽象在用它。

```ts
type Msg = { role: "user" | "ai"; text: string; streaming?: boolean };
function useStreamChat(url: string) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const ctrl = useRef(null);
  async function send(input: string) {
    ctrl.current = new AbortController();
    setMessages((m) => [...m, { role: "user", text: input },
                              { role: "ai", text: "", streaming: true }]);
    setLoading(true);
    // 起 fetch 流,把每个分块累积进最后一条 ai 消息;结束/中断时收尾
    setLoading(false);
  }
  return { messages, loading, send, stop: () => ctrl.current?.abort() };
}
```

### 教材与章节

- 主教材/官方文档:MDN 自定义 hook 相关以 React 官方为准,检索词"React 自定义 hook useStreamChat 流式"、"React 大模型 打字机 流式渲染";fetch 流复习 MDN ReadableStream:(https://developer.mozilla.org/zh-CN/docs/Web/API/ReadableStream) 。
- 预读(A级):Vercel AI SDK 官方文档 useChat(第11周正式用,今天作对照):(https://ai-sdk.dev/docs/introduction) ;检索词"useChat 教程"。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 自定义 hook 封装、消息状态建模、流/中断整合 精读+设计 |
| 练习 | 2h | 编写固定产物 useStreamChat.ts + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Vercel AI SDK 英文 useChat 文档(对照) |
| 输出 | 1h | GitHub commit;把"自研 useStreamChat vs 官方 useChat"整理进博客素材 |
| 复盘 | 0.5h | 补 index.md、自检类型完整、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day68/useStreamChat.ts:流式对话整合 hook(≤120行)
  - 封装 useStreamChat(url),内部整合 day64 流接收 + day67 中断;对外暴露 messages、loading、send、stop
  - 用 TS 为消息(role/text/streaming)与返回值建类型;send 新建流式消息并把分块累积进去,结束/中断时收尾清理 streaming 标记
  - stop 通过内部 AbortController 中断当前流;hook 卸载时自动 abort
  - 输入:后端代理/mock 的流地址 + 用户输入;输出:可被组件消费的消息列表与流式状态(前端不含 key)
  - 必须覆盖行为:连续 send 多条不串流、stop 生效、loading 状态正确切换、类型完整无 any;每步有可观察状态
  - 所用知识点清单:流式渲染整合、TS SSE/fetch 流(day64)、中断控制(day67)、打字机/流式 Markdown 供数(day65-66 承接)、自定义 hook、TS 类型建模
- [ ] 补记 学习产物/第10周/day68/index.md:覆盖全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会封装 useFetch 类自定义 hook → 新用法:封装 useStreamChat,消费"持续流"而非一次性响应
- 你已会函数式 setState(`setX(prev=>...)`)→ 新用法:把分块累积进"最后一条流式消息"
- 你已会 useRef 持有可变对象 → 新用法:用 ref 持有 AbortController 供 send/stop 共享
- 你已会设计对外简洁 API → 新用法:messages/loading/send/stop,正是第11周官方 useChat 的形态

### 跟练清单(放extra/)

- extra_multi_session.ts:给 useStreamChat 增加"多会话"雏形——用一个 Map/数组按 sessionId 存不同会话的消息,练习状态组织(为第11周会话状态管理预热)。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 自定义 hook 整合流式对话 | MDN ReadableStream;Vercel AI SDK useChat 对照 | useStreamChat.ts | 流式整合、fetch 流、中断、自定义 hook、消息状态建模、TS 类型 |

【超前】标注集中区:本日出现"多会话状态管理雏形"(extra)属【超前】预热,会话状态管理第11周首教,仅识别不深入。
硬约束复查:仅用 day68 闭包知识点 + 既有前端能力 ✓ TS 类型完整 ✓ key 不硬编码(连代理/mock)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day69(周六,7h)· 综合项目实战:流式对话三要素 demo

今天是项目日,把整周能力组装成一个可对外演示的流式对话组件:发消息→AI 回答逐字打字机浮现→带 Markdown 格式→可随时点"停止"中断。这是骨架第10周的固定产物"React 流式渲染 demo(打字机+流式 Markdown+中断)",也是本周闸门的直接预演。产出:StreamChatDemo.tsx。

💡 前端开发者速读:这就是你熟悉的"容器组件 + 若干展示组件"组合——容器用 useStreamChat 管状态,展示层复用 TypewriterText/StreamMarkdown,停止按钮接 stop。心智上等价于你搭过的一个小型聊天界面,只是数据源是流。重点在"三要素同时在线"时的协调:打字机控节奏、Markdown 控格式、中断控终止,别让它们互相打架(如中断后打字机要停在当前文本)。

### 学习内容(综合复用,少量新整合)

- 容器/展示组件分层:容器持 useStreamChat,展示层复用前几日组件
- 三要素协调:流式 Markdown 承载格式,打字机承载出现节奏,中断承载终止
- 输入框 + 发送/停止按钮 + 消息列表的最小聊天 UI
- 边界:空输入、发送中禁用、中断后状态复位
- key 安全:数据源为后端代理/mock,前端零 key

### 讲解

结论先行:综合日的重点是"组装与协调",不是新 API。容器组件调用 useStreamChat 拿到 messages/loading/send/stop,把每条 ai 消息交给 StreamMarkdown(格式)+ 打字机节奏渲染,发送/停止按钮分别接 send/stop。要特别处理三要素叠加时的边界:中断后打字机应停在已到达文本、loading 复位、可再次发送。把它当作你搭过无数次的聊天 UI,数据源换成流即可。

```tsx
export default function StreamChatDemo() {
  const { messages, loading, send, stop } = useStreamChat("/mock-sse");
  const [input, setInput] = useState("");
  return (
    
      {messages.map((m, i) => (
        
      ))}
       setInput(e.target.value)} />
       send(input)}>发送
      {loading && 停止}
    
  );
}
```

### 教材与章节

- 主教材/官方文档:MDN ReadableStream / AbortController(复习,中文):(https://developer.mozilla.org/zh-CN/docs/Web/API/ReadableStream) ;检索词"React 流式对话 组件 打字机 Markdown 中断 实战"。
- 实操参考(A级):Chrome 中文 Prompt UI / ai-elements(流式对话 UI 范式):(https://developer.chrome.google.cn/blog/prompt-ui-ai-elements-with-vercel-ai?hl=zh_cn) ;Vercel AI SDK 文档(对照):(https://ai-sdk.dev/docs/introduction) 。

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画组件分层、想清三要素协调与边界(中断/loading/空输入) |
| 项目实战 | 3h | 编写 StreamChatDemo.tsx(整合本周全部能力) |
| 英语 | 0.5h | AI 辅助精读 Chrome 中文/英文实操文档 |
| 输出 | 1h | GitHub commit;把 demo 录屏/截图整理为差异化叙事素材 |
| 复盘 | 0.5h | 补 index.md、自检类型完整与闭包、列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第10周/day69/StreamChatDemo.tsx:流式对话三要素 demo(项目日,≤150行)
  - 容器组件复用 useStreamChat(day68),展示层复用 StreamMarkdown(day66)与打字机节奏(day65),中断接 stop(day67)
  - 提供输入框 + 发送按钮 + (发送中)停止按钮 + 消息列表;AI 回答逐字浮现且带 Markdown 格式
  - 用 TS 为组件 props/消息建类型;处理边界:空输入拦截、发送中禁用发送、中断后打字机停在当前文本且 loading 复位
  - 数据源为后端代理或本地 mock SSE,前端不含任何大模型 key
  - 必须覆盖行为:三要素(打字机/流式 Markdown/中断)现场均可演示、连续多轮不串流、`npm run dev` 可跑通展示;每步有可见 UI 反馈
  - 所用知识点清单:打字机效果、流式 Markdown 渲染、中断控制、TS SSE/fetch 流、自定义 hook 整合(day64-68 全部)、React 组件分层、TS 类型
- [ ] 补记 学习产物/第10周/day69/index.md:覆盖设计思路与全部学习内容

### 既有前端能力 → AI集成新用法(对照笔记)

- 你已会容器/展示组件分层 → 新用法:容器管流式状态,展示层复用打字机/Markdown 组件
- 你已会搭聊天 UI(输入/列表/按钮)→ 新用法:数据源从"一次性响应"换成"持续流"
- 你已会表单边界处理(禁用/校验)→ 新用法:发送中禁用、空输入拦截、中断后复位
- 你已会组件组合与 props 类型 → 新用法:三要素叠加时明确各自职责,避免互相干扰

### 跟练清单(放extra/)

- extra_auto_scroll.tsx:给 StreamChatDemo 加"流式输出时自动滚动到底部"的体验优化(监听消息增长滚动容器),练习流式场景下的交互细节。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 三要素综合(打字机+流式 Markdown+中断) | MDN 复习;Chrome 中文实操;Vercel AI SDK 对照 | StreamChatDemo.tsx | 打字机、流式 Markdown、中断、fetch 流、hook 整合、组件分层、TS 类型 |

【超前】标注集中区:本日无超前内容(工具调用可视化/生成式 UI/组件库级封装属第11-12周)。
硬约束复查:仅用 day69 闭包知识点 + 既有前端能力 ✓ TS 类型完整 ✓ key 不硬编码(代理/mock)✓ 项目日 ≤150行 ✓ extra 命名正确 ✓

---

## Day70(周日,7h)· 周检测 + 对账

今天是本周闸门。目标是限时独立完成一个流式渲染 demo,验证"SSE 接收 + 打字机 + 流式 Markdown + 中断"已内化为肌肉记忆。通过后即可平稳进入第11周(Vercel AI SDK / LangChain.js / 工具调用可视化)——届时你会发现官方 useChat 替你封装的,正是本周手写的这套东西。

### 周检测(限时任务)

任务:45分钟内,不看教材、不看本周产物,独立盲写 学习产物/第10周/day70/StreamDemoCheck.tsx:

1. 连接一个流式数据源(本地 mock SSE 服务或后端代理;前端不含任何大模型 key),类型化地逐块接收文本。
2. 实现打字机效果:AI 回答逐字浮现,而非整段闪现。
3. 实现流式 Markdown 渲染:回答中的标题/列表/代码块随分块增量成型,半截语法不崩溃。
4. 实现中断控制:提供"停止"入口,点击后立刻断开流并正确收尾(不误报为错误)。
5. 提供最小交互:一个发送入口触发一次流式回答,消息以列表呈现。
6. 全流程 TS 类型完整(消息/状态/props 有类型,无 any 兜底),`npm run dev` 可跑通并现场演示三要素。

通过标准(须全部满足):

- 45分钟内完成,项目能跑通、无未捕获异常,三要素(逐字打字机 / 流式 Markdown / 可中断)均可现场演示;
- TS 类型完整(关键数据结构与 props 有类型,无 any 兜底);
- 前端不硬编码任何大模型 key(数据经 mock/后端代理,或 key 由服务端/环境变量注入);
- 仅用截至 day70 的闭包知识点(本周新增首教 + 前九周已学 + 既有前端能力),第三方库仅限已装的 Markdown 解析等前端包;
- ≤180 行(周末检测放宽)。

未通过补救方案:

- 仅个别 API 用法或类型写错 → 当天用缓冲 1h 对照 Day64/Day67 讲解订正,次日重盲写一次(≤45min);
- 三要素某一项(如中断或流式 Markdown)不通 → 重做对应 Day66/Day67,再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第11周前 2 天先补流式渲染欠账,再进入 Vercel AI SDK/useChat,闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项✅/❌/⚠️):
   - day64/sseClient.ts ☐ day64/extra/extra_stream_to_dom.ts ☐ day64/index.md ☐
   - day65/TypewriterText.tsx ☐ day65/extra/extra_typewriter_cursor.tsx ☐ day65/index.md ☐
   - day66/StreamMarkdown.tsx ☐ day66/extra/extra_md_throttle.tsx ☐ day66/index.md ☐
   - day67/useAbortStream.ts ☐ day67/extra/extra_stop_button.tsx ☐ day67/index.md ☐
   - day68/useStreamChat.ts ☐ day68/extra/extra_multi_session.ts ☐ day68/index.md ☐
   - day69/StreamChatDemo.tsx ☐ day69/extra/extra_auto_scroll.tsx ☐ day69/index.md ☐
   - day70/StreamDemoCheck.tsx(检测产物)☐
   - package.json / 依赖(Markdown 解析库等本周所用 npm 包)☐
2. 填 README 进度跟踪表:完成% / 自评 1-5 / 卡点 / 补救。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第11周前 2 天改补欠账。
4. 验收:每个组件/hook 必须能在本地 `npm run dev` 跑通并演示;确认前端源码中无任何硬编码 key(全局检索一遍)。

## 周尾附录:完整知识点累计清单(截至第10周day70)

第01-09周(已有):Python 全栈(基础语法/控制流/数据结构、函数与模块、OOP、文件读写、异常全体系、venv/pip/requirements、requests、正则 re、typing、asyncio);大模型 API 调用、环境变量读 key、Chat API、Prompt 工程、JSON Mode、流式 Streaming、Function Calling、多轮上下文;LangChain/LCEL、向量数据库(Chroma/Milvus/Faiss)、RAG 全链路、Dify/Coze 入门;引用标注、rerank 重排、RAG 评测方法;Agent、Tool、Memory、ReAct、LangGraph 入门、MCP(认知)。既有前端能力:10 年 JS/TS/React(组件/hooks/状态/类型系统/fetch/EventSource/Webpack/RN)。

第10周(本周新增):

- TS SSE:EventSource(GET-only、自动重连)、fetch + ReadableStream(getReader + TextDecoder 逐块解码)、用 TS 为分块/消息类型化、两种方式的取舍
- 流式渲染:流式 Markdown 增量渲染(累积 buffer + 整体重解析、半截语法容错)、中断控制(AbortController/AbortSignal、AbortError 识别、主动中断 vs 真错误)、自定义 hook 整合(useStreamChat:messages/loading/send/stop)
- 打字机效果:游标推进 + slice 截取、setInterval/rAF、useEffect 清理防泄漏防串字、速度可控
- 【超前】识别项(不要求掌握):会话状态管理雏形(多会话,第11周首教);Vercel AI SDK useChat(第11周正式教,本周作对照预读)

下周预告(第11周day71-77):Vercel AI SDK(useChat 开箱即用的流式对话 hook)、LangChain.js(前端侧链式调用)、工具调用可视化(把工具名/入参/结果渲染为可见 UI)、会话状态管理;并同步完成简历改版(诚信修正:真实头衔 + 业务描述 + AI 项目置顶)。据主计划,Vercel AI SDK/LangChain.js 为差异化自选加分项(暂无权威 JD 一手佐证),面试以"生产级 AI 交互体验交付能力"陈述。
