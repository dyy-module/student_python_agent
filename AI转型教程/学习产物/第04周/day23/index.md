# day23 学习笔记(学习者本人填写)

> 口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段单独成块并标注语言。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
<待填写(题目查周教程 Day23「学习内容」段:requests GET/POST/状态码/超时/JSON/异常)>
### requests 是什么
python 用于处理请求的第三方包，基于urllib3 封装，使用起来更简洁,需要单独安装
自动处理了连接池、Keep-Alive、内容解码、JSON 序列化等所有底层细节

### 核心方法
```python
import requests

requests.get('https://api.github.com/events')          # GET
requests.post('http://httpbin.org/post', data={'k': 'v'})  # POST
requests.put('http://httpbin.org/put', data={'k': 'v'})    # PUT
requests.delete('http://httpbin.org/delete')           # DELETE
requests.head('http://httpbin.org/get')                # HEAD
requests.options('http://httpbin.org/get')             # OPTIONS

```

URL 参数：使用 params 字典，requests 会自动编码并拼接到 URL 上。值为 None 的键会被自动忽略，值可以是列表，会展开为多个同名参数

```python
import requests
try:
    payload = {'key1': 'value1', 'key2': ['v2', 'v3'], 'key3': None}
    r = requests.get('http://httpbin.org/get', params=payload,timeout=2)
    # 实际 URL: http://httpbin.org/get?key1=value1&key2=v2&key2=v3
except requests.exceptions.Timeout:
    print('超时处理')
except requests.exceptions.HTTPError as err:
    print(err.response.status_code) # err 请求的所有信息
```

### Response 对象：响应的统一接口
核心属性与方法：

|属性 / 方法|	作用	|说明
|-----|-----|-----|
|r.status_code |	HTTP 状态码 |	如 200、404。可用 r.status_code == requests.codes.ok 增强可读性。|
|r.text |	文本形式的响应体 |	自动根据响应头推断编码并解码。|
|r.content |	字节形式的响应体 |	适用于图片、文件等二进制数据。|
|r.json() |	将响应体解析为 | JSON	自动调用 json.loads()，失败会抛 JSONDecodeError。|
|r.headers |	响应头字典 |	大小写不敏感，可用 r.headers['content-type'] 或 r.headers.get('Content-Type')。|
|r.url |	最终请求的 URL|	在发生重定向后，此属性反映最终的地址。|
|r.request.headers |	实际发送的请求头|	用于调试，查看 requests 默认添加了哪些头。|

默认情况下，requests 不会因为 4xx 或 5xx 状态码而抛出异常。你需要显式调用 r.raise_for_status()，如果状态码表示错误（4xx/5xx），它会抛出一个 requests.exceptions.HTTPError 异常。

r.text 和 r.json() 区别

r.text：响应体经字符编码解码后的 str。你拿到的是“文本本身”，需要自己决定怎么解析
r.json()：对 r.text 调用 json.loads() 的结果，通常是 dict 或 list（也可能是 str、int、bool、None，取决于 JSON 顶层结构）。它做的是“结构化解析” 

#### 编码推断：r.text 最容易被忽视的细节
HTTP 响应头中的 charset（如 Content-Type: text/html; charset=gbk）——优先级最高。

若响应头无 charset，则回退到 chardet/charset_normalizer 库对响应体字节的探测结果。

对于 application/json 等类型，requests 在某些版本中会按 RFC 7159 优先使用 UTF-8。
```python
r.encoding           # 查看 requests 推断出的编码
r.apparent_encoding  # chardet 探测出的编码
r.text               # 用 r.encoding 解码的结果
```

如果服务器返回的 Content-Type 声明了错误的 charset（比如实际是 UTF-8 却声明成 ISO-8859-1），r.text 会出现乱码。此时可以手动修正：
```python
import requests

r = requests.get('http://www.baidu.com',timeout=2)
r.encoding = 'utf-8'
print(r.text)  # 现在正确了
```

#### r.json() 的解析行为
依赖 r.text：先解码成字符串，再解析。所以编码问题会传递过来。

严格性：JSON 规范要求字符串用双引号、不允许尾随逗号等。json.loads() 比 JavaScript 的 JSON.parse() 更严格（后者也不允许尾随逗号，但 Python 的 json 模块对 NaN/Infinity 默认宽容，可用 parse_constant 控制）。

失败即抛异常：响应体不是合法 JSON 时，抛 requests.exceptions.JSONDecodeError（它是 json.JSONDecodeError 的子类，Python 3.5+ 起 requests 会包装）。

不校验 Content-Type：即使响应头是 text/html，只要 body 是合法 JSON，r.json() 照样能解析成功。它不检查 Content-Type 是否为 application/json



### Session
requests.Session() 是 requests 最重要的高级特性，它同时解决了状态保持和性能优化两个问题。
状态保持：Session 会自动在跨请求间保持 Cookie、认证信息、默认请求头等。这使得“登录后访问后续页面”这类任务变得非常简单：
```python
import requests

with requests.Session() as s:
    s.post('https://api.example.com/login', data={'user': 'admin', 'pass': '123'})
    profile = s.get('https://api.example.com/profile').json()  # 自动携带登录 Cookie
```
性能优化：连接池与 Keep-Alive
每次使用 requests.get() 都是一次独立的请求，会经历完整的 TCP 握手和挥手过程。而 Session 底层维护着一个连接池，对同一主机的多个请求会复用已建立的 TCP 连接，避免了重复握手和 TLS 协商的开销，能带来显著的性能提升（后续请求可快数倍）


### 超时控制：连接超时与读取超时
永远不要省略 timeout 参数。requests 默认没有超时限制，一个挂起的请求会无限期阻塞你的程序
timeout 参数可以是一个数字，也可以是一个元组，二者含义完全不同:

连接超时（Connect Timeout）：等待 TCP 连接建立的最大秒数。应设置得较短（如 3~5 秒），因为网络可达性通常很快就能确定。

读取超时（Read Timeout）：连接建立后，等待服务器发送下一个字节的最大间隔秒数（注意：它约束的是相邻数据块之间的间隔，而非整个响应的总时长）。对于普通请求可设置 10~30 秒，对于流式下载大文件，可能需要设置到 120 秒以上。

```python
import requests

# 推荐：分别控制连接超时与读取超时
r = requests.get(url, timeout=(3.05, 15))  # 连接等 3.05 秒，读取间隔等 15 秒
```

### 其他关键配置
代理（Proxies）：通过 proxies 字典为不同协议指定代理服务器。
```python
import requests

proxies = {'http': 'http://10.10.1.10:3128', 'https': 'http://10.10.1.10:1080'}
requests.get('http://example.com', proxies=proxies, timeout=5)
```

### 异常处理

requests.ConnectionError |网络不通、DNS 失败、连接被拒绝 |检查网络、重试、告警
requests.Timeout |连接或读取超时 | 重试、增加超时时间
requests.HTTPError | 由 raise_for_status() 主动抛出（4xx/5xx）|根据 e.response.status_code 处理业务逻辑
requests.TooManyRedirects |重定向次数超过限制 |检查 URL 或服务器配置

### 重试机制：应对瞬时故障
对于网络抖动或服务端瞬时 5xx 错误，简单的重试能显著提升稳定性。requests 通过 HTTPAdapter 和 urllib3 的 Retry 类来配置自动重试。
```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(
    total=3,                     # 总重试次数
    backoff_factor=1,            # 指数退避：第1次等1秒，第2次2秒，第3次4秒...
    status_forcelist=[502, 503, 504],  # 对这些状态码进行重试
)
session.mount('https://', HTTPAdapter(max_retries=retries))
```

### json 模块
函数	方向	输入/输出
json.dumps(obj)	Python → JSON	返回 str
json.dump(obj, fp)	Python → JSON	写入文件对象 fp
json.loads(s)	JSON → Python	接受 str（或 bytes）
json.load(fp)	JSON → Python	从文件对象 fp 读取

```python
import json

data = {'name': '张三', 'age': 30, 'tags': ['a', 'b']}

s = json.dumps(data)          # '{"name": "\\u5f20\\u4e09", "age": 30, "tags": ["a", "b"]}'
obj = json.loads(s)           # 回到 dict

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open('data.json', encoding='utf-8') as f:
    obj = json.load(f)
```

## JS→Python 对照
  JS `axios.get(url,{params})` → Python `requests.get(url, params=)`
  JS `await res.json()` → Python `r.json()`(同步返回 dict,无 await)
  JS `res.status` / `res.headers` → Python `r.status_code` / `r.headers`
  JS axios 4xx/5xx 自动 reject → Python requests 不自动抛错,需 `r.raise_for_status()`
  JS fetch 超时靠 AbortController → Python `timeout=` 参数内建
  JS `.catch(err)` → Python `except requests.exceptions.RequestException as e`

## 两行自检
- ①我说不出出处的知识点:无
- ②学了但没落进任何行为的知识点: 
  - put/delate/head/options 请求
  - Session
  - 代理
  - 重试
  
except requests.exceptions.HTTPError 这个分支什么时候会被执行到？ 结合"非 2xx requests 不自动抛错"这条，说说你的产物里 404 会发生什么。
只有手动调用 r.raise_for_status() 且4xx 5xx 错误时才会抛出错误 HTTPError
2xx（成功）：不抛异常，正常返回 None
3xx（重定向）：不抛异常。因为 requests 默认会自动跟随重定向，raise_for_status() 检查的是最终响应的状态码只有在你显式设置 allow_redirects=False 时，才会看到 3xx 状态码，而它同样不会被 raise_for_status() 视为错误

with requests.get(...) as res:` 里的 with 起了什么作用？** 它和你 index.md 里记的with requests.Session() as s:的 with 是同一回事吗？（你 env_check/diary 里用的是with open，三种 with 放一起说清差异。）

共同的机制：上下文管理器协议
任何对象只要实现了 __enter__ 和 __exit__ 两个方法，就能用在 with 语句里

with open as f: 释放文件描述符
with requests.Session() as s：关闭整个连接池
```python
with requests.Session() as s:
    s.get(url1)
    s.get(url2)   # 复用同一连接池
# 退出时连接池被关闭，所有 Keep-Alive 连接被释放

```

with requests.get(...) as res:释放单个响应的连接
Response.__exit__ 调用 Response.close()，它做两件事

如果响应体尚未被完全读取（_content_consumed 为 False），关闭底层 urllib3 的 raw 连接。
调用 release_conn()，把连接释放回连接池（或关闭，取决于连接是否可复用）

### 关键陷阱：默认非流式下，这个 with 几乎是空操作
这是最容易误解的地方。requests.get() 默认 stream=False，意味着在 get() 返回之前，响应体已经被完整读取并缓存在内存中，连接也已经释放回池。等到 with 退出时：
_content_consumed 已是 True，跳过关闭 raw 连接；
release_conn() 是幂等的，连接早已释放，等于没做事。

真正让这个 with 有价值的场景是流式请求：
```python
with requests.get(url, stream=True) as res:
    res.raise_for_status()
    for chunk in res.iter_content(chunk_size=8192):
        process(chunk)
        # 如果中途 break 或抛异常
# 退出时 close() 会关闭未读完的 raw 连接，避免连接泄漏
#tream=True 时响应体没有被预读，连接处于“占用”状态。如果中途退出而不读完，不调用 close() 就会泄漏连接（连接无法复用也无法关闭，#直到 GC 兜底）。with 在这里是防泄漏的关键

```

## 卡点与解决(非必填)
<可留空>
