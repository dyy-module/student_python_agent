# urllib 是什么
python  标准库中用于处理 URL 的核心模块包。
四个核心：request、parse、error、robotparser

## request
用于打开和读取 URL。它提供了基础的 urlopen() 函数，以及更复杂的 Request 类来处理请求头、数据等

1. urllib.request.urlopen(url, data=None, [timeout, ]*, context=None)
    urllib.request 模块采用 HTTP/1.1 协议，并且在其 HTTP 请求中包含 Connection:close 头部信息
    url：请求地址，返回 request 对象
    data：
        传参对象，一旦传入data,urlopen 默认变成post
        数据必须是 bytes 类型，通常是经过 urllib.parse.urlencode() 编码的表单数据

    timeout：单位秒，请求超时设置，不设置可能会完全丢失请求
    context：
        context 参数必须是一个 ssl.SSLContext 实例。这个实例对象封装了 SSL/TLS 协议的各种参数，例如证书验证策略、使用的 TLS 版本、加密套件等。当你需要访问一个 HTTPS 网址时，urllib 就会使用这个 context 对象来建立安全的连接。

        context参数的核心作用是定制化 HTTPS 连接的安全行为。默认情况下，urlopen 会使用 Python 的默认安全设置，通常会严格验证服务器证书。但在某些特定场景下，你需要通过 context 来改变这一行为：
        场景一：访问使用自签名证书或测试证书的服务器
        场景二：为客户端指定自定义的 CA 证书包
        场景三：进行客户端证书认证（双向 TLS）

        仅对 https 生效

2. urllib.request.Request(url, data=None, headers={}, method=None)
   当需要添加请求头、明确指定方法或发送 POST 数据时，就需要使用 Request 对象来封装请求信息
   ```python
    import urllib.request
    import urllib.parse

    data = urllib.parse.urlencode({'key': 'value'}).encode('utf-8')  # 编码为 bytes
    req = urllib.request.Request('https://httpbin.org/post', data=data, method='POST')
    with urllib.request.urlopen(req) as response:
        print(response.status)
   ```

### 扩展引擎：OpenerDirector 与 Handler
    urlopen() 实际上是在内部构建了一个默认的 OpenerDirector（简称 opener），并调用它的 open() 方法

    OpenerDirector：负责调度和协调各个 Handler
    Handler：每个处理器负责一项具体任务。例如，HTTPHandler 处理 HTTP 协议，HTTPSHandler 处理 HTTPS，ProxyHandler 处理代理，HTTPRedirectHandler 处理重定向，HTTPCookieProcessor 处理 Cookie。

    自定义 Opener 的用途：
    当你需要代理、身份认证、自定义 Cookie 策略等默认 urlopen 不支持的功能时，就需要手动构建 OpenerDirector 并添加相应的 Handler。
    
    ```python
    import urllib.request

    # 1. 构建携带特定 Handler 的 opener
    proxy_handler = urllib.request.ProxyHandler({'http': 'http://proxy.example.com:8080'})
    opener = urllib.request.build_opener(proxy_handler)

    # 2. 使用这个 opener 来发请求
    with opener.open('http://example.com') as response:
        print(response.read()[:100])
    ```
`urllib.request.ProxyHandler` 代理请求，走代理服务器中转
`urllib.request.build_opener` 创建opener
你也可以通过 `urllib.request.install_opener(opener)` 将这个自定义 opener 设置为全局默认，之后所有的 urlopen() 调用都会使用它

## parse
用于解析和构建 URL，例如拆分 URL 的各个组成部分（协议、域名、路径、查询参数），或对查询字符串进行编码/解码
```python
from urllib.parse import urlparse, urlsplit

url = "https://user:pass@www.example.com:8080/path/to/page?key=value#frag"

parsed = urlparse(url)
print(parsed.scheme)    # 'https'
print(parsed.netloc)    # 'user:pass@www.example.com:8080'  (网络位置)
print(parsed.path)      # '/path/to/page'
print(parsed.query)     # 'key=value'
print(parsed.fragment)  # 'frag'
```

urlparse 与 urlsplit 的区别：urlparse 的结果对象额外包含一个 params 属性（路径中最后一个 ; 之后的部分，是早期 URL 规范遗留的特性）。urlsplit 不解析 params，将这部分保留在 path 中。

函数	返回类型	是否含 params
urlparse(url)	ParseResult	✅ 有 params 属性
urlsplit(url)	SplitResult	❌ 无 params，其内容归入 path
实践中 params 几乎不再使用，所以 urlsplit 更轻量、更常用。另外，两者都支持通过 scheme、allow_fragments 等参数控制解析行为。

### 查询字符串解析：parse_qs / parse_qsl
```python
from urllib.parse import parse_qs, parse_qsl

query = "name=alice&age=30&tag=py&tag=web"

parse_qs(query)   # {'name': ['alice'], 'age': ['30'], 'tag': ['py', 'web']}
parse_qsl(query)  # [('name', 'alice'), ('age', '30'), ('tag', 'py'), ('tag', 'web')]
```
parse_qs 返回字典，每个键的值是列表（因为同一参数可能出现多次）。

parse_qsl 返回元组列表，保留原始顺序，适合需要顺序或允许重复键的场景。

二者都默认会解码（unquote）键和值，可通过 keep_blank_values、strict_parsing 等参数调整行为

### 构建与编码：urlencode / quote / unquote /quote_plus/unquote_plus
```python
from urllib.parse import urlencode

params = {'name': '张三', 'age': 30, 'tags': ['a', 'b']}
urlencode(params)              # 'name=%E5%BC%A0%E4%B8%89&age=30&tags=%5B%27a%27%2C+%27b%27%5D'
urlencode(params, doseq=True)  # 'name=%E5%BC%A0%E4%B8%89&age=30&tags=a&tags=b'
```
doseq=True：当值是可迭代对象（如列表）时，会为每个元素生成一个同名参数。处理多值参数时必须加上这个参数，否则会把列表的 repr 字符串整体编码进去
它内部使用 quote_plus，因此空格会被编码成 +

uote / quote_plus：对 URL 的单个组件（路径段、查询值等）进行百分号编码。
```python
from urllib.parse import quote, quote_plus

text = "a b/c?d=e"
quote(text)        # 'a%20b/c%3Fd%3De'  (空格 → %20，/ 默认不编码)
quote(text, safe='')  # 'a%20b%2Fc%3Fd%3De' (连 / 也编码)
quote_plus(text)   # 'a+b%2Fc%3Fd%3De'   (空格 → +)
```
safe 参数：指定哪些字符不编码，默认 '/'。构造路径段时通常保持默认；构造查询值时可能希望把 safe=''。

quote_plus 与 quote 的核心差异：前者把空格编为 +，符合 HTML 表单提交的 application/x-www-form-urlencoded 约定；后者编为 %20，更通用。urlencode 内部用的是 quote_plus。

unquote / unquote_plus：上述操作的逆过程，把 %XX 序列（以及 +）还原为原字符

### URL 拼接：urljoin
```python
from urllib.parse import urljoin

base = "https://example.com/docs/guide/index.html"

urljoin(base, "page2.html")       # 'https://example.com/docs/guide/page2.html'
urljoin(base, "../api/ref.html")  # 'https://example.com/docs/api/ref.html'
urljoin(base, "/root.html")       # 'https://example.com/root.html'
urljoin(base, "//cdn.com/x.js")   # 'https://cdn.com/x.js'
urljoin(base, "?q=1")             # 'https://example.com/docs/guide/index.html?q=1'
urljoin(base, "https://other.com")# 'https://other.com'  (已是绝对 URL，原样返回)

```
## error
包含了由 urllib.request 抛出的异常类（如 URLError, HTTPError），用于错误处理
```python
    OSError
└── URLError                    # 所有 urllib 请求错误的基类
    ├── HTTPError               # HTTP 协议层面的错误（如 404、500）
    └── ContentTooShortError    # 下载内容长度不足
```
HTTPError :
HTTPError 是 URLError 的子类，但它有一个特殊之处：它同时也是一个合法的响应对象。当服务器成功返回了一个 HTTP 响应，但状态码表示错误（通常是 4xx 或 5xx）时，urlopen 会抛出 HTTPError

400	Bad Request	请求参数格式错误
401	Unauthorized	缺少或无效的认证信息
403	Forbidden	服务器拒绝访问（如反爬、权限不足）
404	Not Found	资源不存在
405	Method Not Allowed	用了不该用的 HTTP 方法
429	Too Many Requests	触发限流，需退避重试
500	Internal Server Error	服务器端代码出错
502	Bad Gateway	上游服务器返回无效响应
503	Service Unavailable	服务暂时不可用（维护、过载）
504	Gateway Timeout	上游服务器超时


### 与 http.client 异常的边界
urlopen() 阶段的错误 → 包装为 URLError / HTTPError
读取响应体（resp.read()）阶段的错误 → 抛出 http.client.HTTPException 的子类（如 IncompleteRead），不会被包装成 URLError

```python
import http.client
import urllib.error

try:
    with urllib.request.urlopen(url) as resp:
        data = resp.read()  # 这一步可能抛 http.client.IncompleteRead
except http.client.HTTPException as e:
    # 需要单独捕获 http.client 的异常
    print(f"读取响应时出错: {e}")
```

## robotparser
用于解析网站的 robots.txt 文件，以判断爬虫是否有权限访问特定路径\
robots.txt 是放在网站根目录下的纯文本文件（如 https://example.com/robots.txt），用简单的指令告诉爬虫哪些路径可以抓、哪些不能抓

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url('https://example.com/robots.txt')  # 设置 robots.txt 地址
rp.read()                                      # 发起 HTTP 请求获取并解析

# 第二种写法
rp = RobotFileParser('https://example.com/robots.txt')
rp.read()
```
read() 的内部行为：

它会用 urllib.request.urlopen() 去请求 robots.txt（默认超时由全局 socket 设置决定，可通过继承重写 read() 来加超时）。

根据 HTTP 响应状态码决定策略（见下文“状态码语义”）。

如果获取失败（网络错误等），会静默吞掉异常，将内部状态标记为“无法获取”，后续 can_fetch() 默认返回 False（即禁止）

离线解析：如果已经拿到 robots.txt 文本，可以用 parse() 直接传入行列表，避免发网络请求：
```python
rp = RobotFileParser()
lines = [
    "User-agent: *",
    "Disallow: /private/",
]
rp.parse(lines)
```

### 核心方法：can_fetch(useragent, url)

```python
rp = RobotFileParser('https://example.com/robots.txt')
rp.read()

print(rp.can_fetch('*', 'https://example.com/public/page.html'))   # True
print(rp.can_fetch('*', 'https://example.com/private/data.html'))  # False
print(rp.can_fetch('BadBot', 'https://example.com/anything'))      # False
```

User-Agent 匹配：按 robots.txt 中 User-agent 行出现的顺序，找到第一个与传入 useragent 子串匹配的组（不区分大小写）。若没有精确/子串匹配，则使用 User-agent: * 组。

路径匹配：在选定的组内，检查 URL 的路径部分是否以某个 Disallow 规则开头。

最长匹配优先：如果多条规则都匹配，最长的那条规则胜出；长度相同时，Allow 优先于 Disallow。这是 robots.txt 规范（RFC 9309）的约定，Python 的实现遵循了这一点。

空规则：Disallow: 后面为空表示允许所有；Disallow: / 表示禁止所有。