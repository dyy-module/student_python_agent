# 第04周 · venv + requests + 正则 + 类型提示 + asyncio

> 与主计划的差异说明:本周严格对应修订版路线图「阶段1后段」(17周映射第04周),主题为 venv/pip/requirements.txt、requests、正则re、类型提示typing、asyncio,闸门为 **day28 阶段1闸门**(新闻摘要生成器限时完成 + 能讲清 Python 与 JS 差异)。关键变化:**day22 为第三方库解禁点**——「Day22 前禁一切第三方库」的约束自本周起解除,day22 及以后产物方可使用 requests。venv/pip/requirements.txt、requests、re、typing、asyncio 五项均在本周首教,与 reference 日程表第04周完全一致,不增删。
> 变更记录:首版(基于2026市场修订版生成)。
> 变更记录:v1.1(2026-10-24 day21 对账日检测第04周,锚点覆盖性订正)——联网实测后修四处教程侧缺陷(均不转嫁学习者):①Day26 主教材原指 async-io 根,但 23.1「协程」页实为 yield 老式写法与产物 async def 不符→改指 23.2「使用asyncio」为正式出处+加勿顺翻 23.3aiohttp 提醒;②Day23 验收区“异步本周不涉及”与 Day26 教 asyncio 矛盾→改为“异步请求库不教、标准库 asyncio 归 day26”精确表述;③Day22 主教材升级具体 venv 小节并标明 pip freeze/requirements 的权威锚点=官方 tutorial/venv 页(廖雪峰 venv 页不讲 requirements);④Day24 标明 findall/sub 廖雪峰 reg-exp 页未讲、以官方 re 模块页为准。【待统一】工作日时间分配体例(英语/复盘未分行,与周03不一致)已挂 README 呆账。仅改教程文本/链接,主计划与知识点排期未变。
> 变更记录:v1.2(2026-10-28 day23 教程检测,联网实测订正)——①Day23 主教材由廖雪峰书根目录升级为 **17.2 requests 具体小节**(实测真讲 get/params/status_code/text/json()/headers/post/timeout,根目录页不直接讲 requests),并补相邻页提醒(17.3 chardet/17.4 psutil 非本周项勿顺翻);②Day23 补 requests 官方英文 quickstart 为异常体系/raise_for_status 参考页(中文 readthedocs 链接实测 404,维持搜索词口径;并订正旧注记——廖 17.2 页**实含 timeout= 参数**,未讲的仅 raise_for_status 与异常体系);③消除 raise_for_status 三无项:在【超前】区写明“本日只教识别、产出不强制、欲用放 beyond/”(此前该口径只存在于产物壳,属题面双源)。连带:骨架总表第04周 requests 中文文档 404 链接同日回写。仅改教程文本/链接,知识点排期未变。
> 变更记录:v1.3(2026-11-05 day25 教程检测,联网实测订正)——①**消除 Day25 假锚点**:原“主教材廖雪峰—函数/高级特性”实为书根目录且全书无独立 typing 小节(2026-11-05 联网复核+往期 grep 记录;当日站点正文抓取为空体,标疑似存活·需人工确认),降为导航入口,主锚点改官方 typing 页(实测 200,正文 grep 到 Optional[X]≡X|None、Callable[[int],str] 等词条;属参考工具页,已加“按需检索勿通读”提醒);②补“运行时不强制”概念锚点=官方教程 4.9.8 函数注解(实测正文真讲“存入 __annotations__、对函数其他部分没有影响”,同日初抓 errors/appendix 两页均无注解内容后改抓 controlflow 页确认);③菜鸟根页标注“不讲 typing 仅备用”;④超前口径向 day23 句式对齐(欲用放 beyond/ 即留痕不判未标),消除“仅识别 vs 可隔离试用”措辞张力;⑤“3-4 个函数”前加“例如”消示例四项与题干的边界歧义;当日产出补两行自检交检句(全周其余 6 天同缺,仍留 day28 对账批量统一);讲解代码块补“教学演示非产物答案”标注。另:mypy 只一句提及无归属,属轻三无项,挂呆账未改正文。仅改教程文本/链接,知识点排期未变。
> 变更记录:v1.4(2026-11-06 day26 教程检测,联网实测复核)——①Day26 讲解代码块与产物 async_demo.py 结构同构但缺标注(同 day17 已确立口径、day24/25 均已带,day26 漏),补"教学演示,非产物答案"标注并注明设计由学习者自定;②本轮实测复核 v1.1 锚点订正成立:廖 23.2 正文 grep 到 async def/await asyncio.sleep/asyncio.run 真讲(day26 承重锚点覆盖性通过),官方 asyncio 页实为概念概览+API 索引(asyncio.run 调用形式未直接出现),维持"速查"定位不当承重点;菜鸟根页实测不讲 asyncio,仅语法速查(与 day25 同口径)。连带登记:day26 产物壳仍为 v3 旧版(壳 18 行超 v3.1 的 15 行红线、改写扩写教程题面、复述教材 URL 与知识点清单),待转功能2 重生成 v3.1 指针壳(只动注释不碰实现行);两行自检交检句与时间分配体例仍留 day28 对账批量统一。仅改教程文本,知识点排期未变。
> 变更记录:v1.5(2026-11-07 day27 教程检测+产物壳重生成,联网实测)——①Day27 主教材由书根目录(反模式:根目录不得当唯一锚点)升级为廖 13.1 文件读写具体小节(实测 200,正文真讲 open/with/read/write),速查行改为带复习日标注的具体小节清单(官方 re 页实测 200 含 findall/sub/search,官方 typing、廖 15/23.2 沿用 v1.1-v1.3 实测结论);②消除"列目录"矛盾信号:产出硬要求"遍历指定目录下多个 .md"但 os.listdir/glob 未正式教(周头仅口头识别),讲解/学习内容无出处——已在获取层就地补口径(硬编码文件名列表规避,或 os 作【超前】最小片段/放 beyond/,不判未教先用),属反模式第1/2条教程侧缺陷当场修(直接影响产出可执行性,白工风险);③day27 两个产物壳由 v3 旧版重生成 v3.1 指针壳(旧壳改写扩写教程题面致两处对不上、重列知识点与 URL、extra 壳自创≤60行),只动注释不涉实现(学习者尚未盲写)。连带登记:项目日≤150行与 00_验证规则"工作日≤120"存在口径差(周六项目日非"工作日"非"周日检测",两套文件互不覆盖),挂 README 呆账留 day28 对账统一;两行自检交检句与时间分配体例仍随全周批量。仅改教程文本/链接与产物壳,知识点排期未变。
> 变更记录:v1.6(2026-11-07 day26 产物验收中学习者质疑经确认的排期订正)——**asyncio.gather 由【超前】转正式教学,落位 Day26**:原排期把"顺序vs并发区别"列为当日考点却禁产物实际使用 gather,属矛盾信号+判罚错配(学习者产物自发写 gather 对照并分析时序,反被按超前未留痕压分,违规在题面非人);且廖 23.2 原文并发示例即 gather,教材给了、首日不用属白工。新口径:gather 作"顺序vs并发区别"这一已计概念的语法载体(概念计数仍≤5,不违反种子规则12),create_task/Task 对象调度与 aiohttp 仍【超前】。改动:Day26 开篇/学习内容/讲解代码块/当日产出/JS对照/验收区,连带周头【超前】预警、Day27 两处、周尾累计清单。不改:Day28 闸门题面(gather 会写属加分不作通过线)、主计划与骨架(无 gather 粒度,无冲突)。验收口径同步:此前 day26 产物因 gather 所扣闭包分撤销,归因教程侧。仅改教程文本,其余知识点排期未变。
> 变更记录:v1.7(2026-11-07 day26 验收争议订正)——Day26 产出硬项"额外:用 print 说明 time.sleep 阻塞后果"改为 print/注释均可:该条考点(阻塞卡死事件循环)已由"顺序vs并发"概念项覆盖,print 还是 # 属载体格式、无理解含量差异;原口径致误判扣分(学习者注释已答对仍被扣功能完整性分),属反模式第7条判罚错配,当场按白工条款收回。同批口径声明:格式类措辞差异不得单独作为验收靶子。仅改题面一句,知识点排期未变。
> 本周产物约定:固定产物置于 学习产物/第04周/dayN/.py;跟练 extra_*.py 放 学习产物/第04周/dayN/extra/;每日笔记 index.md 同目录;严禁混放。

## 本周概览

- 主题:打通第三方库与工程实用技能——用虚拟环境隔离依赖、用 requests 访问网络、用正则清洗文本、用类型提示提升可维护性、用 asyncio 迈向高并发。
- 为什么对拿offer有用:venv/pip 是工程化与部署的地基(第13周 FastAPI/Docker 的依赖隔离全靠它);requests 是调 API 与爬数据的主力(第05周大模型 API 调用、RAG 语料获取的雏形);正则 re 是文本清洗与结构化抽取的核心(RAG 文档预处理、脏数据提取);typing 类型提示是可维护性信号(FastAPI/Pydantic 靠类型注解驱动参数校验与自动文档);asyncio 是高并发 AI 服务的基础(第13周 FastAPI 异步接口、第06周流式 Streaming 都建立在事件循环之上)。本周直接锚定第05周国产大模型 API 与第13周 FastAPI 服务化。
- 教材使用策略:主教材 廖雪峰Python(60%)+官方中文文档速查(25%)+菜鸟教程语法速查(15%)。requests/re/typing/asyncio 部分优先用你 10 年 JS/TS 经验做映射式理解(npm→pip、axios/fetch→requests、RegExp→re、TS类型→typing、Promise/async-await→asyncio),只重点看差异。
- 本周结束时应能做到:
  1. 用 `python -m venv` 建虚拟环境、激活后用 pip 装包,并用 `pip freeze` 生成 requirements.txt 锁定依赖。
  2. 用 requests 发起 GET/POST,读状态码/响应头/JSON,设超时并用 try/except 兜底网络异常。
  3. 用 re 完成 match/search/findall/sub/split 与分组捕获,清洗与抽取文本;给函数写 Optional/List/Dict/Callable 类型提示。
  4. day28 阶段1闸门:45 分钟内独立盲写「新闻摘要生成器」(requests 抓取 → re 清洗提取 → 输出摘要),并能口头讲清 Python 与 JS 在包管理/类型/异步上的差异。

## 前置知识点闭包(截至第03周已学,本周可直接用)

基础类型(int/float/str/bool/None)、print/input、f-string、if/elif/else、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、切片进阶、生成器表达式、random.randint、datetime.date、def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念;OOP(class/__init__/self、实例属性vs类属性、继承/方法重写/super()/多态、issubclass/isinstance/type、魔术方法 __str__/__repr__/__eq__/__add__/__len__/__lt__)、文件读写(open/with、模式 r/w/a、encoding、read/readline/readlines/write、for line in f、strip)、异常全体系(try/except/else/finally、按类型多异常捕获、as e、raise、自定义异常类继承 Exception)。

本周新增(首教):venv/pip/requirements.txt、requests(Day22 第三方库解禁点)、正则 re、类型提示 typing、asyncio。
【超前】预警:aiohttp/httpx(requests 的异步替代,本周不教,异步抓取仅以【超前】最小片段识别)、re 高级特性(命名分组 `(?P...)`、非捕获组 `(?:...)`、零宽断言,本周仅识别不深入)、asyncio.gather(2026-11-07 v1.6 起于 day26 正式教学,作"顺序vs并发区别"的语法载体)与 asyncio.create_task/Task 对象调度、aiohttp 异步请求属【超前】本周不教、json 模块的 dumps/loads 序列化(requests 的 `.json()` 直接返回 dict 可用,但独立 import json 属【超前】)、sys/os/time 等标准库模块(本周不作正式教学,产物如需仅以【超前】最小片段出现)。

---

## Day22(周一,7h)· venv / pip / requirements.txt(第三方库解禁点)

今天正式解除「禁第三方库」的封印。第一步不是急着装包,而是学会用虚拟环境把每个项目的依赖隔离开——这是所有工程化与部署的地基,第13周 FastAPI/Docker 的依赖锁定全建立在此。产出:一个环境自检脚本 + requirements.txt,确认你已能在 .venv 内安装并导入 requests。

💡 JS开发者速读:心智模型高度可迁移——`python -m venv .venv` ≈ 给项目建一个隔离的 `node_modules`;`pip install requests` ≈ `npm install axios`;`pip freeze > requirements.txt` ≈ 生成 `package.json` 的 dependencies 锁版本;`pip install -r requirements.txt` ≈ `npm install`(按锁文件还原)。关键差异:Python 的虚拟环境需要**手动激活**(Windows 跑 `.venv\Scripts\activate`),激活后终端提示符前会出现 `(.venv)`;而 Node 靠本地 node_modules 自动解析,无需激活。

### 学习内容

- 为什么需要虚拟环境:依赖版本隔离,避免全局污染(JS对应 项目级 node_modules)
- 创建与激活:`python -m venv .venv` + `.venv\Scripts\activate`(Windows)(JS对应 无需激活的差异点)
- pip 装包/升级/卸载/查看:`pip install`、`--upgrade`、`uninstall`、`show`、`list`(JS对应 npm install/update/uninstall/info/ls)
- `pip freeze > requirements.txt` 锁定依赖 与 `pip install -r requirements.txt` 还原(JS对应 package.json + npm install)
- 第三方库解禁:自 day22 起可 `import requests`(JS对应 import 第三方包)

### 讲解

结论先行:虚拟环境是「一个项目一套独立依赖」的目录;激活后,`pip install` 装进 .venv 而非全局 Python,`import` 也优先从 .venv 找。requirements.txt 是依赖快照(每行 `包名==版本`),提交到 Git 后他人一条命令即可还原环境。下面的命令是终端操作(非 Python 代码),代码块仅演示"激活后如何验证 requests 来自 .venv"。

```python
# 终端流程(理解即可,非Python语句):
#   python -m venv .venv                 创建虚拟环境
#   .venv\Scripts\activate               Windows 激活(提示符出现 (.venv))
#   python -m pip install requests       装第三方库(day22 起解禁)
#   python -m pip freeze > requirements.txt   锁定依赖
import requests                          # 激活后才能导入成功
print("requests 版本:", requests.__version__)
print("来自路径:", requests.__file__)     # 路径含 .venv 即证明隔离生效
```

### 教材与章节

- 主教材:廖雪峰Python — **16.13 venv**(创建/激活/deactivate 的真实出处,但该页**不讲 requirements.txt/pip freeze**):(https://liaoxuefeng.com/books/python/built-in-modules/venv/index.html)
- 速查(**本日 requirements.txt/pip freeze/install -r 的权威锚点**):Python官方中文教程 — 12.虚拟环境和包:(https://docs.python.org/zh-cn/3/tutorial/venv.html) ;venv 模块:(https://docs.python.org/zh-cn/3/library/venv.html)
- 语法速查:菜鸟教程 Python3 模块:(https://www.runoob.com/python3/python3-module.html)

### 时间分配

| 时段 | 时长 | 内容                                                                       |
| ---- | ---- | -------------------------------------------------------------------------- |
| 学习 | 3.5h | venv 创建/激活、pip 五类子命令、requirements.txt 生成与还原 精读+实操(含英语 30min 精读官方英文 venv 文档) |
| 练习 | 2.5h | 建 .venv 装 requests,编写 env_check.py + requirements.txt + extra 跟练     |
| 笔记 | 1h   | 补 index.md,写 JS→Python 对照,GitHub 首次 commit 本项目                    |

### 当日产出

- [ ] 在 学习产物/第04周/day22/ 下创建并激活 .venv,`pip install requests`,用 `pip freeze` 生成同目录 requirements.txt(终端操作,命令写入 index.md 备查)
- [ ] 编写 学习产物/第04周/day22/env_check.py:虚拟环境自检脚本(≤120行)
  - 导入 requests 成功时,print 其 `__version__` 与 `__file__` 路径(用于肉眼确认来自 .venv 而非全局)
  - 用文件读写(week03 闭包)读取同目录 requirements.txt,逐行 print 出已锁定的"包名==版本"清单
  - 用 try/except 捕获 ImportError:若 requests 未安装,print 友好提示(提醒先激活 .venv 再 pip install),程序不崩溃
  - python env_check.py 在激活的 .venv 内直接跑通,每步有 print
  - 所用知识点清单:import、第三方库 requests(day22 解禁)、`__version__`/`__file__` 属性、try/except(ImportError)、with open/for line in f/strip(week03 文件闭包)、print、f-string
- [ ] 补记 学习产物/第04周/day22/index.md:覆盖全部学习内容,记录建环境/装包/freeze 的终端命令(代码块纯 Python 可运行,终端命令用文本标注不混入 .py)

### JS→Python对照笔记

- JS `npm init` + 本地 node_modules → Python `python -m venv .venv`(需手动激活)
- JS `npm install axios` → Python `pip install requests`
- JS package.json 的 dependencies → Python requirements.txt(`包名==版本` 每行一条)
- JS `npm install`(按 package-lock 还原)→ Python `pip install -r requirements.txt`
- JS `npm ls` / `npm info x` → Python `pip list` / `pip show x`
- JS 自动解析 node_modules 无需激活 → Python 必须先 activate 才走 .venv

### 跟练清单(放extra/)

- extra_freeze_read.py:用文件读写打开 requirements.txt,对每行用字符串 split("==") 拆出包名与版本,print 成"包名 -> 版本"的整齐清单;文件不存在时用 try/except 提示。

### 当日验收(合规区)

| 学习内容                            | 教材章节                        | 当日产物                   | 产物所用知识点                                                    |
| ----------------------------------- | ------------------------------- | -------------------------- | ----------------------------------------------------------------- |
| venv/pip/requirements.txt/解禁 requests | 廖雪峰-模块;官方-12.虚拟环境和包 | env_check.py + requirements.txt | import、requests、`__version__`/`__file__`、try/except、文件读写、print、f-string |

【超前】标注集中区:本日无超前内容(aiohttp/httpx、pip 高级用法不展开)。
硬约束复查:仅用 day22 闭包知识点 ✓ 第三方库合规(day22 解禁点,requests 可用)✓ ≤120行 ✓ extra/命名正确 ✓

---

## Day23(周二,7h)· requests:GET / POST / 状态码 / 超时 / JSON

今天让程序真正联上网络。requests 是你访问一切 HTTP 接口的主力——第05周调国产大模型 API、RAG 抓语料,底层都是它。你已用 axios/fetch 十年,重点是搞清 Python 的写法差异(同步阻塞、显式超时、`.json()` 自动解析、异常靠 except 而非 Promise.catch)。产出:一个健壮的 HTTP 抓取器。

💡 JS开发者速读:`requests.get(url)` ≈ `axios.get(url)`,但**默认同步阻塞**(不像 fetch 返回 Promise);`r.status_code` ≈ `res.status`;`r.json()` ≈ `await res.json()`(requests 直接返回 dict,无需 await);`r.headers` ≈ `res.headers`;超时用 `timeout=` 参数(fetch 需 AbortController,requests 内建)。最大差异:错误处理走 `try/except requests.exceptions.X`,而不是 `.catch()`;非 2xx 状态码 requests **不会自动抛异常**(需手动 `raise_for_status()`),这点和 axios 不同(axios 4xx/5xx 会 reject)。

### 学习内容

- `requests.get(url, params=, timeout=)` 发起 GET,查询参数与超时(JS对应 axios.get + params + AbortController)
- `requests.post(url, json=/data=)` 发起 POST(JS对应 axios.post body)
- 响应对象:`status_code`、`headers`、`text`、`.json()`(JS对应 res.status/headers/text()/json())
- 非 2xx 不自动抛错,`raise_for_status()` 手动触发(JS对应 axios 自动 reject 的差异)
- 异常体系:`requests.exceptions.Timeout`/`ConnectionError`/`RequestException`(JS对应 try/catch 或 .catch)

### 讲解

结论先行:一次健壮请求 = 设 timeout + 查 status_code + try/except 兜底。requests 是同步的,调用会阻塞到响应返回;`.json()` 在响应体是合法 JSON 时直接给你 dict,否则抛异常(要放进 try)。永远设 timeout,否则网络卡死会永久挂起。下面用 `(https://example.com`(IANA) 保留示例域名)做占位,实际替换为你的目标接口。

```python
import requests
url = "(https://example.com/api")        # 替换为真实公开接口/页面
try:
    r = requests.get(url, params={"q": "python"}, timeout=5)
    print("状态码:", r.status_code)     # 200 才是成功
    print("最终URL:", r.url)            # params 拼接后的地址
    print("类型:", r.headers.get("Content-Type"))
    print("正文前80字:", r.text[:80])   # 切片(week01 闭包)
except requests.exceptions.Timeout:
    print("超时:请检查网络或调大 timeout")
except requests.exceptions.RequestException as e:
    print("请求失败:", e)
```

### 教材与章节

- 主教材:廖雪峰Python — **17.2 requests**(get/params/status_code/text/json()/headers/post/data=/json=/timeout 的真实出处):(https://liaoxuefeng.com/books/python/third-party-modules/requests/index.html)
  ⚠ 该页**不讲 raise_for_status 与异常体系**(本日产出硬要求,以下方官方 quickstart 为准);17.2 下一页即 17.3「chardet」、17.4「psutil」(均非本周项),勿顺翻
- 参考(异常体系 Timeout/ConnectionError/HTTPError/RequestException 与 raise_for_status 的正式出处,英文·借翻译工具精读):requests 官方 Quickstart:(https://requests.readthedocs.io/en/stable/user/quickstart/)
- 速查:Python官方中文 urllib.request(requests 的标准库底层对应,非 requests 本体):(https://docs.python.org/zh-cn/3/library/urllib.request.html) ;HOWTO 抓取 URL:(https://docs.python.org/zh-cn/3/howto/urllib2.html)
- 语法速查:菜鸟教程 Python3:(https://www.runoob.com/python3/)
- 注:requests 官方**中文**文档链接不稳定(2026-10-28 实测 readthedocs zh-cn 路径 404),如需中文版请用搜索词「requests 官方中文文档」自行定位,本清单不杜撰链接。

### 时间分配

| 时段 | 时长 | 内容                                                                       |
| ---- | ---- | -------------------------------------------------------------------------- |
| 学习 | 3.5h | GET/POST、响应对象四属性、超时、异常体系、raise_for_status 精读+敲示例(含英语 30min 精读 urllib 英文文档) |
| 练习 | 2.5h | 编写 http_fetcher.py + extra 跟练                                          |
| 笔记 | 1h   | 补 index.md,写 JS→Python 对照,GitHub commit                                |

### 当日产出

- [ ] 编写 学习产物/第04周/day23/http_fetcher.py:健壮 HTTP 抓取器(≤120行)
  - 用 requests.get 抓取一个自选公开接口/页面,必须设置 timeout,并检查 status_code
  - 成功分支:print 状态码、Content-Type 响应头、正文前若干字符(text 切片);若响应为 JSON 则用 `.json()` 取出并 print 其中一个字段
  - 演示一次带查询参数(params)的 GET,print 拼接后的最终 URL
  - 用 try/except 分别捕获 Timeout 与 RequestException,print 友好错误信息,程序不崩溃
  - 所用知识点清单:requests.get、params、timeout、status_code、headers、text、`.json()`、requests.exceptions(Timeout/RequestException)、try/except、字符串切片、print、f-string
- [ ] 补记 学习产物/第04周/day23/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `axios.get(url,{params})` → Python `requests.get(url, params=)`
- JS `await res.json()` → Python `r.json()`(同步返回 dict,无 await)
- JS `res.status` / `res.headers` → Python `r.status_code` / `r.headers`
- JS axios 4xx/5xx 自动 reject → Python requests 不自动抛错,需 `r.raise_for_status()`
- JS fetch 超时靠 AbortController → Python `timeout=` 参数内建
- JS `.catch(err)` → Python `except requests.exceptions.RequestException as e`

### 跟练清单(放extra/)

- extra_headers.py:用 requests 抓取一个公开地址,打印全部响应头(遍历 headers);再用自定义 headers(如 User-Agent)发起一次请求,print 状态码,体会请求头的作用。

### 当日验收(合规区)

| 学习内容                                  | 教材章节                          | 当日产物        | 产物所用知识点                                                          |
| ----------------------------------------- | --------------------------------- | --------------- | ----------------------------------------------------------------------- |
| requests GET/POST/状态码/超时/JSON/异常 | 廖雪峰-17.2 requests;官方-quickstart(异常体系)+urllib.request | http_fetcher.py | requests.get、params、timeout、status_code、headers、text、json()、异常、切片、print |

【超前】标注集中区:异步请求库 aiohttp/httpx 属【超前】,本周不教(注:标准库 asyncio 于 day26 会教,它与本日 requests 的同步阻塞是两回事,勿混为一谈);requests 的异步替代留综合项目仅识别。raise_for_status() 为本日教学识别项、产出**不强制使用**(廖 17.2 页不讲,口径见上方教材注与官方 quickstart);产物欲试用属超范围,放 day23/beyond/ 隔离即留痕,**不判超前未标**。
硬约束复查:仅用 day23 闭包知识点 ✓ 第三方库合规(requests,day22 已解禁)✓ ≤120行 ✓ extra/命名正确 ✓

---

## Day24(周三,7h)· 正则表达式 re:match / search / findall / 分组 / sub

今天学文本处理的瑞士军刀。正则是 RAG 语料清洗、结构化抽取(从网页/日志里抠出邮箱、日期、金额)的核心技能,day28 闸门的"新闻正文提取"就靠它。你已写熟 JS 正则,重点是 Python re 的 API 差异(函数式入口、findall 直接给 list、分组用 group()、sub 做替换)。产出:一个文本清洗与抽取器。

💡 JS开发者速读:正则**语法**几乎一致(`\d`、`[\w.+-]+`、`{3,}`、`^$` 都通用),差异在**调用方式**——JS 是 `str.match(re)` / `re.exec(str)`,Python 是 `re.findall(pattern, str)` / `re.search(pattern, str)`(模式在前、文本在后);JS `match` 带 g 返回数组 ≈ Python `re.findall` 直接返回 list;分组 JS `m[1]` → Python `m.group(1)`;替换 JS `str.replace(re, x)` → Python `re.sub(pattern, x, str)`。Python 建议用**原始字符串** `r"..."` 写模式,避免反斜杠被转义(JS 无此烦恼)。

### 学习内容

- `re.match`(从头匹配)/`re.search`(全文找第一个)/`re.findall`(找全部返回 list)(JS对应 ^锚定match / exec / match+g)
- 分组捕获 `(...)` 与 `m.group(n)`/`groups()`(JS对应 捕获组 m[n])
- `re.sub(pattern, repl, str)` 替换/脱敏(JS对应 str.replace)
- `re.split(pattern, str)` 按模式切分(JS对应 str.split(re))
- 字符类与量词 `\d \w \s [] + * ? {m,n}`、原始字符串 `r"..."`(JS对应 同语法,差异在转义写法)

### 讲解

结论先行:选对函数就成功一半——只要"有没有"用 search,要"全部"用 findall,要"从头是否匹配"用 match,要"改写"用 sub。分组 `()` 让你从匹配结果里精确抠出子片段,用 `group(1)/group(2)` 取。写模式一律加 `r` 前缀。下面是教学演示,产物的清洗规则由你自己设计。

```python
import re
text = "联系 alice@mail.com 或 bob@test.org,电话 13800138000"
emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text)   # 找全部→list
print("邮箱:", emails)
m = re.search(r"(\d{3})(\d{8})", text)                  # 分组捕获
if m:
    print("号段:", m.group(1), "尾号:", m.group(2))
print("脱敏:", re.sub(r"\d", "*", text))                # 逐位替换
print("切分:", re.split(r"[\s,]+", text))               # 按空白/逗号切
```

### 教材与章节

- 主教材:廖雪峰Python — **15 正则表达式**(match/split/group()/compile/贪婪):(https://liaoxuefeng.com/books/python/reg-exp/index.html)  ⚠ 该页**不教 findall/sub**(本日产出硬要求),此两点以下方官方 re 模块页为准
- 速查(**findall/sub/search 正式出处**):Python官方中文 re 模块:(https://docs.python.org/zh-cn/3/library/re.html) ;正则表达式 HOWTO:(https://docs.python.org/zh-cn/3/howto/regex.html)
- 语法速查:菜鸟教程 Python3:(https://www.runoob.com/python3/)

### 时间分配

| 时段 | 时长 | 内容                                                                       |
| ---- | ---- | -------------------------------------------------------------------------- |
| 学习 | 3.5h | match/search/findall/sub/split、分组、字符类量词、原始字符串 精读+逐条实验(含英语 30min 精读 re HOWTO 英文) |
| 练习 | 2.5h | 编写 regex_cleaner.py + extra 跟练                                         |
| 笔记 | 1h   | 补 index.md,整理常用模式速查表,GitHub commit                              |

### 当日产出

- [ ] 编写 学习产物/第04周/day24/regex_cleaner.py:文本清洗与抽取器(≤120行)
  - 程序内置一段含噪声的文本(混有 HTML 标签、多余空白、邮箱、手机号)
  - 用 re.findall 提取全部邮箱并 print;用 re.search + 分组把手机号拆成号段与尾号分别 print
  - 用 re.sub 完成两件事:去掉 HTML 标签、把手机号中间四位脱敏为 *,各 print 结果
  - 用 re.split 按空白/标点把文本切成词列表并 print 数量
  - 所用知识点清单:re.findall、re.search、re.sub、re.split、分组 group()、字符类与量词、原始字符串 r""、str 方法、for、len、print、f-string
- [ ] 补记 学习产物/第04周/day24/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `str.match(/re/g)` → Python `re.findall(r"re", str)`(模式在前,返回 list)
- JS `re.exec(str)` / `str.search` → Python `re.search(r"re", str)`
- JS `m[1]` → Python `m.group(1)`
- JS `str.replace(/re/g, x)` → Python `re.sub(r"re", x, str)`
- JS `str.split(/re/)` → Python `re.split(r"re", str)`
- JS 正则字面量 `/.../` → Python 原始字符串 `r"..."`(避免反斜杠转义)

### 跟练清单(放extra/)

- extra_extract.py:用 re 从一段混合文本中提取所有 URL、所有日期(YYYY-MM-DD 格式)、所有中文手机号,并对手机号做分组打印号段与尾号。

### 当日验收(合规区)

| 学习内容                                     | 教材章节                   | 当日产物         | 产物所用知识点                                                     |
| -------------------------------------------- | -------------------------- | ---------------- | ------------------------------------------------------------------ |
| re match/search/findall/sub/split/分组/字符类 | 廖雪峰-正则;官方-re 模块+HOWTO | regex_cleaner.py | re.findall/search/sub/split、分组、字符类量词、原始字符串、str、for、print |

【超前】标注集中区:命名分组 `(?P...)`、非捕获组 `(?:...)`、零宽断言 `(?=)/(?!)` 属【超前】,本日仅识别语法存在,产物不要求使用。
硬约束复查:仅用 day24 闭包知识点 ✓ 第三方库合规(未使用,标准库 re)✓ ≤120行 ✓ extra/命名正确 ✓

---

## Day25(周四,7h)· 类型提示 typing:Optional / List / Dict / Callable

今天给 Python 补上你熟悉的"类型感"。作为写了十年 TS 的人,这天最轻松——但要抓住关键差异:Python 类型提示**运行时不强制**(只是注解,解释器不报错),靠 mypy/IDE 做静态检查;而 TS 是编译期强制。typing 是第13周 FastAPI/Pydantic 的直接前置(Pydantic 靠类型注解做参数校验与序列化)。产出:一组带完整类型标注的数据处理函数。

💡 JS开发者速读:语法几乎是你 TS 经验的平移——`def f(x: int) -> str` ≈ `function f(x: number): string`;`List[int]` ≈ `number[]`(或 `Array`);`Dict[str, int]` ≈ `Record`;`Optional[str]` ≈ `string | null`(可能是 None);`Callable[[int], int]` ≈ `(x: number) => number`。**最大差异**:Python 类型提示纯注解、运行时不校验(传错类型也不会崩,除非你手动检查),TS 编译期就拦截;且 Python 需 `from typing import ...`(3.9+ 也可直接用 `list[int]`,本周统一用 typing 写法)。

### 学习内容

- 变量与函数参数/返回值注解 `x: int`、`def f(a: str) -> bool`(JS对应 TS 类型标注)
- 容器泛型 `List[int]`、`Dict[str, int]`、`Tuple`、`Set`(JS对应 number[]、Record、元组)
- `Optional[X]`(= X 或 None)、`Union[X, Y]`(JS对应 X | null、X | Y)
- `Callable[[参数类型], 返回类型]`(JS对应 函数类型 (a:number)=>number)
- 类型提示运行时不强制、仅供工具检查(与 TS 编译期强制的核心差异)

### 讲解

结论先行:类型提示是"写给人和工具看的契约",不改变运行行为——加不加,程序跑起来一样;它的价值在可读性、IDE 补全、mypy 静态检查,以及 FastAPI/Pydantic 的自动校验。`Optional[X]` 表示"可能是 X 也可能是 None",提醒调用方判空。下面演示四类标注(教学演示,非产物答案),产物由你设计更完整的函数集。

```python
from typing import Optional, List, Dict, Callable

def total(nums: List[int]) -> int:
    return sum(nums)       

def find(user: Dict[str, str], key: str) -> Optional[str]:
    return user.get(key)                 # 找不到→None,故标 Optional

def twice(f: Callable[[int], int], x: int) -> int:
    return f(f(x))                       # 参数是"接收int返回int的函数"

print(total([1, 2, 3]), find({"n": "Li"}, "n"), twice(lambda v: v + 1, 5))
```

### 教材与章节 

- 主锚点:Python官方中文 typing 模块( Optional/Union/Callable/List/Dict 的正式出处;⚠ 该页是**参考工具页,按需检索词条即可,勿通读**——TypedDict/Protocol/NewType 等大半页属【超前】或第13周):(https://docs.python.org/zh-cn/3/library/typing.html)
- "运行时不强制"概念锚点:官方教程 4.9.8 函数注解(实讲注解机制:存入 `__annotations__`、对函数其他部分没有影响):(https://docs.python.org/zh-cn/3/tutorial/controlflow.html)
- 注:廖雪峰全书**无独立 typing 小节**(2026-11-05 联网复核,其函数章不讲类型提示),原列书根目录**不得当本日锚点**,仅留作全书导航入口:(https://liaoxuefeng.com/books/python/)
- 语法速查:菜鸟教程 Python3(通用索引页,不讲 typing,仅备用):(https://www.runoob.com/python3/)

### 时间分配

| 时段 | 时长 | 内容                                                                       |
| ---- | ---- | -------------------------------------------------------------------------- |
| 学习 | 3.5h | 参数/返回注解、List/Dict/Optional/Union/Callable、运行时不强制的验证 精读+实验(含英语 30min 精读 typing 英文文档) |
| 练习 | 2.5h | 编写 typed_stats.py + extra 跟练                                           |
| 笔记 | 1h   | 补 index.md,整理 TS↔typing 对照表,GitHub commit                           |

### 当日产出

- [ ] 编写 学习产物/第04周/day25/typed_stats.py:带类型提示的数据统计工具(≤120行)
  - 定义 3-4 个函数并写**完整**类型提示(例如:求平均值(参数 List[int]、返回 float)、按条件过滤(参数 List + Callable 谓词、返回 List)、词频统计(参数 List[str]、返回 Dict[str, int])、安全取值(找不到返回 None 故标 Optional))
  - 主流程用一组示例数据调用这些函数并 print 结果
  - 额外演示:故意传入类型不符的值,print 说明"程序仍运行"(印证类型提示运行时不强制)
  - 所用知识点清单:from typing import Optional/List/Dict/Callable、参数与返回值注解、def、lambda、推导式、dict.get、len/sum、print、f-string
- [ ] 补记 学习产物/第04周/day25/index.md:覆盖全部学习内容;末两行自检照旧(①我说不出出处的知识点;②学了但没落进任何行为的知识点)

### JS→Python对照笔记

- TS `function f(x: number): string` → Python `def f(x: int) -> str`
- TS `number[]` / `Array` → Python `List[int]`
- TS `Record` → Python `Dict[str, int]`
- TS `string | null` → Python `Optional[str]`;TS `A | B` → Python `Union[A, B]`
- TS `(x: number) => number` → Python `Callable[[int], int]`
- TS 编译期强制类型 → Python 运行时**不**强制(仅注解,靠 mypy/IDE 检查)

### 跟练清单(放extra/)

- extra_typed_funcs.py:写 3 个函数并加完整类型提示——一个返回 Optional、一个参数含 Callable、一个用 Dict/List 容器标注;调用并 print,验证类型注解不影响运行结果。

### 当日验收(合规区)

| 学习内容                                       | 教材章节                | 当日产物       | 产物所用知识点                                                              |
| ---------------------------------------------- | ----------------------- | -------------- | --------------------------------------------------------------------------- |
| typing 注解/Optional/List/Dict/Callable/不强制 | 官方-typing 模块+教程4.9.8 函数注解(廖雪峰无 typing 小节) | typed_stats.py | typing(Optional/List/Dict/Callable)、注解语法、def、lambda、推导式、dict.get、print |

【超前】标注集中区:TypedDict、Protocol、Generic[T] 泛型、`from __future__ import annotations` 属【超前】,本日仅识别存在,产物不要求使用;欲试用放 day25/beyond/ 隔离目录即留痕,**不判超前未标**。
硬约束复查:仅用 day25 闭包知识点 ✓ 第三方库合规(未使用,标准库 typing)✓ ≤120行 ✓ extra/命名正确 ✓

---

## Day26(周五,7h)· asyncio:async / await / 事件循环

今天迈出高并发的第一步。asyncio 是第06周流式 Streaming、第13周 FastAPI 异步接口的底层模型——AI 服务大量时间在等网络 IO,异步能让"等待"不浪费 CPU。你有 JS async/await 十年经验,心智模型直接迁移,重点是 Python 的差异:协程需**显式启动事件循环**(asyncio.run),`await` 只能用在 async def 内,sleep 要用 `asyncio.sleep` 而非阻塞的 time.sleep。产出:一个协程执行顺序演示器。

💡 JS开发者速读:`async def` ≈ `async function`;`await x` ≈ `await x`;协程不 await 就"不执行"(和 JS 调用 async 函数返回 Promise 类似,但 Python 是返回 coroutine 对象,不 await 根本不跑)。核心差异:JS 事件循环是**运行时内建**的,你直接调 async 函数即可;Python 必须 `asyncio.run(main())` **手动启动**事件循环。另一个坑:JS `setTimeout` 不阻塞,Python 的 `time.sleep` 会**阻塞整个循环**,协程里必须用 `await asyncio.sleep()`。并发编排 `asyncio.gather` ≈ `Promise.all`(本日正式教,作顺序vs并发的对照载体;更细的 create_task/Task 对象调度属【超前】)。

### 学习内容

- `async def` 定义协程函数(JS对应 async function)
- `await` 等待协程/可等待对象,只能在 async def 内用(JS对应 await)
- `asyncio.run(main())` 启动事件循环(JS对应 运行时内建、无需手动启动的差异)
- `await asyncio.sleep(n)` 非阻塞等待(JS对应 setTimeout/Promise 延时,差异于阻塞的 time.sleep)
- 协程不 await 则不执行;顺序 await 与并发 `asyncio.gather` 的区别(gather 本日正式教,作此概念的语法载体;create_task/Task 对象调度属【超前】)

### 讲解

结论先行:协程是"可暂停/恢复的函数"——遇到 `await` 处若任务在等 IO,事件循环就切去跑别的协程,IO 好了再回来,从而在单线程内实现高并发。但**只有 await 才让出控制权**;顺序 await 各协程仍是串行等待。Python 与 JS 最大不同:必须用 `asyncio.run()` 显式点火。下面演示"顺序 await=串行"与"gather=并发"的对照(教学演示,非产物答案,协程个数、名称、时序设计由你自定)。

```python 
import asyncio

async def task(name: str, sec: int) -> str:
    print(f"{name} 开始")
    await asyncio.sleep(sec)          # 非阻塞等待(勿用 time.sleep)
    print(f"{name} 完成")
    return name

async def main():
    await task("A", 1)                # 顺序 await:串行
    await task("B", 1)
    # gather 并发对照:输出交叠,总耗时≈最长者
    print(await asyncio.gather(task("A", 1), task("B", 1)))

asyncio.run(main())                   # 手动启动事件循环
```

### 教材与章节

- 主教材:廖雪峰Python — **23.2 使用asyncio**(本日 async def/await/asyncio.run 的正式出处):(https://liaoxuefeng.com/books/python/async-io/asyncio/index.html)
  ⚠ 勿读 23.1「协程」((https://liaoxuefeng.com/books/python/async-io/coroutine/index.html)):该页用 yield 老式协程写法,与本日产物的 async def/await 完全不同,不属于本日教学;23.2 下一页即 23.3「使用aiohttp」(aiohttp 属【超前】本周不教),勿顺翻
- 速查:Python官方中文 asyncio — 异步 I/O:(https://docs.python.org/zh-cn/3/library/asyncio.html)
- 语法速查:菜鸟教程 Python3:(https://www.runoob.com/python3/)

### 时间分配

| 时段 | 时长 | 内容                                                                       |
| ---- | ---- | -------------------------------------------------------------------------- |
| 学习 | 3.5h | async def/await/asyncio.run/asyncio.sleep/asyncio.gather、事件循环与协程调度、顺序vs并发对照 精读+实验(含英语 30min 精读 asyncio 英文文档) |
| 练习 | 2.5h | 编写 async_demo.py + extra 跟练                                            |
| 笔记 | 1h   | 补 index.md,写 JS↔asyncio 对照,GitHub commit                              |

### 当日产出

- [ ] 编写 学习产物/第04周/day26/async_demo.py:协程执行顺序演示器(≤120行)
  - 用 async def 定义 2-3 个协程,每个内部先 print"开始"、`await asyncio.sleep(不同秒数)`、再 print"完成"并返回一个结果
  - 定义 main 协程,用**顺序 await** 依次调用这些协程,print 观察执行是串行(一个完成才下一个开始)
  - 再追加**并发对照段**:用 `await asyncio.gather(...)` 一次性调度这些协程,print 观察输出交叠、总耗时≈最长者(与顺序段串行时序形成对照);更细的 create_task/Task 对象调度属【超前】,不在本日要求内
  - 额外:说明"若把 time.sleep 换成阻塞会发生什么"——print 或注释写明均可(2026-11-07 v1.7 订正:验收看说法正确性,载体格式不作硬项;不引入 time 模块)
  - 所用知识点清单:async def、await、asyncio.sleep、asyncio.run、asyncio.gather、协程返回值、print、f-string
- [ ] 补记 学习产物/第04周/day26/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS `async function f()` → Python `async def f()`
- JS `await p` → Python `await coro`(只能在 async def 内)
- JS 事件循环运行时内建、直接调 async 函数 → Python 必须 `asyncio.run(main())` 手动启动
- JS `setTimeout`/延时不阻塞 → Python 用 `await asyncio.sleep(n)`(阻塞的 time.sleep 会卡死循环)
- JS `Promise.all([...])` → Python `await asyncio.gather(...)`(本日正式教;JS 传数组,Python 逗号分隔传协程对象)
- JS 调 async 函数返回 Promise(会开始执行)→ Python 调协程返回 coroutine 对象(不 await 不执行)

### 跟练清单(放extra/)

- extra_coroutine.py:定义两个协程(如"下载"和"解析",各 await asyncio.sleep 模拟耗时),在 main 中顺序 await 执行,print 出清晰的开始/完成时序,体会 await 的暂停与恢复。

### 当日验收(合规区)

| 学习内容                                | 教材章节                | 当日产物     | 产物所用知识点                                        |
| --------------------------------------- | ----------------------- | ------------ | ----------------------------------------------------- |
| async/await/asyncio.run/sleep/gather/事件循环 | 廖雪峰-异步IO;官方-asyncio | async_demo.py | async def、await、asyncio.sleep、asyncio.run、asyncio.gather、print、f-string |

【超前】标注集中区:asyncio.create_task/Task 对象调度、aiohttp 异步请求属【超前】,本日仅在注释/讲解识别,产物不实际使用(gather 自 v1.6 起为当日正式教学内容,不再列超前;更复杂的并发编排留后续周)。
硬约束复查:仅用 day26 闭包知识点 ✓ 第三方库合规(未使用,标准库 asyncio)✓ ≤120行 ✓ extra/命名正确 ✓

---

## Day27(周六,7h)· 综合项目实战:Markdown 批量处理器

今天是项目日,把本周四天(venv/requests/re/typing/asyncio)连同第03周的文件与异常拧成一个完整工具——这正是骨架固定产物「Markdown 批量处理器」,也是第07周 RAG"文档加载与清洗"的能力预演。产出:markdown_batch_processor.py,分层设计(获取/清洗/存储),批量把杂乱 md 清洗规整并落盘,单文件失败不影响整体。

💡 JS开发者速读:整体结构类似你写过的"批量处理管道"(读取→transform→写出),差异在持久化用文件而非浏览器存储、清洗用 Python re、批处理编排可选用 asyncio(而非 Promise.all)。序列化仍用手写字符串与文件读写(json 模块本周未首教,遵守闭包)。

### 学习内容(综合复用,无全新理论)

- 分层设计:获取层(读本地多个 .md / 可选 requests 抓取)、清洗层(re 去噪规整)、存储层(批量写盘)
- 用 typing 给各处理函数加类型标注(复用 day25)
- 用 re 清洗 Markdown(去 HTML 标签、规整标题、提取链接)(复用 day24)
- 用异常处理保障单文件读/写/解析失败时整体不崩(复用 week03)
- 可选:用 asyncio 编排批处理协程(复用 day26,gather 已于 day26 v1.6 转正教学),真异步文件 IO 属【超前】

### 讲解

结论先行:综合项目的关键是"分层解耦"——每层只干一件事、用 typing 标清输入输出契约、用异常兜住每个文件的失败。清洗规则用 re,批处理主循环用 for 遍历文件列表;若想练 asyncio,可用协程包裹每个文件的处理再顺序 await(真并发文件 IO 属【超前】)。下面只演示"分层骨架"的结构思路,**不是**产物答案,清洗与批量逻辑由你设计。

```python
# 分层结构演示(思路骨架,非产物答案):
import re
from typing import List

def clean(md: str) -> str:                 # 清洗层:一个规则示例
    return re.sub(r"]+>", "", md)       # 去 HTML 标签

def process_batch(files: List[str]) -> List[str]:   # 批处理层
    return [clean(f) for f in files]        # 推导式(week01)遍历

print(process_batch(["标题", "正文"]))
```

### 教材与章节

- 主教材:廖雪峰Python — **13.1 文件读写**(week03 承重技能复习的正式出处,2026-11-07 day27 检测由书根目录升级为具体小节;根目录仅留作全书导航入口,不得当锚点):(https://liaoxuefeng.com/books/python/io/file/index.html)
- 速查(均为本周已读页,复习即回查这些具体小节,勿整章重读):官方中文 re 模块(复习 day24):(https://docs.python.org/zh-cn/3/library/re.html) ;typing 模块(复习 day25,按需检索勿通读):(https://docs.python.org/zh-cn/3/library/typing.html) ;廖雪峰 15 正则(复习 day24):(https://liaoxuefeng.com/books/python/reg-exp/index.html) ;廖雪峰 23.2 使用asyncio(复习 day26,勿读 23.1/勿顺翻 23.3):(https://liaoxuefeng.com/books/python/async-io/asyncio/index.html)
- 语法速查:菜鸟教程 Python3:(https://www.runoob.com/python3/)

### 时间分配

| 时段      | 时长 | 内容                                                             |
| --------- | ---- | ---------------------------------------------------------------- |
| 学习/设计 | 2h   | 画分层结构图、想清清洗规则与异常场景、定 typing 契约(含英语 30min) |
| 项目实战  | 4h   | 编写 markdown_batch_processor.py,准备若干测试 .md 文件            |
| 复盘      | 1h   | 补 index.md,自检闭包合规,列可改进点,GitHub commit                |

### 当日产出

- [ ] 准备 学习产物/第04周/day27/ 下若干测试用 .md 源文件(含 HTML 标签/杂乱标题/链接等噪声,自己造数据)
- [ ] 编写 学习产物/第04周/day27/markdown_batch_processor.py:Markdown 批量处理器(项目日,≤150行)
  - 获取层:遍历指定目录下多个 .md 文件并读入(with open,week03);可选扩展——用 requests 抓取一个公开 md 源(标为可选,离线也能跑主路径)。注:列目录需 os.listdir/glob(标准库 os 本周仅"识别"未正式教,属【超前】最小片段——目录列表可在程序内硬编码文件名规避,或直接用硬编码列表起批,os 欲试用放 day27/beyond/,不判未教先用)
  - 清洗层:用 re 对每个文件做至少两项清洗(如去 HTML 标签、规整标题层级、提取或重写链接),用 typing 给清洗函数加参数与返回类型标注
  - 存储层:把清洗后的内容批量写入 output 子目录(文件名可加 _clean 后缀),并生成一个汇总(处理文件数、总字符数)print 出来
  - 健壮性:用 try/except 保证单个文件读/写/解析失败时 print 警告并跳过,不中断整批处理
  - python markdown_batch_processor.py 可跑通,演示"多文件读入→清洗→批量写出→汇总"完整闭环
  - 所用知识点清单:文件读写(open/with,week03)、异常全体系(week03)、re(sub/search/findall)、typing(List/Optional 等)、for/推导式、str 方法、可选 requests、可选 asyncio、print、f-string
- [ ] 补记 学习产物/第04周/day27/index.md:覆盖分层设计思路与全部学习内容

### JS→Python对照笔记

- JS 批处理管道 map(transform) → Python `[clean(x) for x in items]` 推导式
- JS localStorage/浏览器存储 → Python with open 写本地文件
- JS `Promise.all` 批量 → Python for 顺序处理 或 `asyncio.gather` 并发(复用 day26,非超前)
- JS JSON.stringify 序列化 → 本周手写字符串拼接与文件读写(json 模块未首教)

### 跟练清单(放extra/)

- extra_md_stats.py:读取一个本地 .md 文件,用 re 统计并 print——一级/二级标题(#)数量、Markdown 链接 `[]()` 数量、代码块 ``` 数量,练习正则计数。

### 当日验收(合规区)

| 学习内容                          | 教材章节                    | 当日产物                     | 产物所用知识点                                                                     |
| --------------------------------- | --------------------------- | ---------------------------- | ---------------------------------------------------------------------------------- |
| venv/requests/re/typing/asyncio + 文件/异常 综合应用 | 廖雪峰-文件/正则/异步;官方-re+typing | markdown_batch_processor.py | 文件读写、异常全体系、re、typing、for/推导式、str 方法、可选 requests/asyncio、print |

【超前】标注集中区:真异步文件 IO(aiofiles)、requests 异步替代(aiohttp/httpx)属【超前】,若产物涉及仅以最小片段出现并标注,不要求深入。注:asyncio.gather 不属超前(day26 已正式教学,本日为复用)。
硬约束复查:仅用 day27 闭包知识点 ✓ 第三方库合规(requests 已解禁,可选使用)✓ 项目日≤150行 ✓ extra/命名正确 ✓

---

## Day28(周日,7h)· 周检测 / 阶段1闸门 + 对账

今天是**阶段1闸门**(五个阶段闸门 day28/42/63/84/98 的第一个)。目标是限时独立完成一个"requests 抓取 + re 清洗提取 + 输出摘要"三合一的新闻摘要生成器,验证本周第三方库与实用技能已内化,同时检验你能否讲清 Python 与 JS 的关键差异(闸门附加要求)。通过后即平稳进入第05周(国产大模型 API)。

### 周检测(限时任务)

任务:45 分钟内,不看教材、不看本周产物,独立盲写 学习产物/第04周/day28/news_summary.py:

1. 用 requests 抓取一个自选公开新闻页面/接口(GET,必须设 timeout,检查 status_code 为 200 再继续)。
2. 用 re 从返回文本中清洗并提取正文或标题(如去 HTML 标签、抽取标题/关键段落),至少用到 findall/search/sub 中的一种以上。
3. 基于提取结果生成摘要(如取前 N 个字符或前若干句),print 输出摘要与其字符数。
4. 用 try/except 兜底网络异常(Timeout/RequestException)与解析异常,任一环节失败都 print 友好提示且程序不崩溃。
5. 主流程跑通一次完整"抓取→清洗→摘要→输出",每步有 print。

通过标准(须全部满足):

- 45 分钟内完成,`python news_summary.py` 一次跑通、无未捕获异常;
- 正确使用 requests(GET + status_code 检查 + timeout)与 re(至少一处提取或替换);
- 摘要输出合理(非空、来自真实抓取内容),异常分支有兜底;
- 仅用截至 day28 的闭包知识点,**可用第三方库 requests**(day22 已解禁),≤180 行(周末检测放宽);
- **阶段1闸门附加**:能口头/在 index.md 讲清 Python 与 JS 的至少三处差异(建议:包管理 venv/pip vs npm、类型 typing 运行时不强制 vs TS 编译期强制、异步 asyncio.run 手动启动 vs JS 事件循环内建)。

未通过补救方案:

- 仅个别 requests/re 写法出错 → 当天用缓冲 1h 对照 Day23/Day24 讲解订正,次日重盲写一次(≤45min);
- 抓取或清洗逻辑不通(拿不到正文/正则匹配不到)→ 重做 Day23 + Day24,再补一次盲写;
- 严重超时(>90min)或结构混乱 → 本周降级:第05周前 2 天先补 requests/re 欠账,再进入大模型 API,**阶段1闸门顺延但不取消**。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day22/env_check.py ☐ day22/requirements.txt ☐ day22/extra/extra_freeze_read.py ☐ day22/index.md ☐
   - day23/http_fetcher.py ☐ day23/extra/extra_headers.py ☐ day23/index.md ☐
   - day24/regex_cleaner.py ☐ day24/extra/extra_extract.py ☐ day24/index.md ☐
   - day25/typed_stats.py ☐ day25/extra/extra_typed_funcs.py ☐ day25/index.md ☐
   - day26/async_demo.py ☐ day26/extra/extra_coroutine.py ☐ day26/index.md ☐
   - day27/markdown_batch_processor.py ☐ day27/output/(清洗结果)☐ day27/extra/extra_md_stats.py ☐ day27/index.md ☐
   - day28/news_summary.py(检测产物)☐
2. 填 README 进度跟踪表:完成%/自评 1-5/卡点/补救(第04周行)。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 第05周前 2 天改补欠账。
4. 验收:每个 .py 必须 `python xxx.py` 跑通(env_check/http_fetcher/news_summary 需联网,离线时确认异常分支已兜底不崩);确认 day28 闸门附加的"Python vs JS 差异"已写入 index.md。

## 周尾附录:完整知识点累计清单(截至第04周day28)

第01-02周(已有):基础类型(int/float/str/bool/None)、print/input、f-string、控制流、for/while/range/enumerate/break/continue、字符串切片与方法、list/tuple/dict/set、推导式、切片进阶、生成器表达式、random.randint、datetime.date、def/docstring、参数全体系、lambda、map/filter、模块与包、import、闭包、nonlocal、装饰器概念。

第03周(已有):OOP(class/__init__/self、实例vs类属性、继承/重写/super()/多态、issubclass/isinstance/type)、魔术方法(__str__/__repr__/__eq__/__add__/__len__/__lt__)、文件读写(open/with、模式 r/w/a、encoding、read/readline/readlines/write、for line in f、strip)、异常全体系(try/except/else/finally、多异常捕获、as e、raise、自定义异常类)。

第04周(本周新增):

- 环境与依赖:venv 创建/激活、pip(install/--upgrade/uninstall/show/list)、pip freeze、requirements.txt 生成与 `pip install -r` 还原、第三方库解禁(day22 起)
- requests:get/post、params、timeout、status_code、headers、text、`.json()`、raise_for_status、requests.exceptions(Timeout/ConnectionError/RequestException)
- 正则 re:match/search/findall/sub/split、分组捕获 group()/groups()、字符类与量词(\d \w \s [] + * ? {m,n})、原始字符串 r""
- 类型提示 typing:参数/返回值注解、List/Dict/Tuple/Set、Optional/Union、Callable、"运行时不强制"特性
- asyncio:async def、await、asyncio.run(启动事件循环)、asyncio.sleep、asyncio.gather(并发对照,v1.6 转正)、协程不 await 不执行、顺序 vs 并发
- 【超前】识别项(不要求掌握):aiohttp/httpx、asyncio.create_task/Task 对象调度、aiofiles、re 命名分组/非捕获组/零宽断言、typing 的 TypedDict/Protocol/Generic、json 模块 dumps/loads

下周预告(第05周day29-35):国产大模型 API(通义千问/DeepSeek/GLM)、环境变量读 key(零硬编码)、Chat API 调用、Prompt 工程、结构化输出 JSON Mode。注:据 2026 市场修订版,阶段2 起 API **国产大模型优先**(通义千问/DeepSeek/GLM),并前移 Dify/Coze 低代码模块;本周 requests + typing + asyncio 正是调用大模型 API 与后续流式的直接地基。
