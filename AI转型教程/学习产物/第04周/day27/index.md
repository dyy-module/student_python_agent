# day27 学习笔记(学习者本人填写)

> 口径:标 `python` 的代码块须纯 Python 且可直接运行。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
<待填写(综合项目日:分层 获取/清洗/存储 的 Markdown 批量处理器,复用 venv/requests/re/typing/asyncio + week03 文件异常)>
1. 环境 venv
    - 创建环境 python -m venv .myenv
    - 激活环境:
        cd 文件夹，
        window:script/activate
        mac/liniux:source bin/activate
    - 撤销激活：deactivate
    - 安装不同的包：python -m pip install packageName
    - 导出配置 pip freeze > requirements.txt
     window坑：需注意powershell 版本大于等于7
2. 标准请求模块 urllib, 三方同步请求模块 requests，异步请求模块httpx
    urllib 模块
    request 模块 request.urlopen(url, data=None, timeout=..., cafile=None, 
    capath=None, cadefault=False, context=None)
    
    error 模块 状态错误： HTTPError， 底层错误：URLError
    parse：参数解析/编码 parse.urlencode(data).encode('utf-8')

    requests 请求
    requests.get(url)
    requests.post(url,data={}) # put delete,head,options

    返回值response：
    status_code: 状态码
    text 文本响应体
    content 二进制响应体
    json() json响应体，本质是text自动调用json解析
    headers 响应头
    url 真正的链接，可能是重定向后的
    request.headers 实际发送的请求头

    Session 用来处理登录态
    with requests.Session() as s: 后续使用s请求，会自动处理

    timeout 超时一定要设置，不然可能会永久挂起，阻塞进程，浪费资源

    异常处理：
    TooManyRedirects 重定向次数超过限制
    HTTPError http 状态错误，需手动 raise_for_status() 调用
    Timeout 超时错误
    ConnectionError 网络不通、DNS 失败、连接被拒绝 |检查网络

    json 模块
    函数	方向	输入/输出
    json.dumps(obj)	Python → JSON	返回 str
    json.dump(obj, fp)	Python → JSON	写入文件对象 fp
    json.loads(s)	JSON → Python	接受 str（或 bytes）
    json.load(fp)	JSON → Python	从文件对象 fp 读取
3. 类型注释 typing
    基础类型 str int float bool
    typing.Dict[str,int] # [key,value]
    typing.Tuple[str,...]
    typing.Optional[str] #3.15 str | None
    typing.Union[str,int] str|int
    自定义字典 typing.TypedDict class CostomClass(TypedDict):... 通过继承定义
    typing.Callable[[str],str] # 第一个参数[]是入参类型，单入参也需要[]。第二个是出参类型

    需要精确表达复杂签名时，用 Protocol 定义 __call__：[超前]
    class AreaFn(Protocol):
        def __call__(self, *, width: float, height: float = 1.0) -> float:
            pass

4. 正则表达式re
   方法：
    re.match(re_str，data) // 必须在位置 0 ，结束位置任意 返回Match |None
    re.fullmatch(re_str，data) // 必须在位置 0 ，到结尾结束， 返回Match |None
    re.search(re_str，data) // 全文任意位置开始匹配，结束匹配， 返回Match |None

    re.findall(re_str，data) // 多个，返回list,如果有分组，返回的是分组内容
    re.finditer(re_str，data) // findall 的迭代器版本，逐个产出Match
    re.sub(re_str,new_str,data，count=0) // 替换后的新字符串 返回str count 可设置替换几个
    re.subn(re_str,new_str,data，count=0) //(新字符串, 替换次数) tuple[str, int]
    re.split(re_str,data) // 切割字符串
    re.compile(re_str) // 预编译，用于多次复用re串，提升性能

    re.escape //转义特殊字符后的字符串 不常用
    re.purge // 清空内部缓存 不常用

    Match 对象
    m.group() == m.group(0) // 返回匹配到的整串
    m.group(1) //返回匹配到的第一个分组
    m.groups() // group元组
    m.start() // 开始位置
    m.end() // 结束位置

    内置字符
    \d 数字 | \D 非数字
    \w 字母数字下划线 | \W 取反
    \s 空白() | |S 取反
    . 任意字符
    [a-zA-Z0-9/><]合集

    分组
    m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-05")
    ?P<year> 为组名
    m.groupdict()       # {'year': '2024', 'month': '05'}
    非捕获分组 (?:...) —— 只分组不提取
    re.findall(r"(?:ab)+", "abab")   # 匹配但不占组号
    反向引用：\1 引用第1组
    re.search(r"(\w+) \1", "hello hello")   # 匹配重复单词

    量词与贪婪
    * 贪婪0或多次 
    + 1次或多次
    ? 0次或1次
    *? +? ?? 非贪婪（懒匹配，尽量少匹配）

    锚点
    ^ 开头 $结尾 \b 单词边界 \B 非边界
    \A 严格开头 \Z严格结尾 （不受 re.M 影响）

    断言：
    (?=...) 正向先行:后面是
    (?!...) 负向先行：后面不是
    (?<=...) 正向后行：前面是
    (?<!...) 负向后行：前面不是

    Flags
    re.I	忽略大小写	Ignorecase
    re.M	^$ 匹配每行首尾	Multiline
    re.S	. 也匹配换行	dotall
    re.X	允许写注释换行	verbose
    re.A	\d\w 只认 ASCII	ASCII


5. 异步I/O asyncio
    定义 async def ... 不用run触发，直接调用不执行
    异步 await
    触发调用 asyncio.run(coroutine)
    asyncio.sleep() 协程
    time.sleep() 同步

## 分层设计思路
<待填写:三层各干什么、typing 契约怎么标、单文件失败如何处理>
清洗层，专注清洗各类数据
存储层：处理读取/写入数据
健壮层：使代码更健壮，不至于报错宕机

根据函数出入参类型，标注typing
单文件失败，打印提醒，不崩溃，

## 两行自检
- ①我说不出出处的知识点:无
- ②学了但没落进任何行为的知识点:
- 异步io 、urllib

## 卡点与解决(非必填)
<可留空>
