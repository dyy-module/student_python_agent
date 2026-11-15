# 第08周 · RAG 进阶:引用标注 + 重排 rerank + 评测

> 与主计划的差异说明:本周对应修订版路线图「阶段3中段」(17周映射第08周,day50-56)。在第07周跑通 RAG 全链路的基础上,把检索质量从"能用"提升到"可信、可评测":新增引用标注、重排 rerank、RAG 评测方法三项首教知识点(与 reference 闭包日程表第08周完全一致)。据 2026 市场修订,模型评测/RAG 质量既是 JD 加分项也是面试高频弹药,本周产物直接沉淀为博客"RAG 召回评测"素材与项目1 README 的真实质量数据。Day22 已过,第三方库解禁,本周在 venv 内使用 langchain/向量库/reranker 等并登记 requirements.txt;API key 一律环境变量读取、零硬编码。闸门为 day56 周检测(限时盲写),非阶段闸门(阶段3闸门在 day63)。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第08周/dayN/.py;跟练统一命名 extra_*.py 放入 学习产物/第08周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。

## 本周概览

- 主题:把第07周"能用"的 RAG 升级为"可信、可评测"——引用标注让答案可溯源,rerank 提升召回质量,评测方法让效果可量化。
- 为什么对拿offer有用:引用标注=答案可溯源,是知识库/客服/导购类 AI 产品的信任基础(直接服务项目1"商品知识库导购问答");rerank=召回质量的关键手段,是 JD 高频加分项;评测=面试高频问题"你怎么衡量 RAG 效果"的标准答案。本周直接产出博客"RAG 召回评测"素材,并为项目1 README 验收清单准备真实质量数据(命中率/judge 分)。
- 教材使用策略:主视频 尚硅谷 LangChain(RAG 检索/向量库章节,A级)(50%)+ Datawhale llm-cookbook(Prompt/评测)(25%)+ 国产大模型官方文档(阿里云百炼/DeepSeek/智谱,用于生成与 judge 调用)(25%)。rerank 与评测无可信中文直出视频处,一律用官方文档 + 中文搜索词定位,不编造 BV 号。
- 本周结束时应能做到:
  1. 给检索片段编号并让答案带可溯源引用(编号→来源片段/页码),理解忠实度(faithfulness)。
  2. 在向量召回之上接入 reranker 做二次重排,取 Top-K,并能对比重排前后差异。
  3. 构建 30-50 条评测集,计算召回命中率,并用 LLM-as-judge 对答案打相关性/忠实度分汇总。
  4. day56 闸门:45 分钟内独立盲写"带引用 + 命中率统计 + LLM-as-judge"的综合 RAG 评测程序。

## 前置知识点闭包(截至第07周已学,本周可直接用)

基础类型与容器(int/float/str/bool/None、list/tuple/dict/set)、print/input、f-string、控制流(if/elif/else、for/while/range/enumerate/break/continue)、字符串切片与方法、推导式、生成器表达式、random/datetime、def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念、OOP(class/__init__/self、继承/多态/super、魔术方法、isinstance/type)、文件读写(open/with/模式/encoding)、异常全体系(try/except/else/finally、raise、自定义异常)、venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio、大模型基础概念(token/上下文/温度)、国产大模型 API 调用(通义千问/DeepSeek/GLM)、环境变量读 key、Prompt 工程、JSON Mode 结构化输出、流式 Streaming、Function Calling、多轮上下文管理、LangChain/LCEL、文档加载与切分、embedding、向量数据库(Chroma/Milvus/Faiss)、检索器、RAG 全链路(加载→切分→向量化→检索→生成)、Dify/Coze 入门。

本周新增(首教):引用标注(答案溯源到 chunk)、重排 rerank(召回后二次排序)、RAG 评测方法(评测集/召回命中率/LLM-as-judge)。
【超前】预警:Agentic RAG、多路召回融合(hybrid search 加权/RRF)、专业评测框架(Ragas/TruLens)深度使用本周不作正式教学,若产物需要仅以【超前】最小片段出现并标注(见 Day51/Day55)。

---

## Day50(周一,7h)· 引用标注:让答案可溯源

今天把第07周"能答"的 RAG 升级为"答得有据"。裸 RAG 最大的信任问题是:用户不知道答案从哪来、模型是否在编造。引用标注就是给答案加"脚注"——每句话能回溯到具体来源片段/页码。这是知识库、客服、导购类 AI 产品的信任基础,也是项目1 上线前必须过的关。产出:citation_qa.py,输出带编号引用与来源清单的答案。

💡 JS开发者速读:引用标注 ≈ 给答案加脚注/来源角标(类似前端 `` 上标 + tooltip 显示出处);编号→片段映射 ≈ JS 里用对象/Map 做 id→data 查表;`enumerate(chunks, start=1)` ≈ JS `arr.map((c,i)=>...)` 但直接给出从 1 开始的序号;"仅依据给定片段作答"的 Prompt 约束 ≈ 前端只渲染接口返回的白名单字段,不轻信多余数据。

### 学习内容

- RAG 答案为何需要引用标注(可溯源 = 信任基础,防幻觉)
- 给检索到的 chunk 编号(enumerate 从 1 开始,建立 编号→(来源,文本) 映射)
- Prompt 约束:要求模型"仅依据提供的编号片段作答,并在句末标注引用编号"
- 把答案与被引用来源片段/页码一起结构化输出
- 忠实度(faithfulness):答案不应超出给定片段范围

### 讲解

结论先行:引用标注的工程做法是"先给召回片段编号 → 把编号写进 Prompt 上下文 → 要求模型答复时标注所用编号 → 程序把编号映射回真实来源一起展示"。关键是编号在检索阶段就固定,答案里出现的每个编号都能查回原文,这样既约束模型只依据片段作答(降低幻觉),又让用户可核对出处。

```python
# 教学演示:给检索片段编号,拼成带来源的上下文(非产物答案)
chunks = [("商品A说明书", "支持7天无理由退货"),
          ("售后政策", "退货运费由买家承担")]
context_lines = []
for idx, (source, text) in enumerate(chunks, start=1):   # 从1编号
    context_lines.append(f"[{idx}] (来源:{source}) {text}")
context = "\n".join(context_lines)
prompt = f"仅依据下列编号片段回答,并在句末标注引用编号:\n{context}\n问题:能退货吗?"
print(prompt)
# 期望模型答复形如:"支持7天无理由退货[1],运费由买家承担[2]"
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(RAG 检索/生成章节,A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程(RAG/Prompt 章节):(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"引用标注 citation RAG 教程"、"RAG 答案 溯源 片段编号"(无可信中文直出视频时用官方文档 + 搜索词,不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 引用标注原理/Prompt 约束/忠实度 精读 + 官方文档 |
| 练习 | 2.5h | 编写 citation_qa.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读英文 RAG/citation 文档片段 |
| 输出 | 1h | GitHub commit + 博客"RAG 召回评测"素材归档 |
| 复盘 | 0.5h | 补 index.md、闭包自检 |

### 当日产出

- [ ] 编写 学习产物/第08周/day50/citation_qa.py:带引用标注的知识库问答(≤120行)
  - 复用第07周 RAG 检索:对用户问题召回 Top-N 片段
  - 用 enumerate 给片段从 1 编号,建立 编号→(来源,文本) 的映射(dict)
  - 构造 Prompt:要求模型"仅依据编号片段作答,句末标注引用编号"
  - 调用大模型生成答案(API key 从环境变量读取,零硬编码)
  - 输出:打印带引用编号的答案 + 打印被引用编号对应的来源片段/页码
  - 必须覆盖:答案里出现的每个引用编号都能映射回真实片段;模型未给引用时的兜底提示;检索为空时不崩溃
  - 所用知识点清单:RAG 检索(第07周)、enumerate、dict 映射、f-string、Prompt 工程、Chat API、环境变量读 key、异常处理、for、if、print
- [ ] 补记 学习产物/第08周/day50/index.md:覆盖全部学习内容(代码块纯 Python 可运行)

### JS→Python对照笔记

- 引用标注 ≈ 给答案加脚注/来源角标(前端 `` + tooltip 出处)
- 编号→片段映射 ≈ JS 用 `{}`/`Map` 做 id→data 查表;Python 用 dict
- JS `arr.map((c,i)=>...)` → Python `enumerate(chunks, start=1)` 直接给从 1 的序号
- "仅依据片段作答"的 Prompt 约束 ≈ 前端只渲染接口白名单字段,不轻信多余数据

### 跟练清单(放extra/)

- extra_citation_format.py:把带编号引用的答案再格式化为"答案正文 + 参考来源列表(编号/来源/页码)"两段式,练习结构化输出与来源清单渲染。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 片段编号/Prompt 引用约束/忠实度/来源映射 | 尚硅谷 LangChain-检索生成;Datawhale-RAG | citation_qa.py | RAG 检索、enumerate、dict、Prompt 工程、Chat API、环境变量读 key、异常、print |

【超前】标注集中区:本日无超前内容(Agentic RAG/多路召回融合不深入)。
硬约束复查:仅用 day50 闭包知识点 ✓ 第三方库合规(langchain/向量库,venv 内 pip 并登记 requirements.txt)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day51(周二,7h)· 重排 rerank:召回之后的二次精排

昨天让答案有据可查,今天让"据"更准。向量召回是"粗排"——快但不够精,Top-N 里常混入半相关片段。rerank 是在召回之后用一个专门的重排模型对每个 query-chunk 对打相关性分,再重新排序取 Top-K。这一步是提升 RAG 命中质量性价比最高的手段之一,也是 JD 里"检索质量优化"的核心考点。产出:rerank_demo.py,对比重排前后的 Top-K 顺序。

💡 JS开发者速读:rerank ≈ 搜索结果的二次相关性排序(类似前端拿到一批数据后按更精细的业务规则 `sort` 再截取);两阶段"召回→重排" ≈ 先用便宜的粗筛缩小范围、再用贵的精排,和你做过的"分页接口粗查 + 前端精排"同理;`sorted(docs, key=lambda c: score(...), reverse=True)` ≈ JS `arr.sort((a,b)=>score(b)-score(a))`。

### 学习内容

- 为什么召回 Top-N 后还要重排(向量粗排 vs reranker 精排)
- reranker 模型的作用(bge-reranker 等,对 query-chunk 对打相关性分)
- 两阶段流程:召回 Top-N → rerank → 取 Top-K
- 重排前后顺序对比(评估重排收益)
- rerank 与引用标注配合(重排后仍保留编号来源)

### 讲解

结论先行:标准做法是"召回宽、重排严"——先用向量检索召回较大的 Top-N(如 20 条)保证相关片段不被漏掉,再用 reranker 对这 N 条逐一与 query 打相关性分,按分数降序取较小的 Top-K(如 3-5 条)喂给生成模型。这样既控住了生成上下文长度与成本,又显著提升了进入答案的片段质量。

```python
# 教学演示:两阶段"召回→重排"(用可替换的打分函数示意,非产物答案)
query = "怎么退货"
recalled = [("商品A说明书", "支持7天无理由退货"),
            ("物流说明", "默认顺丰发货"),
            ("售后政策", "退货运费由买家承担")]

def score(q, text):                 # 生产中替换为 reranker 模型打分
    return 1 if any(k in text for k in ["退货", "退回"]) else 0

reranked = sorted(recalled, key=lambda c: score(query, c[1]), reverse=True)
topk = reranked[:2]                 # 重排后取 Top-K
for i, (src, txt) in enumerate(topk, 1):
    print(f"[{i}] {src}: {txt}")
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(检索/向量库章节,A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程:(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"RAG rerank 重排 bge-reranker 教程"、"混合检索 hybrid search 教程"、"召回 重排 top-k"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | rerank 原理/两阶段检索/reranker 模型 精读 + 文档 |
| 练习 | 2.5h | 编写 rerank_demo.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读英文 reranker 文档片段 |
| 输出 | 1h | GitHub commit + 博客素材(重排前后对比) |
| 复盘 | 0.5h | 补 index.md、闭包自检 |

### 当日产出

- [ ] 编写 学习产物/第08周/day51/rerank_demo.py:召回后重排演示(≤120行)
  - 对 day50 召回的 Top-N 片段,接入 reranker(venv 内 pip 安装并写入 requirements.txt)做二次相关性打分
  - 打印:重排前的 Top-N 顺序、重排后的顺序、以及最终取用的 Top-K
  - 对比重排前后进入 Top-K 的片段变化,说明重排收益
  - 若 reranker 走 API 调用,key 从环境变量读取,零硬编码;调用失败有异常兜底
  - 必须覆盖:空召回不崩溃;Top-K 截取边界(K 大于 N 时的处理)
  - 所用知识点清单:RAG 检索、重排 rerank、sorted+key/lambda、列表切片、enumerate、第三方库(reranker/langchain)、异常处理、for、print、f-string
- [ ] 补记 学习产物/第08周/day51/index.md:覆盖全部学习内容

### JS→Python对照笔记

- rerank ≈ 拿到一批数据后按更精细业务规则二次 `sort` 再截取 Top-K
- JS `arr.sort((a,b)=>score(b)-score(a))` → Python `sorted(docs, key=lambda c: score(c), reverse=True)`
- JS `arr.slice(0,k)` → Python `docs[:k]`
- 两阶段"召回宽→重排严" ≈ 后端粗查分页 + 前端精排,成本/质量折中思路一致

### 跟练清单(放extra/)

- extra_rerank_topk.py:改变 Top-K 取值(如 K=1/3/5),观察并打印重排后进入答案的片段随 K 变化的差异,体会 K 对质量与成本的影响。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 两阶段召回→重排/reranker 打分/Top-K 截取 | 尚硅谷 LangChain-检索;Datawhale | rerank_demo.py | RAG 检索、rerank、sorted+lambda、切片、enumerate、异常、第三方库、print |

【超前】标注集中区:多路召回融合(hybrid search 的加权融合/RRF 倒数排名融合)属【超前】,本周只做"单路向量召回 + rerank",不深入融合算法;若产物提及仅以【超前】最小片段标注。
硬约束复查:仅用 day51 闭包知识点 ✓ 第三方库合规(reranker 在 venv 内、requirements.txt 登记)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day52(周三,7h)· RAG 评测基础:评测集 + 命中率

前两天让 RAG 更好,今天开始回答面试官最爱问的一句:"你怎么衡量 RAG 的效果?" 答案是——建评测集、算命中率。没有量化指标的优化都是拍脑袋。今天构建一份 30-50 条的黄金评测集(问题 + 期望命中的来源 chunk),并计算召回命中率(hit rate):标准 chunk 是否落在 Top-K 内。产出:build_testset.py,落盘评测集并跑出第一个命中率数字。

💡 JS开发者速读:评测集 ≈ 单元测试的 fixture(一组"输入 + 期望输出"的固定样本);命中率(hit rate)≈ "测试用例里有多少条通过";召回率(recall)≈ 测试覆盖率思路(该覆盖的相关片段覆盖了多少);把评测集落盘为 json/csv ≈ 前端把 mock 数据抽成独立 fixture 文件复用。

### 学习内容

- 为什么要评测(面试高频"你怎么衡量 RAG 效果")
- 评测集(黄金集)构建:问题 + 标准答案/标准应命中 chunk
- 召回命中率(hit rate):Top-K 中是否包含标准 chunk
- 召回率(recall)概念:命中的相关 chunk 占全部相关 chunk 的比例
- 把评测集与评测结果落盘为可读文件(with/open/json 复用第03周)

### 讲解

结论先行:评测的第一步是"有一把尺子"——评测集。每条样本至少含"问题"和"这个问题应该命中哪个来源 chunk(或标准答案要点)"。最基础的指标是命中率:对每个问题跑一次检索,看标准 chunk 是否出现在返回的 Top-K 里,统计命中的比例。有了这把尺子,后续 day53 的 judge 打分、day54 的参数调优才有可对比的基准。

```python
# 教学演示:用迷你评测集算命中率(非产物答案)
eval_set = [
    {"q": "怎么退货", "gold_chunk": "售后政策"},
    {"q": "发什么快递", "gold_chunk": "物流说明"},
]

def topk_sources(q):                # 生产中替换为真实 RAG 检索
    return {"怎么退货": ["售后政策", "商品A说明书"],
            "发什么快递": ["商品A说明书"]}[q]

hit = 0
for item in eval_set:
    got = topk_sources(item["q"])
    ok = item["gold_chunk"] in got  # 标准 chunk 是否在 Top-K 内
    hit += ok
    print(f"Q:{item['q']} 命中:{ok} Top-K:{got}")
print(f"命中率 = {hit}/{len(eval_set)} = {hit/len(eval_set):.0%}")
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(检索/评测相关章节,A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程:(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"RAG 评测 召回率 命中率"、"RAG 评测集 构建 golden"、"hit rate recall RAG"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 评测集设计/命中率/召回率 精读 + 文档 |
| 练习 | 2.5h | 编写 build_testset.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读英文 RAG evaluation 文档片段 |
| 输出 | 1h | GitHub commit + 评测集入库(项目1 素材) |
| 复盘 | 0.5h | 补 index.md、闭包自检 |

### 当日产出

- [ ] 编写 学习产物/第08周/day52/build_testset.py:构建评测集 + 命中率基础(≤120行)
  - 构建一份 30-50 条评测集,每条含:问题、期望命中的来源 chunk(或标准答案要点)
  - 用 with/open + json 把评测集保存到本地文件(如 testset.json),并打印总条数
  - 抽样打印若干条校验格式正确(问题非空、gold_chunk 非空)
  - 提供一个基础命中率计算:对每条问题跑检索,判断 gold_chunk 是否在 Top-K 内,打印逐条命中与总命中率
  - 必须覆盖:评测集为空/文件写入失败时的异常兜底;命中率分母不为零的边界处理
  - 所用知识点清单:RAG 评测方法、评测集构建、命中率、文件读写(with/open/json)、list/dict、for、len、异常处理、print、f-string
- [ ] 补记 学习产物/第08周/day52/index.md:覆盖全部学习内容

### JS→Python对照笔记

- 评测集 ≈ 单元测试 fixture(输入 + 期望输出的固定样本)
- 命中率 hit rate ≈ "多少条用例通过";召回率 recall ≈ 覆盖率思路
- JS `JSON.stringify/parse` + `fs.writeFileSync` → Python `json.dump` + `with open(...,'w')`
- JS `arr.filter(...).length / arr.length` → Python `sum(ok for ...) / len(eval_set)`

### 跟练清单(放extra/)

- extra_testset_stats.py:统计评测集的问题类型分布(如按业务域/难度打标),打印各类型条数,检查评测集是否覆盖均衡。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 评测集构建/命中率/召回率/结果落盘 | 尚硅谷 LangChain-评测;Datawhale | build_testset.py | RAG 评测方法、评测集、命中率、文件读写/json、for、len、异常、print |

【超前】标注集中区:专业评测框架(Ragas/TruLens)的深度使用属【超前】,本周手写命中率即可,不引入框架;若提及仅以【超前】最小片段标注。
硬约束复查:仅用 day52 闭包知识点 ✓ 第三方库合规(向量库/langchain,requirements.txt 登记)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day53(周四,7h)· LLM-as-judge:用模型给答案打分

命中率只回答"该找到的片段找到没有",但答得好不好、有没有忠于片段,还需要更细的评价。今天学 LLM-as-judge:用一个(通常更强的)大模型当"评委",按相关性(relevance)和忠实度(faithfulness)给答案打分,并复用第05周的 JSON Mode 让分数可被程序解析汇总。这是当前 RAG/Agent 评测的主流做法,也是面试的加分弹药。产出:llm_judge.py,对评测集答案打分并汇总平均分。

💡 JS开发者速读:LLM-as-judge ≈ 用一个模型给另一个模型的输出打分(类似 code review 里的"自动评审器");让 judge 输出 JSON ≈ 你熟悉的"约定接口返回结构再 parse";把多条分数汇总求平均 ≈ 前端对一组评分做 `reduce` 聚合;judge 有偏差需人工抽检 ≈ 自动化测试之外仍需人工验收。

### 学习内容

- LLM-as-judge 概念:用一个模型给另一个模型的答案打分
- 打分维度:相关性(relevance,是否切题)、忠实度(faithfulness,是否仅依据给定片段)
- 让 judge 模型输出结构化分数(复用第05周 JSON Mode)
- 汇总多条打分(平均分/分布)
- judge 的局限(位置偏差/评分漂移,需人工抽检校准)

### 讲解

结论先行:LLM-as-judge 的关键是"给评委一份明确的评分标准 + 强制结构化输出"。把问题、给定片段、待评答案一起交给 judge,要求它只输出形如 `{"relevance":4,"faithfulness":5}` 的 JSON,程序再 parse 出来累加。忠实度尤其重要——它衡量答案是否"只用了给定片段、没有编造",这正是引用标注想保证的东西,两者互为印证。

```python
# 教学演示:用一个 LLM 给答案打"相关性/忠实度"分(非产物答案)
import os
q, context, answer = "怎么退货", "[1]售后政策:运费买家承担", "支持退货[1]"
judge_prompt = (
    "你是严格的评测员,只输出JSON,不要解释。给答案打分(1-5):\n"
    "relevance=是否切题;faithfulness=是否仅依据给定片段、无编造。\n"
    f"问题:{q}\n给定片段:{context}\n待评答案:{answer}\n"
    '仅输出形如 {"relevance":4,"faithfulness":5} 的JSON。'
)
api_key = os.environ["MODEL_API_KEY"]      # key 从环境变量读,零硬编码
# resp = 调用 Chat API(judge_prompt) → 解析 JSON → 累加分数(留给产物实现)
print(judge_prompt)
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程(Prompt/评测章节):(https://datawhalechina.github.io/llm-cookbook/)
- 大模型官方文档(judge 调用):阿里云百炼 (https://help.aliyun.com/zh/model-studio/qwen-function-calling) ;DeepSeek (https://platform.deepseek.com/api-docs/zh-cn/) ;智谱 GLM (https://docs.bigmodel.cn/cn/guide/develop/http/introduction)
- 中文搜索词:"LLM-as-judge 评测集 构建"、"RAG faithfulness relevance 打分"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | LLM-as-judge 原理/评分维度/JSON 输出 精读 + 官方文档 |
| 练习 | 2.5h | 编写 llm_judge.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读英文 LLM-as-judge 文档片段 |
| 输出 | 1h | GitHub commit + 博客素材(judge 评分维度设计) |
| 复盘 | 0.5h | 补 index.md、闭包自检 |

### 当日产出

- [ ] 编写 学习产物/第08周/day53/llm_judge.py:LLM-as-judge 打分器(≤120行)
  - 读取 day52 评测集,对每条问题取其 RAG 答案与给定片段
  - 构造 judge Prompt(评分标准明确),要求 judge 模型只输出 JSON(relevance/faithfulness,1-5)
  - 调用大模型(key 从环境变量读,零硬编码),用 JSON Mode/解析拿到分数
  - 汇总:打印每条问题的相关性/忠实度分,以及两维度的平均分
  - 必须覆盖:judge 返回非法 JSON 时的解析异常兜底(不计入平均并警告);评分范围越界的处理
  - 所用知识点清单:LLM-as-judge、Prompt 工程、JSON Mode、Chat API、环境变量读 key、dict/list、for、异常处理、len、print、f-string
- [ ] 补记 学习产物/第08周/day53/index.md:覆盖全部学习内容

### JS→Python对照笔记

- LLM-as-judge ≈ 自动评审器:一个模型给另一个模型输出打分
- 约定 judge 输出 JSON ≈ 前端约定接口返回结构再 `JSON.parse`
- JS `scores.reduce((a,b)=>a+b,0)/n` → Python `sum(scores)/len(scores)`
- judge 有偏差需人工抽检 ≈ 自动化测试之外仍需人工验收

### 跟练清单(放extra/)

- extra_judge_rubric.py:给 judge 增加一条自定义评分维度(如"简洁度"或"是否给出可执行建议"),观察分数变化,练习评分标准(rubric)设计。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| LLM-as-judge/评分维度/JSON 输出/汇总 | 尚硅谷 LangChain;Datawhale;百炼/DeepSeek 官方文档 | llm_judge.py | LLM-as-judge、Prompt 工程、JSON Mode、Chat API、环境变量读 key、异常、for、print |

【超前】标注集中区:本日无超前内容(专业评测框架的深度集成不展开)。
硬约束复查:仅用 day53 闭包知识点 ✓ 第三方库合规(langchain/大模型 SDK,requirements.txt 登记)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day54(周五,7h)· 召回优化排查:为什么没命中

有了评测集(尺子)和 judge(评委),今天做真正的"优化"——但不是瞎调,而是做对照实验。命中率上不去通常有三个源头:切分粒度(chunk size/overlap)、embedding 模型、query 本身的表述。今天固定评测集,每次只改一个变量,观察命中率变化,得出可复现的结论。这是把"我感觉变好了"升级为"数据证明变好了"的关键,也是项目1 README 里最有说服力的部分。产出:recall_tuning.py,输出变量→命中率的对照表。

💡 JS开发者速读:对照实验 ≈ 前端做 A/B 或性能剖析时"一次只改一个变量";切分粒度权衡 ≈ 打包时的 chunk 拆分(太大噪声多、太小语义断裂);query 改写 ≈ 搜索框把用户口语 query 规整/补全关键词再发请求;把实验结果落盘 ≈ 把 lighthouse/benchmark 结果存成可回归的基线。

### 学习内容

- 影响命中率的三大因素:切分粒度(chunk size/overlap)、embedding 模型、query 表述
- 对照实验方法:固定评测集,一次只改一个变量,记录命中率变化
- query 改写/扩展:把口语问题改写成更利于检索的形式
- 切分粒度权衡(太大→噪声多,太小→语义断裂)
- 把排查结论沉淀为可复现记录(为 README/博客准备数据)

### 讲解

结论先行:优化的前提是"可对比"。固定同一份评测集,只改一个变量(如 chunk size 从大改小、或开/关 query 改写),各跑一次命中率,把结果排成对照表。这样才能判断到底是哪个因素在拖累召回,而不是同时改一堆、最后不知道是哪个起了作用。对照实验 + 命中率,就是 RAG 调优的科学方法。

```python
# 教学演示:固定评测集,改变切分粒度做对照实验(示意,非产物答案)
eval_set = [{"q": "怎么退货", "gold": "售后政策"}]

def hit_rate(chunk_size):           # 生产中:按 chunk_size 重切→重建索引→检索
    table = {"small": 0.6, "large": 0.4}   # 示意命中率(需真实实验得到)
    return table[chunk_size]

for size in ["small", "large"]:
    print(f"切分粒度={size} 命中率={hit_rate(size):.0%}")
print("结论:本评测集上较小切分粒度命中率更高(须以真实实验数据为准)")
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(切分/检索章节,A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程:(https://datawhalechina.github.io/llm-cookbook/)
- 中文搜索词:"RAG 召回率 优化 chunk size overlap"、"query 改写 RAG 检索"、"embedding 模型 对比 命中率"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 2.5h | 召回影响因素/对照实验法/query 改写 精读 + 文档 |
| 练习 | 2.5h | 编写 recall_tuning.py + extra 跟练 |
| 英语 | 0.5h | 借工具精读英文 chunking/retrieval 调优文档片段 |
| 输出 | 1h | GitHub commit + 对照实验数据入博客素材 |
| 复盘 | 0.5h | 补 index.md、闭包自检 |

### 当日产出

- [ ] 编写 学习产物/第08周/day54/recall_tuning.py:召回优化对照实验(≤120行)
  - 固定 day52 评测集,分别在不同设置下跑检索:如切分粒度(大/小)、query 改写(开/关)
  - 每种设置各计算一次命中率,把"变量→命中率"排成对照表并打印
  - 给出结论:在本评测集上哪种设置命中率更优(以真实实验数据为准,不臆断)
  - 可选:把对照结果写入本地文件,作为可回归的基线记录
  - 必须覆盖:某一设置检索失败时跳过并警告、不中断整体实验;评测集为空的兜底
  - 所用知识点清单:RAG 检索/切分、评测集、命中率、query 改写、for、dict、f-string、文件读写、异常处理、print
- [ ] 补记 学习产物/第08周/day54/index.md:覆盖全部学习内容

### JS→Python对照笔记

- 对照实验"一次改一个变量" ≈ 前端性能剖析/A-B,控制变量法
- 切分粒度权衡 ≈ 打包 chunk 拆分:太大噪声多、太小语义断裂
- query 改写 ≈ 搜索框把口语 query 规整/补全关键词再发请求
- 实验结果落盘 ≈ 把 lighthouse/benchmark 存成可回归基线

### 跟练清单(放extra/)

- extra_query_rewrite.py:对评测集里口语化问题做简单改写(补全关键词/去停用词),对比改写前后的命中率变化,打印对照。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| 召回影响因素/对照实验/query 改写/命中率 | 尚硅谷 LangChain-切分检索;Datawhale | recall_tuning.py | RAG 检索/切分、评测集、命中率、query 改写、for、dict、文件读写、异常、print |

【超前】标注集中区:多路召回融合(hybrid search 加权/RRF)、Agentic RAG 的自适应检索属【超前】,本周对照实验只在单路召回上做变量控制,不深入融合/智能体检索。
硬约束复查:仅用 day54 闭包知识点 ✓ 第三方库合规(langchain/向量库/embedding,requirements.txt 登记)✓ key 零硬编码 ✓ ≤120行 ✓ extra 命名正确 ✓

---

## Day55(周六,7h)· 综合项目日:带引用 + rerank + 可评测的 RAG

今天是项目日,把本周四天拧成一条完整链路:检索 → rerank 重排 → 带引用标注生成 → 评测集命中率 + LLM-as-judge 打分 → 汇总成一张评测结果表。这正是把第07周"能跑的 RAG"升级为"可信、可评测的 RAG",也是项目1"商品知识库导购问答"README 里质量数据的直接来源。产出:cited_rerank_rag.py(≤150行)+ 一张评测结果表。

💡 JS开发者速读:整体结构类似你搭过的"数据层→服务层→展示层"前端应用,只是这里分层是"检索层→重排层→生成层→评测层";把各环节解耦成函数再串成 pipeline ≈ 前端把请求/转换/渲染拆成纯函数组合;评测结果表 ≈ 你把 benchmark 结果渲染成一张报表组件。

### 学习内容(综合复用,无全新理论)

- 把第07周基础 RAG 升级为"带引用标注 + rerank 重排 + 可评测"的完整版
- 串起 day50-54:检索 → rerank → 带引用生成 → 命中率 + LLM-as-judge
- 分层组织(检索层/重排层/生成层/评测层),各环节解耦成函数
- 产出一张评测结果表(逐条明细 + 汇总命中率/平均分)

### 讲解

结论先行:综合项目的关键是"分层解耦 + 一条可复现的评测流水线"。把检索、重排、带引用生成、judge 打分各自写成独立函数,再用一个 pipeline 函数对评测集逐条串起来,最后汇总成表。这样任何一环都能单独替换或调优(呼应 day54 的对照实验),也让评测结果可复现、可写进 README。

```python
# 教学演示:综合 RAG 评测流水线的分层骨架(示意,非产物答案)
def retrieve(q):       ...   # 召回 Top-N(第07周)
def rerank(q, docs):   ...   # 重排取 Top-K(day51)
def answer(q, docs):   ...   # 带引用生成(day50)
def judge(q, docs, a): ...   # LLM-as-judge 打分(day53)

def run_pipeline(eval_set):
    rows = []
    for item in eval_set:
        docs = rerank(item["q"], retrieve(item["q"]))
        ans = answer(item["q"], docs)
        score = judge(item["q"], docs, ans)
        hit = item["gold"] in [d[0] for d in docs]
        rows.append({"q": item["q"], "hit": hit, "answer": ans, "score": score})
    return rows                      # 再汇总为评测结果表(命中率/平均分)
```

### 教材与章节

- 主视频:尚硅谷 LangChain 从入门到实战(RAG 综合案例章节,A级):(https://www.atguigu.com/video/346/)
- 文档:Datawhale LLM 入门教程:(https://datawhalechina.github.io/llm-cookbook/)
- 大模型官方文档:阿里云百炼 (https://help.aliyun.com/zh/model-studio/qwen-function-calling) ;DeepSeek (https://platform.deepseek.com/api-docs/zh-cn/)
- 中文搜索词:"RAG 综合项目 引用 rerank 评测"(不编造 BV 号)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 1.5h | 画分层结构、想清 pipeline 数据流与评测表字段 |
| 项目实战 | 3.5h | 编写 cited_rerank_rag.py + 跑评测出结果表 |
| 英语 | 0.5h | 借工具精读英文 RAG pipeline 文档片段 |
| 输出 | 1h | GitHub commit + 评测表沉淀为 README/博客素材 |
| 复盘 | 0.5h | 补 index.md、闭包自检、列可改进点 |

### 当日产出

- [ ] 编写 学习产物/第08周/day55/cited_rerank_rag.py:带引用+rerank+可评测的 RAG(项目日,≤150行)
  - 升级第07周 RAG:检索 → rerank 重排取 Top-K → 带引用标注生成答案
  - 用 day52 评测集跑全流程,统计命中率;用 day53 的 judge 对每条答案打相关性/忠实度分
  - 生成并保存一张评测结果表:逐条(问题/是否命中/答案/引用编号/judge 分)+ 末尾汇总(总命中率 + 两维度平均分)
  - API key 从环境变量读取,零硬编码;第三方库在 venv 内,requirements.txt 登记
  - 必须覆盖:检索为空/judge 解析失败/评测集为空时不崩溃;结果表可写入本地文件
  - 所用知识点清单:RAG 全链路、rerank、引用标注、评测集、命中率、LLM-as-judge、JSON Mode、文件读写、dict/list、for、异常处理、print、f-string
- [ ] 补记 学习产物/第08周/day55/index.md:覆盖设计思路(分层)与全部学习内容

### JS→Python对照笔记

- 分层"检索→重排→生成→评测" ≈ 前端"数据层→服务层→展示层",各司其职
- 各环节解耦成函数再串 pipeline ≈ 前端把请求/转换/渲染拆成纯函数组合
- 评测结果表 ≈ 把 benchmark 数据渲染成报表组件
- Python `[{...}, {...}]` 汇总 ≈ JS 对象数组 `map` 后聚合

### 跟练清单(放extra/)

- extra_report_md.py:把评测结果表额外导出为 Markdown 表格文件,作为博客"RAG 召回评测"与项目1 README 的质量数据素材。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| -------- | -------- | -------- | -------------- |
| RAG 全链路 + rerank + 引用 + 评测综合 | 尚硅谷 LangChain-RAG 综合案例;Datawhale | cited_rerank_rag.py | RAG 全链路、rerank、引用标注、评测集、命中率、LLM-as-judge、JSON Mode、文件读写、异常 |

【超前】标注集中区:Agentic RAG(检索由智能体自主决策多轮)、专业评测框架(Ragas/TruLens)集成属【超前】,本项目日手写 pipeline 与指标即可,若提及仅以【超前】最小片段标注。
硬约束复查:仅用 day55 闭包知识点 ✓ 第三方库合规(langchain/向量库/reranker/大模型 SDK,requirements.txt 登记)✓ key 零硬编码 ✓ 项目日 ≤150行 ✓ extra 命名正确 ✓

---

## Day56(周日,7h)· 周检测 + 对账

今天是本周闸门。目标是限时独立完成一个"带引用标注 + 命中率统计 + LLM-as-judge"的综合 RAG 评测程序,验证本周知识已内化。通过后即可平稳进入第09周(Agent/Tool/Memory/LangGraph + 阶段3闸门预备)。本周非阶段闸门(阶段3闸门在 day63:知识库问答 10 个测试问题 ≥7 个合理且引用正确)。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第08周/day56/cited_kb_qa_check.py:

1. 准备一组问题(可用内置迷你评测集:每条含问题 + 标准应命中来源 chunk)。
2. 对每个问题跑 RAG 检索 →(建议)rerank 重排取 Top-K → 生成带引用编号的答案(编号可映射回来源片段)。
3. 用评测集统计命中率:标准 chunk 是否落在 Top-K 内,给出命中数/命中率。
4. 用 LLM-as-judge 给每条答案打相关性/忠实度分(JSON 输出),汇总平均分。
5. 打印逐条明细(问题/是否命中/答案/引用编号/judge 分)+ 末尾汇总(命中率 + 平均分);key 从环境变量读取,零硬编码。

通过标准(须全部满足):

- 45 分钟内完成,python cited_kb_qa_check.py 一次跑通、无未捕获异常;
- 答案带可溯源引用(每个引用编号都能映射回真实来源片段);
- 有 rerank 或命中率统计(至少其一,建议命中率),并给出量化数字;
- 有 LLM-as-judge 打分与汇总平均分;
- key 零硬编码;仅用截至 day56 的闭包知识点;第三方库在 venv 内且 requirements.txt 登记;≤180行(周末检测放宽)。

未通过补救方案:

- 仅个别错误(引用编号映射/judge 的 JSON 解析)→ 当天用缓冲 1h 对照 Day50/Day53 讲解订正,次日重盲写一次(≤45min);
- 评测/引用逻辑不通(命中率算错、答案无来源)→ 重做 Day52 评测集 + Day54 命中率,再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第09周前 2 天先补 RAG 评测欠账,再进入 Agent;day63 阶段3闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项✅/❌/⚠️):
   - day50/citation_qa.py ☐ day50/extra/extra_citation_format.py ☐ day50/index.md ☐
   - day51/rerank_demo.py ☐ day51/extra/extra_rerank_topk.py ☐ day51/index.md ☐
   - day52/build_testset.py ☐ day52/testset.json ☐ day52/extra/extra_testset_stats.py ☐ day52/index.md ☐
   - day53/llm_judge.py ☐ day53/extra/extra_judge_rubric.py ☐ day53/index.md ☐
   - day54/recall_tuning.py ☐ day54/extra/extra_query_rewrite.py ☐ day54/index.md ☐
   - day55/cited_rerank_rag.py ☐ day55/评测结果表 ☐ day55/extra/extra_report_md.py ☐ day55/index.md ☐
   - day56/cited_kb_qa_check.py(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5(功能完整性/闭包合规/行数与命名/代码质量四维)/卡点/补救。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第09周前 2 天改补欠账。
4. 验收:每个 .py 必须 python xxx.py 跑通;把本周评测结果(命中率/judge 分/day54 对照实验)沉淀为博客"RAG 召回评测"素材与项目1 README 的真实质量数据。

## 周尾附录:完整知识点累计清单(截至第08周day56)

第01-07周(已有):基础类型与容器、print/input、f-string、控制流、字符串方法、推导式/生成器表达式、random/datetime、函数与参数全体系、lambda、map/filter、模块与包、import、闭包/nonlocal、装饰器概念、OOP(class/继承/多态/super/魔术方法/isinstance/type)、文件读写(open/with/模式/encoding)、异常全体系(try/except/else/finally/raise/自定义异常)、venv/pip/requirements.txt、requests、正则 re、类型提示 typing、asyncio、大模型概念(token/上下文/温度)、国产大模型 API 调用、环境变量读 key、Prompt 工程、JSON Mode、流式 Streaming、Function Calling、多轮上下文管理、LangChain/LCEL、文档加载与切分、embedding、向量数据库(Chroma/Milvus/Faiss)、检索器、RAG 全链路、Dify/Coze 入门。

第08周(本周新增):

- 引用标注:片段编号(enumerate 从 1)、编号→(来源,文本)映射、Prompt 约束"仅依据编号片段作答并标注引用"、答案附来源片段/页码、忠实度(faithfulness)概念。
- 重排 rerank:两阶段"召回宽 Top-N → 重排严 Top-K"、reranker 模型(bge-reranker 等)对 query-chunk 打相关性分、sorted+key/lambda 重排、重排前后顺序对比。
- RAG 评测方法:评测集(黄金集)构建(问题 + 标准 chunk/答案)、召回命中率 hit rate、召回率 recall、切分粒度/embedding/query 改写的对照实验排查、LLM-as-judge(relevance/faithfulness,JSON 输出 + 汇总平均)、评测结果表/报告落盘。
- 【超前】识别项(不要求掌握):多路召回融合(hybrid search 加权/RRF)、Agentic RAG(智能体自主多轮检索)、专业评测框架(Ragas/TruLens)深度使用。

下周预告(第09周day57-63):Agent、Tool、Memory、LangGraph 入门、MCP(认知);把本周"可评测的 RAG"接入智能体编排,产出多工具 Agent + Memory + LangGraph 编排示例,项目1"商品知识库导购问答"上线(README 含架构图与成本数据)。day63 为阶段3闸门:个人知识库问答系统 10 个测试问题 ≥7 个回答合理且引用正确。
