urllib.request 详解
一、模块定位
urllib.request 是 Python 3 内置的用于打开和读取 URL 的核心模块（Python 2 时代的 urllib + urllib2 合并而来）。它属于 urllib 包，整个包分为四个子模块：
子模块	作用
urllib.request	打开和读取 URL，发送 HTTP 请求
urllib.error	捕获 request 抛出的异常
urllib.parse	解析、拆分、合并、编码 URL
urllib.robotparser	解析网站的 robots.txt（判断哪些内容可爬）
urllib.request 能处理认证验证、重定向、Cookie 等复杂场景，支持 HTTP/HTTPS/FTP 等协议。

二、urlopen()：最基础的请求
urlopen() 是模块的入口函数，类似“在浏览器输入网址后回车”：
import urllib.request

response = urllib.request.urlopen('http://www.baidu.com')
html = response.read().decode('utf-8')   # read() 返回 bytes，需手动解码
print(html)
函数签名与常用参数：
urllib.request.urlopen(url, data=None, timeout=..., 
                       cafile=None, capath=None, cadefault=False, context=None)
● url：目标网址（字符串或 Request 对象）
● data：有值则为 POST 请求（必须是 bytes 类型），为 None 则是 GET
● timeout：超时时间（秒）
● context：ssl.SSLContext 类型，用于指定 SSL 设置（如忽略未认证的 CA 证书）
返回值是一个类文件对象（http.client.HTTPResponse），支持文件对象的操作方法。

三、响应对象的常用属性和方法
import urllib.request

response = urllib.request.urlopen('http://www.baidu.com')

# —— 文件类方法 ——
response.read()        # 读取全部内容
response.readline()    # 读一行
response.readlines()   # 按行读取，返回列表
response.close()       # 关闭连接

# —— HTTP 信息 ——
response.status        # 状态码，如 200
response.reason        # 状态原因，如 OK
response.getheaders()  # 获取全部响应头
response.getheader('Server')  # 获取指定响应头
response.geturl()      # 返回实际请求的 url（重定向后的）
response.info()        # 返回 HTTPMessage 对象，包含响应头信息
状态码含义：1xx 进行中，2xx 成功，3xx 重定向，4xx 客户端错误（如 404），5xx 服务器错误。

四、Request 对象：定制请求
裸用 urlopen() 面对反爬机制（如校验 User-Agent）就不够用了。此时需要构造 Request 对象：
import urllib.request

url = 'http://www.baidu.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html'
}

req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
构造参数： Request(url, data=None, headers={}, method=None)
Request 对象的重要属性：
● full_url：完整请求 URL
● type：URL 协议类型（http/https 等）
● host：主机名（可能含端口）
● data：请求体数据
● method：HTTP 方法（GET/POST 等）

五、POST 请求：data 参数 + 编码
发送 POST 时，data 必须是 bytes，所以要先用 urllib.parse.urlencode() 编码：
import urllib.request
import urllib.parse

url = 'https://httpbin.org/post'
data = {'username': 'admin', 'password': '123456'}

# 关键两步：编码 -> 转 bytes
data = urllib.parse.urlencode(data).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={
    'User-Agent': 'Mozilla/5.0 ...'
})
response = urllib.request.urlopen(req)
print(response.read().decode('utf-8'))
记忆点：“data 有值即 POST，无值即 GET”；dict → urlencode() → .encode('utf-8') 才能传。

六、异常处理（配合 urllib.error）
爬虫必须捕获异常，否则网络一波动程序就崩：
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://www.example.com', timeout=5)
except urllib.error.HTTPError as e:
    # HTTPError 是 URLError 的子类，专指 HTTP 状态码错误（404、403 等）
    print('HTTP错误:', e.code, e.reason)
except urllib.error.URLError as e:
    # URLError：更底层的错误，如网络不通、DNS 解析失败、超时
    print('URL错误:', e.reason)
else:
    print(response.read().decode('utf-8'))
注意顺序：先捕获子类 HTTPError，再捕获父类 URLError，反了 HTTPError 永远捕获不到。

七、Handler 与 Opener：进阶玩法
当需要代理 IP、管理 Cookie 等操作时，就要用到处理器架构：
import urllib.request

# 代理示例
proxy_handler = urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
})
opener = urllib.request.build_opener(proxy_handler)

req = urllib.request.Request('http://www.baidu.com', headers={'User-Agent': 'Mozilla/5.0 ...'})
response = opener.open(req)
print(response.read().decode('utf-8'))
OpenerDirector 是请求处理的中枢，管理各种 handler 并执行实际的 URL 打开操作。urlopen() 本质上就是内部构建了一个默认 opener。
ProxyHandler 的代理效果
核心效果：一句话
让请求“绕道”代理服务器中转，目标网站接收到的访问 IP 变成代理 IP，从而隐藏本机真实 IP。
请求链路的变化
不用代理：  本机 ──────────────→ 目标网站
                            （网站看到你的真实 IP）

使用代理：  本机 ──→ 代理服务器 ──→ 目标网站
                ←── 代理服务器 ←──
                            （网站看到的是代理 IP）
原理是：请求目标网站之前先请求代理服务器，代理服务器代替你去访问目标网站，拿到数据后再转发回你的代码。
效果验证
用 http://httpbin.org/ip 可以直观验证（该网站专门用于查看 HTTP 请求参数）：
from urllib import request

# 不用代理：返回本机真实 IP
resp = request.urlopen('http://httpbin.org/ip')
print(resp.read().decode('utf-8'))

# 使用代理：返回结果变为代理 IP
handler = request.ProxyHandler({'http': '111.177.190.14:9999'})
opener = request.build_opener(handler)
resp = opener.open('http://httpbin.org/ip')
print(resp.read().decode('utf-8'))   # origin 字段变成代理 IP
实际带来的三大好处
1. 防止本机 IP 被封：很多网站会统计一段时间内同一 IP 的访问次数，频率不像正常人就封禁。用代理后，被封的是代理 IP，本机安全
2. 突破封禁后继续爬：一个代理 IP 被禁止，换一个代理接着爬，不影响任务
3. 配合 IP 池轮换：把多个代理组成列表，按时间策略随机切换使用，进一步降低被检测概率
生效范围：两种模式
# 模式一：仅 opener.open() 生效
response = opener.open(request)
# 只有通过这个自定义 opener 发出的请求走代理，
# urlopen() 发出的请求不受影响

# 模式二：全局生效
urllib.request.install_opener(opener)
# 之后所有请求（无论 opener.open 还是 urlopen）都走代理
还可以用“代理开关”模式灵活控制：
proxy_handler = urllib.request.ProxyHandler({'https': '27.191.234.69:9999'})
null_proxy_handler = urllib.request.ProxyHandler()   # 空代理

proxy_switch = True
if proxy_switch:
    opener = urllib.request.build_opener(proxy_handler)
else:
    opener = urllib.request.build_opener(null_proxy_handler)
需要注意的副作用
代理是“借道”，质量自然受中转服务器影响：
问题	说明
超时/连接失败	免费代理寿命短、速度慢、不稳定，失败时换 IP 或重试即可
常见报错	TimeoutError 10060（连接超时）、ConnectionResetError 10054（远程主机强制关闭）、URLError 10061（目标计算机拒绝连接）
匿名度分级	代理分透明、匿名、混淆、高匿四种类型，透明代理仍会暴露真实 IP，反爬场景选高匿代理
带认证的代理	付费私密代理格式为 'http://user:password@ip:port'
总结：ProxyHandler 的效果本质是改变请求的出口 IP——数据依然来自目标网站，但网站那边“看到的访问者”从你换成了代理服务器。这是爬虫对抗 IP 频率检测反爬机制的常用手段。

八、urlretrieve()：快捷下载文件
from urllib.request import urlretrieve

# 两行代码把网页/文件保存到本地
urlretrieve('http://www.baidu.com', 'baidu.html')

九、典型抓取流程总结
1. 分析目标 URL
2. 构造 headers（伪装 UA，绕过基础反爬）
3. Request 对象封装 url + headers（+ data 若为 POST）
4. urlopen() 发送请求
5. read().decode() 获取内容
6. urllib.error 捕获异常，保证程序不中断
7. 配合 urllib.parse 处理参数编码
学习建议：urllib.request 的价值在于①无外网环境下的应急方案；②理解 HTTP 请求的底层构造过程。日常写爬虫仍以 requests 为主力，但上面这套“Request → urlopen → read → decode → error 处理”的流程要能独立写出来。

这个问题问得挺本质的。其实 urlopen 和 opener.open() 不是两个完全不同的东西，urlopen 内部就是调用了 opener.open()，只是它用的是一个"默认的全局 opener"。

它们的关系

可以这样理解：

urlopen(url)
    ↓ 内部实际执行
全局默认 opener.open(url)

urlopen 是一个模块级别的便捷函数，它背后有一个由 urllib.request 自动构建好的默认 OpenerDirector，里面装了 HTTPHandler、HTTPSHandler、HTTPRedirectHandler 等基础处理器。

为什么要用 opener.open()

当你需要 Cookie、代理、认证等高级功能时，默认 opener 就不够用了。 你需要自己用 build_opener() 组装一个带特定 Handler 的 opener：

import urllib.request
import http.cookiejar

cookie_jar = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(handler)

必须用这个 opener 的 open()，因为它才绑定了 CookieJar
opener.open("https://example.com/login")

如果你这时候还调 urlopen()，它用的仍然是那个默认 opener，里面没有 HTTPCookieProcessor，Cookie 就不会被保存。

那能不能让 urlopen 也用自定义 opener？

可以，用 install_opener() 把自定义 opener 设为全局默认：

urllib.request.install_opener(opener)

之后 urlopen 也会走这个 opener
urllib.request.urlopen("https://example.com/profile")

不过一般不推荐这么做，因为 install_opener 是全局副作用，容易让代码变得隐晦。直接调 opener.open() 更清晰——看到 opener 就知道这个请求带了哪些能力。

一句话总结

urlopen = 用默认 opener 调 open()；opener.open() = 用你自己组装的 opener 调 open()。需要 Cookie、代理等功能时，必须用自定义 opener 的 open()，否则那些 Handler 根本不参与请求处理。

需要我为你梳理 OpenerDirector 中各 Handler 的协同处理流程，看看请求具体是怎么被处理吗？