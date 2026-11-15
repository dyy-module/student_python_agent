# 第07周 · RAG 全链路 + LangChain/LCEL + 向量数据库 + Dify/Coze 入门

> 与主计划的差异说明:本周严格对应修订版路线图「阶段3前段」(17周映射第07周),是 RAG 与 Agent 工程化的起点。据 2026 市场修订版,RAG + 向量库(Milvus/Chroma/Faiss)是 AI 应用岗 JD 的硬门槛技能,国产大模型优先(通义千问/DeepSeek/GLM);主题为 LangChain、LCEL、向量数据库、RAG 全链路(加载→切分→向量化→检索→生成)、Dify/Coze 入门,均与 reference 日程表第07周首教项完全一致。Day22 第三方库解禁点已过,本周在 venv 内 pip 安装 langchain/chromadb 等并写入 requirements.txt。闸门为 day49 周检测(命令行独立跑通最小 RAG 问答闭环)。据主计划第七节执行规范,每日 7h;据备案提醒,国内可访问 demo 需备案(周期 2-4 周),本周(RAG 阶段)即提交。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第07周/dayN/.py;跟练统一命名 extra_*.py 放入 学习产物/第07周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。

## 本周概览

- 主题:用 LangChain/LCEL 组织大模型调用链,跑通"文档加载→切分→向量化→检索→生成"的 RAG 全链路,并用 Dify/Coze 低代码平台快速产出一个可对外展示的知识库问答作品。
- 为什么对拿 offer 有用:RAG 是 AI 应用岗招聘中最高频的能力项(JD 硬门槛),直接对应作品集旗舰项目1"商品知识库导购问答";LangChain 是把 Chain/Agent/Tool 组织起来的通用框架(第09周 Agent、第13周服务化都建立在它之上);向量数据库(Milvus/Chroma/Faiss)几乎是所有 RAG/知识库 JD 的必写关键词。本周产出的最小 RAG 闭环,就是项目1 的技术雏形。
- 教材使用策略:主教材 尚硅谷 LangChain 从入门到实战(A级,含 RAG 综合案例)(50%)+ LangChain/Chroma 官方文档速查(30%)+ Datawhale LLM 入门教程补概念(20%)。凡涉及大模型调用,一律用国产模型(通义千问/DeepSeek/GLM)且 api_key 从环境变量读取。低代码部分以 Dify/Coze 官方文档 + 动手为主。
- 本周结束时应能做到:
  1. 用 LangChain 封装国产大模型,用 ChatPromptTemplate + 输出解析器,借 LCEL 的 `|` 管道把"提示→模型→解析"串成一条可 invoke 的链。
  2. 用文本加载器读入本地文档,用 text splitter 按 chunk_size/overlap 切分成片段。
  3. 用 embedding 把片段向量化并存入 Chroma 本地库,再用 retriever 按相似度做 topK 检索。
  4. day49 闸门:45分钟内独立盲写一个"加载→切分→向量化→检索→拼进提示→调国产大模型生成答案"的最小 RAG 问答程序。

## 前置知识点闭包(截至第06周已学,本周可直接用)

基础类型(int/float/str/bool/None)、print/input、f-string、控制流(if/elif/else、for/while/range/enumerate/break/continue)、字符串切片与方法、list/tuple/dict/set、推导式、切片进阶、生成器表达式、random、datetime;def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念;OOP(class/__init__/self、继承/重写/super/多态、魔术方法、isinstance/type)、文件读写(open/with/模式/encoding)、异常全体系(try/except/else/finally、raise、自定义异常);venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio;大模型 SDK 调用、环境变量读 key(零硬编码)、Chat API、Prompt 工程、结构化输出 JSON Mode;流式 Streaming、Function Calling、多轮上下文管理。

本周新增(首教):LangChain、LCEL、向量数据库(Chroma/Milvus/Faiss)、RAG 全链路(加载→切分→向量化→检索→生成)、Dify/Coze 入门。

【超前】预警:重排 rerank、引用标注、RAG 评测方法(命中率/召回)第08周首教;Agent、Tool、Memory、ReAct、LangGraph、MCP 第09周首教;混合检索、Agentic RAG、生成式 UI 等本周均不深入。若本周产物偶尔触及相关概念,仅以【超前】最小片段出现并标注(见 Day48 引用雏形)。

---

## Day43(周一,7h)· LangChain 与 LCEL 基础:模型封装 / PromptTemplate / 输出解析器 / `|` 管道

今天正式进入阶段3。前两周你已能裸调国产大模型 API、写 Prompt、拿 JSON 输出;今天把它们用 LangChain 组织起来——不再手写 requests 拼请求体,而是用统一组件(模型/提示模板/解析器)搭一条"链"。核心是 LCEL:用 `|` 把组件像管道一样串起来。产出:一条最小问答链 langchain_hello.py,输入一个主题,输出模型一句话解释。

💡 JS开发者速读:LangChain 的 Chain ≈ 你熟悉的函数管道 / Promise 链(`f(g(x))` 或 `.then().then()`);LCEL 的 `|` 管道 ≈ RxJS 的 pipe/组合操作符,或 Unix shell 的 `|`——数据从左流到右,每个组件处理一段。ChatPromptTemplate ≈ 模板字符串 + 变量占位;输出解析器 ≈ 把响应 `res.data` 提取成你要的字符串/对象。心智模型可直接迁移,重点记 `|` 的组合语义。

### 学习内容

- LangChain 是什么、为什么用它(统一封装模型/提示/解析,而非裸调 API)
- 用 LangChain 封装国产大模型(通义千问/DeepSeek/GLM 任一;api_key 从环境变量读)
- ChatPromptTemplate:带变量占位的提示模板(from_template / from_messages)
- 输出解析器 StrOutputParser:把模型消息对象转成纯字符串
- LCEL 与 `|` 管道:prompt | model | parser 组合成 chain,用 invoke 调用

### 讲解

结论先行:LCEL 的精髓是"组件皆可被 `|` 串联"。提示模板负责填变量、模型负责生成、解析器负责把结果转成你要的类型;三者用 `|` 连成一条链后,一次 `invoke(输入字典)` 就会自动走完"填模板→调模型→解析"全流程。这与你写 `pipe(map, filter, reduce)` 或 `.then().then()` 是同一种组合思想,只是组件换成了 LLM 零件。切记:模型对象的 api_key 必须从环境变量读,绝不写进代码。

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# model = 你用 LangChain 封装的国产大模型(api_key=os.environ[...] 读,零硬编码)
prompt = ChatPromptTemplate.from_template("用一句话解释:{topic}")
chain = prompt | model | StrOutputParser()   # LCEL:| 把组件串成管道
print(chain.invoke({"topic": "向量数据库"}))  # 一次调用走完 填模板→模型→解析
```

### 教材与章节

- 主教材:尚硅谷 LangChain 从入门到实战(A级)— LangChain 基础与 LCEL 表达式语言章节:(https://www.atguigu.com/video/346/)
- 官方文档速查:LangChain Python 官方文档(LCEL / Prompt Template / Output Parsers):(https://python.langchain.com/) ;检索词"LCEL 管道 教程 中文"、"ChatPromptTemplate 用法"。
- 概念补充:Datawhale LLM 入门教程(A级)— 大模型应用与链式调用:(https://datawhalechina.github.io/llm-cookbook/)
- 模型接入(国产,api_key 环境变量):阿里云百炼通义千问 (https://help.aliyun.com/zh/model-studio/qwen-function-calling) ;DeepSeek (https://platform.deepseek.com/api-docs/zh-cn/) ;智谱 GLM (https://docs.bigmodel.cn/cn/guide/develop/http/introduction)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | LangChain 组件体系、LCEL `\|` 管道、PromptTemplate、输出解析器 精读+敲示例 |
| 练习 | 2h | 编写固定产物 langchain_hello.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 LangChain 官方英文文档(LCEL 章节) |
| 输出 | 1h | GitHub commit(冷启动累计 30+);把今天笔记整理为博客素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包合规、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第07周/day43/langchain_hello.py:LangChain 最小问答链(≤120行)
  - 在 venv 内 pip 安装 langchain 及所选国产模型对应的 langchain 集成包,并把依赖写入 requirements.txt
  - 用 LangChain 封装一个国产大模型(通义千问/DeepSeek/GLM 任一);api_key 必须用 os.environ 从环境变量读取,零硬编码
  - 用 ChatPromptTemplate 定义一个含至少一个变量占位的提示模板
  - 用 LCEL 的 `|` 把"提示模板 | 模型 | 输出解析器"串成一条链
  - 输入:一个主题字符串;输出:模型对该主题的一句话解释,print 出来
  - 必须覆盖行为:模板变量被正确填充、链的 invoke 调用成功、解析器把结果转为字符串、每步有 print(打印所用模型名、模板、最终回答)
  - 所用知识点清单:LangChain 模型封装、ChatPromptTemplate、LCEL(`|` 管道)、StrOutputParser、os.environ 读 key、print、f-string
- [ ] 补记 学习产物/第07周/day43/index.md:覆盖全部学习内容(代码块纯 Python 可运行,禁混 JS 语法)

### JS→Python对照笔记

- JS `f(g(x))` / Promise `.then().then()` → Python LCEL `prompt | model | parser` 再 `.invoke(x)`
- JS RxJS `pipe(map, filter)` → Python LCEL 用 `|` 组合可运行组件(Runnable)
- JS 模板字符串 `` `解释${topic}` `` → Python `ChatPromptTemplate.from_template("解释:{topic}")`
- JS `res.data.content` 手动取值 → Python `StrOutputParser()` 自动把消息转字符串
- JS `process.env.KEY` → Python `os.environ["KEY"]`(均零硬编码)

### 跟练清单(放extra/)

- extra_chain_two_steps.py:搭一条两级链——第一级让模型把一个主题扩写成三个关键词,第二级把关键词拼成一句广告语;体会 `|` 可以把任意多个组件串起来,每级 print 中间结果。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| LangChain 组件 / LCEL 管道 / PromptTemplate / 输出解析器 | 尚硅谷 LangChain-LCEL;官方文档 LCEL | langchain_hello.py | LangChain 模型封装、ChatPromptTemplate、LCEL(`\|`)、StrOutputParser、os.environ 读 key、print、f-string |

【超前】标注集中区:本日无超前内容(Agent/Tool/Memory 属第09周,不涉及)。
硬约束复查:仅用 day43 闭包知识点 ✓ 第三方库合规(langchain 在 venv 内、已写 requirements.txt)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day44(周二,7h)· 文档加载与切分:loader / text splitter / chunk_size 与 overlap

RAG 的第一步不是调模型,而是"喂对资料"。今天解决"怎么把一份长文档变成模型能吃下的小块"。为什么重要:大模型上下文有限,且检索要按片段命中,所以必须把文档切成合适大小的 chunk;切得太大检索不准、太小语义断裂。产出:doc_load_split.py,读入本地文档并按规则切分,打印片段数与首尾片段。

💡 JS开发者速读:text splitter ≈ 你写过的"按固定长度切字符串 + 保留重叠窗口"的逻辑(类似长列表分片渲染、把大文本分段懒加载);chunk_overlap ≈ 分片时前后留一点冗余,避免正好把一句话从中间切断。文档加载器 ≈ `fs.readFile` + 各种格式解析器(PDF/MD/TXT)的封装,你只需给它路径。

### 学习内容

- 文档加载器(Document Loader):从本地 txt/md 等读入原始文本
- 文本切分器(RecursiveCharacterTextSplitter 等)的作用与选型
- chunk_size(每块最大长度)与 chunk_overlap(相邻块重叠)的含义与调参直觉
- 切分结果的结构:一组 Document/字符串片段
- 为什么要切分(上下文限制 + 检索粒度)

### 讲解

结论先行:切分的本质是"在语义尽量完整的前提下,把长文分成可检索的小块"。chunk_size 控制每块大小,chunk_overlap 让相邻块共享一段文字以避免把关键句从中间切断。RecursiveCharacterTextSplitter 会优先按段落/句子等自然边界切,是通用首选。今天先不接模型,只把"读入→切分→打印观察"跑通,为明天向量化备好片段。

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
text = "很长的一段文档......"           # 由加载器从本地文件读入
splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,       # 每块最多约 100 字符
    chunk_overlap=20,     # 相邻块重叠 20 字符,避免语义被切断
)
chunks = splitter.split_text(text)
for i, c in enumerate(chunks):
    print(i, len(c), c[:20])   # 打印每块长度与开头,肉眼观察切分效果
```

### 教材与章节

- 主教材:尚硅谷 LangChain 从入门到实战(A级)— 文档加载与文本切分章节:(https://www.atguigu.com/video/346/)
- 官方文档速查:LangChain Python 官方文档(Document Loaders / Text Splitters):(https://python.langchain.com/) ;检索词"RecursiveCharacterTextSplitter chunk_size chunk_overlap 中文"。
- 概念补充:Datawhale LLM 入门教程(A级)— RAG 与文档处理:(https://datawhalechina.github.io/llm-cookbook/)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 文档加载器、text splitter、chunk_size/overlap 精读+调参实验 |
| 练习 | 2h | 编写固定产物 doc_load_split.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 LangChain 官方英文文档(Text Splitters 章节) |
| 输出 | 1h | GitHub commit;把"chunk 调参直觉"整理为博客素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包合规、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第07周/day44/doc_load_split.py:文档加载与切分器(≤120行)
  - 用文件读写(已学 open/with)或 LangChain 文档加载器读入一份本地文本文档(可先在程序内用 with open("w") 生成一份中英文混合的 sample 文档,保证文件必存在)
  - 用文本切分器按设定的 chunk_size 与 chunk_overlap 把文档切成若干片段
  - 输入:本地文档路径 + 切分参数;输出:打印片段总数、每个片段的长度、首片段与尾片段的内容
  - 必须覆盖行为:切分参数可调(至少演示两组不同 chunk_size 的效果并对比片段数)、每步有 print、片段内容非空校验
  - 所用知识点清单:文档加载与切分(RAG 全链路第一步)、chunk_size/chunk_overlap、open/with、encoding、for、enumerate、len、print、f-string
- [ ] 补记 学习产物/第07周/day44/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `fs.readFileSync(p,'utf8')` → Python `with open(p, encoding='utf-8') as f: f.read()` 或 LangChain loader
- JS 手写 `text.slice(i, i+n)` 分片 → Python `RecursiveCharacterTextSplitter.split_text(text)`
- JS 分片留重叠(冗余窗口) → Python `chunk_overlap` 参数
- JS 数组 `.map/.forEach` → Python `for i, c in enumerate(chunks):`

### 跟练清单(放extra/)

- extra_chunk_tune.py:对同一段文档分别用 chunk_size=50/100/200(overlap 固定 20)切分,打印三组的片段数与平均片段长度,观察参数对切分粒度的影响。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| 文档加载 / text splitter / chunk_size 与 overlap | 尚硅谷 LangChain-文档切分;官方 Text Splitters | doc_load_split.py | 文档加载与切分、chunk_size/overlap、open/with、for、enumerate、len、print |

【超前】标注集中区:本日无超前内容(向量化/embedding 明天首教,今天只切分不向量)。
硬约束复查:仅用 day44 闭包知识点 ✓ 第三方库合规(langchain-text-splitters 在 venv 内、已写 requirements.txt)✓ key 零硬编码(本日不调模型,无 key)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day45(周三,7h)· 向量数据库与 embedding:Chroma 本地建库 / 存取

昨天把文档切成了片段,今天给片段"编码"并存起来。embedding 把一段文本变成一串数字(向量),语义相近的文本向量距离也近;向量数据库就是专门存这些向量并支持"按相似度查"的库。这是 RAG 的心脏,也是 JD 硬门槛关键词(Chroma/Milvus/Faiss)。产出:vector_store_build.py,把文档片段向量化并存入 Chroma 本地库,打印写入条数。

💡 JS开发者速读:embedding ≈ 把文本转成"可比较的特征向量"(类似推荐系统里把商品/用户转成 feature 向量算相似度);向量数据库 ≈ 语义版数据库——普通 DB 按字段精确匹配(`WHERE name='x'`),向量库按"意思有多接近"排序返回。Chroma 本地建库 ≈ 起了一个轻量的本地存储服务,`create_collection` 类似建表,`add` 类似 insert,你只需给文档和 id,它自动帮你算 embedding。

### 学习内容

- embedding(向量化)是什么:文本→向量,语义相近则向量相近
- embedding 模型的来源(国产模型/开源 embedding,api_key 环境变量读)
- 向量数据库三选一定位:Chroma(本地轻量,本周主用)/ Milvus(生产级)/ Faiss(库)
- Chroma 基本操作:创建客户端、create_collection、add(存文档+向量+id)、count
- 持久化 vs 内存库的区别

### 讲解

结论先行:向量库把"文本检索"变成"向量最近邻检索"。你存入文档时,Chroma 会用 embedding 模型把每段文本转成向量一并保存;查询时把问题也转成向量,再找距离最近的若干条。今天只练"建库 + 存入 + 确认条数",查询留到明天。embedding 模型若走国产 API,同样必须环境变量读 key。

```python
import chromadb
client = chromadb.Client()                 # 本地客户端(内存版;生产可换持久化)
col = client.create_collection("kb")        # 建一个集合(≈ 建表)
col.add(
    documents=["杭州是浙江省会", "西湖在杭州"],  # Chroma 自动生成 embedding
    ids=["d1", "d2"],                        # 每条必须有唯一 id
)
print(col.count())                           # 已存入的向量条数
```

### 教材与章节

- 主教材:尚硅谷 LangChain 从入门到实战(A级)— 向量数据库与 embedding 章节:(https://www.atguigu.com/video/346/)
- 官方文档速查:Chroma 官方文档(集合/存取/持久化):(https://docs.trychroma.com/) ;Milvus 官方文档(生产级向量库,认知):(https://milvus.io/docs/) ;检索词"Chroma 向量库 中文 教程"、"embedding 向量化 是什么"。
- 概念补充:Datawhale LLM 入门教程(A级)— 向量与语义检索:(https://datawhalechina.github.io/llm-cookbook/)
- embedding 模型接入(国产,api_key 环境变量):阿里云百炼 (https://help.aliyun.com/zh/model-studio/qwen-function-calling)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | embedding 概念、Chroma 建库/存取、三种向量库定位 精读+实验 |
| 练习 | 2h | 编写固定产物 vector_store_build.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Chroma 官方英文文档 |
| 输出 | 1h | GitHub commit;把"向量库=语义检索"整理为博客素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包合规、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第07周/day45/vector_store_build.py:向量库建库与写入(≤120行)
  - 复用 day44 切分得到的片段(可在程序内重新读文档并切分,或直接内置几条示例片段)
  - 用 Chroma 创建本地集合,把片段向量化后写入,每条分配唯一 id
  - 若 embedding 走国产模型 API,api_key 必须用 os.environ 读取,零硬编码
  - 输入:一组文档片段;输出:打印成功写入的条数、集合名称、以及其中一条片段的向量维度(如可取)
  - 必须覆盖行为:写入前后用 count 对比、重复 id 的处理提示、每步有 print
  - 所用知识点清单:embedding、向量数据库(Chroma)、create_collection/add/count、文档切分(承接 day44)、os.environ 读 key、for、enumerate、print、f-string
- [ ] 补记 学习产物/第07周/day45/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS 建表/建索引 → Python `client.create_collection("kb")`
- JS `db.insert({...})` → Python `col.add(documents=[...], ids=[...])`
- JS `db.count()` → Python `col.count()`
- JS 把对象转 feature 向量 → Python embedding 模型把文本转向量
- JS 普通 DB 精确 `WHERE` → 向量库按相似度排序(明天 retriever 体现)

### 跟练清单(放extra/)

- extra_vector_persist.py:把 Chroma 从内存版换成持久化到本地目录,写入几条片段后重建客户端再读回,验证数据仍在,体会"持久化 vs 内存"的差别。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| embedding / Chroma 建库与存取 / 向量库定位 | 尚硅谷 LangChain-向量库;Chroma 官方文档 | vector_store_build.py | embedding、向量数据库(Chroma)、add/count、切分承接、os.environ 读 key、for、print |

【超前】标注集中区:本日无超前内容(混合检索/rerank 属第08周,今天只做单路向量存储)。
硬约束复查:仅用 day45 闭包知识点 ✓ 第三方库合规(chromadb 在 venv 内、已写 requirements.txt)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day46(周四,7h)· 检索:retriever / 相似度 / topK

库建好了,今天学"怎么查"。检索是 RAG 里决定质量的关键一步:把用户问题也向量化,在库里找最相似的 topK 个片段返回。产出:retriever_demo.py,输入一个查询,返回最相关的 K 个片段及相似度并打印。

💡 JS开发者速读:向量检索 ≈ 语义版的 `filter + sort + slice(0, K)`——但它不是按字段精确匹配,而是按"意思有多接近"打分排序,取前 K 条。retriever ≈ 你封装好的一个"查询函数",输入 query 输出相关文档数组;topK ≈ `.slice(0, K)`;相似度/距离 ≈ 排序的 score(注意有的库距离越小越相似,有的是相似度越大越相关,别搞反)。

### 学习内容

- retriever(检索器)的角色:把 query 转成向量并返回相关片段
- 相似度 / 距离的概念(距离越小越相似 or 相似度越大越相关)
- topK(n_results)参数的含义与取值直觉
- Chroma 的 query(query_texts / n_results)返回结构(documents/distances/ids)
- 检索结果如何为明天的"拼进 prompt"做准备

### 讲解

结论先行:检索就是"用问题去库里找最像的几段资料"。你把查询文本交给 retriever,它向量化后做最近邻搜索,返回 topK 个片段及其距离/相似度。K 太小可能漏关键信息、太大会引入噪声,通常 2-5 起步再调。今天只练"查得准不准",把命中片段打印出来肉眼判断,明天再把它们拼进提示交给模型作答。

```python
res = col.query(
    query_texts=["浙江的省会"],   # 用自然语言查询
    n_results=2,                   # topK=2,返回最相似的 2 条
)
print(res["documents"])            # 命中的文档内容
print(res["distances"])            # 距离越小越相似
print(res["ids"])                  # 命中片段的 id(明天做引用雏形用得上)
```

### 教材与章节

- 主教材:尚硅谷 LangChain 从入门到实战(A级)— 检索器与相似度检索章节:(https://www.atguigu.com/video/346/)
- 官方文档速查:Chroma 官方文档(query / n_results / distances):(https://docs.trychroma.com/) ;LangChain 官方文档(Retriever):(https://python.langchain.com/) ;检索词"向量检索 topK 相似度 中文"、"retriever as_retriever 用法"。
- 概念补充:Datawhale LLM 入门教程(A级)— 语义检索:(https://datawhalechina.github.io/llm-cookbook/)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | retriever、相似度/距离、topK、query 返回结构 精读+实验 |
| 练习 | 2h | 编写固定产物 retriever_demo.py + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Chroma 官方英文文档(query 章节) |
| 输出 | 1h | GitHub commit;把"topK 调参"整理为博客素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包合规、列卡点 |

### 当日产出

- [ ] 编写 学习产物/第07周/day46/retriever_demo.py:向量检索演示(≤120行)
  - 承接 day45:先建库并写入若干片段(或复用已持久化的集合)
  - 用 retriever / query 对一个自然语言查询做相似度检索,返回 topK 个片段
  - 输入:一个查询字符串 + K 值;输出:打印命中的 K 个片段内容、各自的相似度/距离、以及片段 id
  - 必须覆盖行为:演示不同 K(如 1 与 3)返回条数的差异、对"库里没有相关内容"的查询给出可辨识的打印、每步有 print
  - 所用知识点清单:检索器、相似度/距离、topK(n_results)、向量数据库(Chroma,承接 day45)、list 索引、for、print、f-string
- [ ] 补记 学习产物/第07周/day46/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `arr.filter(...).sort(byScore).slice(0,K)` → Python `col.query(query_texts=[q], n_results=K)`
- JS score 越大越靠前 → 向量库 distance 越小越相似(方向相反,注意)
- JS `res.hits.map(h=>h.text)` → Python `res["documents"]` / `res["ids"]`
- JS 取前 K → Python `n_results=K`(topK)

### 跟练清单(放extra/)

- extra_retriever_compare.py:对同一个查询分别取 K=1/3/5,打印三组命中片段,观察 K 增大时是否引入不相关内容,记录你的调参结论到 index.md。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| retriever / 相似度 / topK / query 返回结构 | 尚硅谷 LangChain-检索;Chroma 官方 query | retriever_demo.py | 检索器、相似度/距离、topK、Chroma、list 索引、for、print |

【超前】标注集中区:本日无超前内容(rerank 重排属第08周,今天只做单路向量检索,不做二次排序)。
硬约束复查:仅用 day46 闭包知识点 ✓ 第三方库合规(chromadb/langchain 在 venv 内、已写 requirements.txt)✓ key 零硬编码(若 embedding 走 API)✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day47(周五,7h)· RAG 全链路整合:检索增强生成(项目日)

今天是项目日,把这周四天拧成一条完整链路:加载→切分→向量化→检索→拼进提示→调国产大模型生成答案。这就是 RAG(检索增强生成),也是作品集项目1"商品知识库导购问答"的最小可运行内核。产出:rag_chain_qa.py,输入一个问题,基于本地文档检索后由国产模型作答。

💡 JS开发者速读:RAG ≈ "先 fetch 数据再 render",而不是让组件凭空渲染。模型本身不知道你私有文档的内容(就像后端不知道你数据库里有什么),所以要"先检索资料(retriever)→把资料塞进请求上下文(prompt)→再让模型基于资料回答"。整条链路 ≈ 你写过的 `query → 拼装 payload → 调接口 → 渲染`,只是中间多了"向量检索"这一步。

### 学习内容(综合复用,少量新整合)

- RAG 全链路的分层:检索层(day45-46)+ 生成层(day43 的 LCEL 链)
- 把 topK 检索片段拼成"上下文(context)"字符串
- 用带 context 与 question 两个变量的 ChatPromptTemplate 约束"仅根据资料回答"
- 用 LCEL 把 prompt | model | parser 串成生成链并 invoke
- key 安全:模型与 embedding 的 key 均环境变量读取

### 讲解

结论先行:RAG 的整合点是"把检索到的片段作为 context 注入提示,并要求模型只依据 context 作答"。这样模型回答的是"你的私有资料",而非凭空编造(降低幻觉)。结构上分两层:检索层负责找资料,生成层(昨天的 LCEL 链)负责基于资料作答。今天把两层接起来,就是最小 RAG 闭环——也是明天周检测要盲写的核心。

```python
context = "\n".join(hits)          # hits = retriever 返回的 topK 片段
prompt = ChatPromptTemplate.from_template(
    "仅根据资料回答,资料中没有就说不知道。\n资料:\n{context}\n问题:{question}"
)
chain = prompt | model | StrOutputParser()
answer = chain.invoke({"context": context, "question": q})
print(answer)   # 模型基于检索到的资料作答,而非凭空生成
```

### 教材与章节

- 主教材:尚硅谷 LangChain 从入门到实战(A级)— RAG 综合案例章节:(https://www.atguigu.com/video/346/)
- 官方文档速查:LangChain Python 官方文档(RAG / Retrieval QA):(https://python.langchain.com/) ;检索词"RAG 全链路 检索增强生成 中文 实战"。
- 概念补充:Datawhale LLM 入门教程(A级)— RAG 原理:(https://datawhalechina.github.io/llm-cookbook/)
- 模型接入(国产,api_key 环境变量):DeepSeek (https://platform.deepseek.com/api-docs/zh-cn/) ;智谱 GLM (https://docs.bigmodel.cn/cn/guide/develop/http/introduction) ;阿里云百炼 (https://help.aliyun.com/zh/model-studio/qwen-function-calling)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画 RAG 分层结构、想清"检索→拼 context→生成"的数据流 |
| 项目实战 | 3h | 编写 rag_chain_qa.py(整合本周四天能力) |
| 英语 | 0.5h | AI 辅助精读 LangChain 官方英文 RAG 文档 |
| 输出 | 1h | GitHub commit;把"最小 RAG 闭环"整理为项目1 README 素材 |
| 复盘 | 0.5h | 补 index.md、自检闭包合规、列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第07周/day47/rag_chain_qa.py:最小 RAG 问答(项目日,≤150行)
  - 完整链路:读入本地文档→切分→向量化写入 Chroma→对用户问题做 topK 检索→把命中片段拼成 context→用 LCEL 链调国产大模型基于 context 生成答案
  - 提示模板须约束"仅根据资料回答,资料中没有就说不知道",以降低幻觉
  - 模型与 embedding 的 api_key 均从环境变量读取,零硬编码
  - 输入:一个用户问题;输出:打印检索命中的片段(来源)、最终答案
  - 必须覆盖行为:检索为空时的兜底回答、每步有 print(切分数/命中数/答案)、python rag_chain_qa.py 一次跑通
  - 所用知识点清单:RAG 全链路(加载/切分/向量化/检索/生成)、LCEL(`|`)、ChatPromptTemplate、StrOutputParser、向量数据库(Chroma)、os.environ 读 key、字符串 join、for、print、f-string
- [ ] 补记 学习产物/第07周/day47/index.md:覆盖设计思路与全部学习内容

### JS→Python对照笔记

- JS `await fetch(...)` 拿数据再 render → Python 先 retriever 拿片段再交给生成链
- JS 拼 payload `{context, question}` → Python `chain.invoke({"context":..., "question":...})`
- JS 模板注入变量 → Python `ChatPromptTemplate.from_template("...{context}...{question}")`
- JS 多层 `.then()` 组装 → Python LCEL `prompt | model | parser`

### 跟练清单(放extra/)

- extra_rag_multi_q.py:在 rag_chain_qa 基础上,支持连续问多个问题(用已学 while/input 循环),每次复用同一个已建好的向量库,体会"建库一次、多次检索"的工程做法。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| RAG 全链路整合(检索增强生成) | 尚硅谷 LangChain-RAG 综合案例;官方 RAG | rag_chain_qa.py | RAG 全链路、LCEL、PromptTemplate、解析器、Chroma、os.environ 读 key、join、for、print |

【超前】标注集中区:本日无超前内容(引用标注/rerank/评测属第08周,今天只跑通"能答",不追求"标来源/排序优化/命中率")。
硬约束复查:仅用 day47 闭包知识点 ✓ 第三方库合规(langchain/chromadb 在 venv 内、已写 requirements.txt)✓ key 零硬编码 ✓ 项目日 ≤150行 ✓ extra 命名正确 ✓

---

## Day48(周六,7h)· Dify/Coze 低代码搭一个 RAG 问答(认知+动手)+ 引用雏形

今天换一种姿势做 RAG:不写链路代码,而是用低代码平台(Dify / Coze 扣子)可视化拖拽搭出一个知识库问答应用,再用它的 HTTP API 从 Python 调用。为什么学:①低代码平台是 JD 高频加分项(Dify/Coze/n8n);②它能让你在几分钟内产出一个"可对外展示"的 demo,快速验证想法。产出:dify_coze_demo.py,调用你在平台上搭好的 RAG 应用并打印答案;动手部分(在平台建应用)记录进 index.md。

💡 JS开发者速读:Dify/Coze ≈ 低代码可视化编排平台——像用拖拽的方式搭后端流程(建知识库、配模型、连节点),平台直接给你一个 HTTP 调用地址;你的 Python 代码只需像调普通 REST 接口一样 `requests.post(地址, json={query})` 拿结果。心智上等价于"调一个别人已经写好的后端 API",RAG 的脏活平台替你干了。

### 学习内容

- Dify / Coze(扣子)是什么、各自定位与适用场景
- 在平台上:创建知识库→上传文档→配置模型→发布为应用/获取 API 地址与密钥
- 用 requests(已学)调用平台应用的 HTTP API,api_key/地址从环境变量读
- 平台 RAG 与手写 RAG 的取舍(快速出 demo vs 可控性)
- 【超前】引用雏形:让回答附带来源片段标识(正式引用标注第08周首教)

### 讲解

结论先行:低代码平台的价值是"把 RAG 全链路封装成可视化配置 + 一个 HTTP 接口"。你在平台上传文档、选模型、发布,平台就给你一个调用地址和密钥;Python 侧只需用 requests 发一个 POST、带上 query,就能拿回答案。密钥务必放环境变量。今天以"动手搭出一个能问答的应用 + 用脚本调通它"为目标,代码量很小,重点在平台操作与工程认知。

```python
import os, requests
API_KEY = os.environ["DIFY_API_KEY"]              # 零硬编码,从环境变量读
resp = requests.post(
    os.environ["DIFY_ENDPOINT"],                  # 平台发布的调用地址,也放环境变量
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"query": "商品退货流程?", "inputs": {}, "response_mode": "blocking", "user": "me"},
    timeout=30,
)
print(resp.json()["answer"])                       # 平台已完成 RAG,这里只取答案
```

### 教材与章节

- 主教材/官方文档:Dify 官方文档(知识库/应用发布/API 调用):(https://docs.dify.ai/) ;Coze(扣子)官方站点与文档:(https://www.coze.cn/) ;检索词"Dify 官方文档 中文 知识库"、"Coze 扣子 创建 Bot API 调用"。
- 视频(A级):尚硅谷 LangChain 从入门到实战(低代码/RAG 应用相关章节可对照理解):(https://www.atguigu.com/video/346/)
- HTTP 调用复习:requests 中文文档:(https://requests.readthedocs.io/zh-cn/latest/)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 平台动手 | 3h | 在 Dify 或 Coze 建知识库→上传文档→配模型→发布→拿到 API 地址与密钥 |
| 编码练习 | 2h | 编写 dify_coze_demo.py 调用平台应用 + extra 跟练 |
| 英语 | 0.5h | AI 辅助精读平台英文文档(API 章节) |
| 输出 | 1h | GitHub commit;把"低代码 vs 手写 RAG 取舍"整理为博客素材 |
| 复盘 | 0.5h | 补 index.md(记录平台配置步骤与可展示链接) |

### 当日产出

- [ ] 编写 学习产物/第07周/day48/dify_coze_demo.py:调用低代码平台 RAG 应用(≤120行)
  - 前置动手:在 Dify 或 Coze 上创建一个知识库问答应用(上传一小份文档、选国产模型、发布),拿到调用地址与 API 密钥;把配置步骤与可展示链接记入 index.md
  - 脚本用 requests 向平台应用的 HTTP API 发一个 POST,携带一个查询问题,打印返回的答案
  - 调用地址与 api_key 必须从环境变量读取,零硬编码;设置 timeout 并对请求失败给出可辨识的 print 提示
  - 输入:一个查询问题;输出:打印平台返回的答案
  - 【超前】引用雏形(最小片段,仅识别):若平台返回中含来源/引用字段,额外打印一条"来源"信息即可;正式的引用标注与来源编号规则第08周首教,本日不深入
  - 所用知识点清单:Dify/Coze 入门、requests、os.environ 读 key、JSON 响应解析、异常/超时提示、print、f-string;【超前】引用雏形(最小片段)
- [ ] 补记 学习产物/第07周/day48/index.md:覆盖平台配置步骤、API 调用要点、低代码与手写 RAG 的取舍

### JS→Python对照笔记

- JS `fetch(url, {method:'POST', headers, body})` → Python `requests.post(url, headers=..., json=...)`
- JS `res.json()` → Python `resp.json()`
- JS `process.env.KEY` → Python `os.environ["KEY"]`(地址与密钥都放环境变量)
- JS 调后端 REST 接口 → Python 调低代码平台发布的 HTTP API(平台替你做了 RAG)

### 跟练清单(放extra/)

- extra_platform_compare.py:同一个问题分别问"手写 RAG(day47)"与"平台 RAG(今天)",打印两者答案并简评差异(可控性 vs 便捷),记录到 index.md。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| ---- | ---- | ---- | ---- |
| Dify/Coze 低代码搭 RAG + HTTP API 调用 + 引用雏形 | Dify/Coze 官方文档;尚硅谷 LangChain | dify_coze_demo.py | Dify/Coze 入门、requests、os.environ 读 key、JSON 解析、print;【超前】引用雏形 |

【超前】标注集中区:引用雏形(打印一条来源信息)属【超前】最小片段,已在讲解与产出标注,仅需识别"回答应可回溯到来源",正式引用标注/来源编号第08周首教,本日不要求深入。
硬约束复查:仅用 day48 闭包知识点(超前项已标注)✓ 第三方库合规(requests 已解禁、平台 SDK 若用则入 venv 与 requirements.txt)✓ key/地址零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day49(周日,7h)· 周检测 / 阶段闸门预备 + 对账

今天是本周闸门。目标是限时独立完成一个最小 RAG 问答闭环,验证"加载→切分→向量化→检索→生成"已内化为肌肉记忆。通过后即可平稳进入第08周(RAG 进阶:引用标注/rerank/评测)。同时按主计划要求,本周提交域名备案(周期 2-4 周,RAG 阶段即提交,为第14周公网部署提前铺路)。

### 周检测(限时任务)

任务:45分钟内,不看教材、不看本周产物,独立盲写 学习产物/第07周/day49/kb_qa_check.py:

1. 读入一小段本地文档(可程序内先用 with open("w") 生成一份几行中英文的 sample 文档,保证文件必存在)。
2. 用文本切分器把文档按设定的 chunk_size / chunk_overlap 切成片段。
3. 用 Chroma 建本地集合,把片段向量化后写入(每条唯一 id)。
4. 对一个给定问题做 topK 相似度检索,取回最相关的若干片段。
5. 把命中片段拼成 context,用带 context 与 question 的 ChatPromptTemplate + LCEL 链,调国产大模型基于 context 生成答案。
6. 主流程 print:切分片段数、检索命中数与命中内容、最终答案;检索为空时给出兜底回答,程序不崩溃。

通过标准(须全部满足):

- 45分钟内完成,python kb_qa_check.py 一次跑通、无未捕获异常;
- 正确完成"切分→向量化→检索→生成"完整闭环,答案确实基于检索到的资料;
- 模型/embedding 的 api_key 均从环境变量读取,零硬编码;
- 仅用截至 day49 的闭包知识点(本周新增首教 + 前六周已学),第三方库仅限 venv 内已装并写入 requirements.txt 的 langchain/chromadb 等;
- ≤180 行(周末检测放宽)。

未通过补救方案:

- 仅个别 API 用法或参数写错 → 当天用缓冲 1h 对照 Day43/Day46/Day47 讲解订正,次日重盲写一次(≤45min);
- 检索或生成链路不通 → 重做 Day46(检索)+ Day47(整合),再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第08周前 2 天先补 RAG 全链路欠账,再进入引用标注/rerank/评测,闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项✅/❌/⚠️):
   - day43/langchain_hello.py ☐ day43/extra/extra_chain_two_steps.py ☐ day43/index.md ☐
   - day44/doc_load_split.py ☐ day44/extra/extra_chunk_tune.py ☐ day44/index.md ☐
   - day45/vector_store_build.py ☐ day45/extra/extra_vector_persist.py ☐ day45/index.md ☐
   - day46/retriever_demo.py ☐ day46/extra/extra_retriever_compare.py ☐ day46/index.md ☐
   - day47/rag_chain_qa.py ☐ day47/extra/extra_rag_multi_q.py ☐ day47/index.md ☐
   - day48/dify_coze_demo.py ☐ day48/extra/extra_platform_compare.py ☐ day48/index.md ☐
   - day49/kb_qa_check.py(检测产物)☐
   - requirements.txt(含 langchain/chromadb 等本周依赖)☐
2. 填 README 进度跟踪表:完成% / 自评 1-5 / 卡点 / 补救。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第08周前 2 天改补欠账。
4. 验收:每个 .py 必须 `python xxx.py` 跑通;确认 api_key 全部走环境变量、无任何硬编码泄漏。
5. 备案提醒:本周提交域名备案(周期 2-4 周,主计划要求 RAG 阶段即提交),为第14周作品公网部署提前铺路;记录提交时间与预计下号时间。

## 周尾附录:完整知识点累计清单(截至第07周day49)

第01-06周(已有):基础类型、print/input、f-string、控制流、字符串切片与方法、list/tuple/dict/set、推导式、切片进阶、生成器表达式、random、datetime;def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念;OOP(class/继承/多态/魔术方法/isinstance/type)、文件读写(open/with/模式/encoding)、异常全体系(try/except/else/finally/raise/自定义异常);venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio;大模型 SDK 调用、环境变量读 key、Chat API、Prompt 工程、结构化输出 JSON Mode;流式 Streaming、Function Calling、多轮上下文管理。

第07周(本周新增):

- LangChain:模型封装(国产大模型接入)、ChatPromptTemplate、输出解析器 StrOutputParser
- LCEL:`|` 管道组合(Runnable),chain.invoke 一次跑完"填模板→模型→解析"
- 向量数据库:embedding(文本→向量)、Chroma 建库/写入(add/count)、query 检索、相似度/距离、topK(n_results);Milvus/Faiss 定位认知
- RAG 全链路:文档加载→切分(chunk_size/chunk_overlap)→向量化→检索(retriever)→拼 context→基于资料生成(降低幻觉)
- Dify/Coze 入门:低代码可视化搭 RAG 应用、发布获取 HTTP API、用 requests 调用
- 【超前】识别项(不要求掌握):引用雏形(回答可回溯来源,正式引用标注第08周首教)

下周预告(第08周day50-56):RAG 进阶——引用标注(答案附来源编号)、重排 rerank(含混合检索召回后的二次排序)、RAG 评测方法(构建 30-50 条测试集、命中率/召回率报告)。据 2026 市场修订,评测能力是 AI 应用岗"效果评估"面试弹药的关键一环,也为项目1 README 提供真实数据。
