# day24 学习笔记(学习者本人填写)

## 今日主题
<待填写(题目查周教程 Day24「学习内容」段:re match/search/findall/sub/split/分组/字符类)>


### python 通过内置包 re,支持正则功能，查询、替换、修改字符串

1. 定义：
    r 是 raw string（原生/原始字符串） 的缩写， 的作用是让正则字符串中的反斜杠保持原样，减少双重转义，让正则更易读。
    ```python 
    s1 = "a\\nb"     # 3个字符层面是：a、换行符、b（\n 被转义成换行符）
	s2 = r"a\nb"    # 4个字符：a、\、n、b（原样保留）
    print(s1 ==s2) # True
    ```
2. 常用方法
    方法	        返回类型	                    说明
    re.match	    re.Match | None	            从开头匹配
    re.search	    re.Match | None	            全串找第一个
    re.fullmatch	re.Match | None	            整串完全匹配
    re.findall	    list[str] 或 list[tuple]	所有匹配，有无分组形状不同
    re.finditer	    Iterator[re.Match]	        惰性迭代器，逐个产出 Match
    re.sub	        str	                        替换后的新字符串
    re.subn	        tuple[str, int]	            (新字符串, 替换次数)
    re.split	    list[str]	                按模式切分
    re.compile	    re.Pattern	                预编译的正则对象
    re.escape	    str	                        转义特殊字符后的字符串
    re.purge	    None	                    清空内部缓存

    ```python
    import re
    m = re.search(r"(\d+)-(\d+)", "编号: 12-34")
    m.group()    # '12-34'  整体（= group(0)）
    m.group(1)   # '12'     第1组
    m.groups()   # ('12', '34') 所有组，元组
    m.start()    # 4  起始索引
    m.end()      # 9  结束索引
    m.span()     # (4, 9)
    ```

    re.sub(p, repl, s, count=0)	替换	新字符串
    re.subn(p, repl, s, count=0) 替换  与 sub() 相同，但返回新字符串和替换次数
    re.split(p, s, maxsplit=0)	按模式分割	列表
3. 分组
   ```python
    import re
   	# 基本分组 ()
	re.search(r"(\d{4})-(\d{2})", "2024-05").groups()   # ('2024', '05')
	# 命名分组 (?P<名字>...)
	m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "2024-05")
	m.group("year")     # '2024'
	m.groupdict()       # {'year': '2024', 'month': '05'}
	# 非捕获分组 (?:...) —— 只分组不提取
	re.findall(r"(?:ab)+", "abab")   # 匹配但不占组号
	# 反向引用：\1 引用第1组
	re.search(r"(\w+) \1", "hello hello")   # 匹配重复单词
   ```
    findall 大坑：模式里有 () 时，返回的是分组内容而非整体
    ```python
    import re
    text = "ID:12, ID:345"
    print(re.findall(r'ID:(\d+)', text))
    # ['12', '345']
    # 实际只返回括号里的数字，因为 (\d+) 是捕获组，findall 把完整匹配 ID:12 丢掉了。
    ```
4. 字符类 & 元字符
    写法	含义
    \d / \D	数字 / 非数字
    \w / \W	字母数字下划线 / 非
    \s / \S	空白 / 非空白
    .	任意字符（除换行，除非 re.S）
    [abc] / [a-z] / [^abc]	枚举 / 范围 / 取反
    [中]	中文字符也可放进类

5. 量词与贪婪
    ```python
    *      0次或多次        +   1次或多次
    ?      0或1次           {n} {n,} {n,m}
    *? +? ??  非贪婪（懒匹配，尽量少匹配）← 扩充00
    re.search(r"<.*>", "<a><b>")   # '<a><b>' 贪婪
    re.search(r"<.*?>", "<a><b>")  # '<a>'    非贪婪

    ```
6. 锚点
   ^  开头    $  结尾    \b 单词边界    \B 非边界
   \A 严格开头  \Z 严格结尾（不受 re.M 影响）
7. 环视断言
    (?=...)   正向先行：后面是
    (?!...)   负向先行：后面不是
    (?<=...)  正向后行：前面是（Python 要求定长）
    (?<!...)  负向后行：前面不是
    # 例：数字后面不能跟单位
    re.findall(r"\d+(?!px)", "12px 34em")   # ['34']
0
8. Flags
    flag	作用	记法
    re.I	忽略大小写	Ignorecase
    re.M	^$ 匹配每行首尾	Multiline
    re.S	. 也匹配换行	dotall
    re.X	允许写注释换行	verbose
    re.A	\d\w 只认 ASCII	ASCII
```python 
import re
re.findall(r"ab", "AB", flags=re.I)     # ['AB']
re.search(r"a.b", "a\nb", re.S)         # 匹配成功
```
1. sub 的进阶用法
```python
# 引用分组
re.sub(r"(\w+)@(\w+)", r"\2 的 \1", "tom@qq")  # 'qq 的 tom'
re.sub(r"(\w+)", r"\g<1>_x", "ab")             # \g<1> 更安全，防歧义
 
# repl 传函数（JS 同款玩法）
re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "a1b2")  # 'a2b4'
 
# 只替换第一次：count=1
re.sub(r"\d", "N", "a1b2", count=1)    # 'aNb2'
```


## JS→Python 对照
功能	JavaScript	Python
正则字面量	/re/g	无字面量，用 r"re" 字符串
判断是否匹配	/re/.test(str)	re.search(r"re", s) 非 None
第一个匹配	str.match(/re/) / re.exec(s)	re.search()（从头才用 re.match）
所有匹配	str.match(/re/g)	re.findall(r"re", s)
取分组	m[1]	m.group(1) ⭐
所有分组	m.slice(1)	m.groups()
命名分组	(?<name>...)	(?P<name>...)（多个 P！）
取命名分组	m.groups.name	m.group("name")
替换	str.replace(/re/, "x")	re.sub(r"re", "x", s) ⭐
替换引用分组	"$1"	r"\1" 或 r"\g<1>" ⭐
替换传函数	str.replace(/re/, fn)	re.sub(r"re", fn, s)
按正则分割	str.split(/re/)	re.split(r"re", s)
忽略大小写	/re/i	flags=re.I
多行模式	/re/m	flags=re.M
点号跨行	/re/s	flags=re.S
遍历匹配	re.exec + g + lastIndex 循环	re.finditer() 迭代（无需手动重置）⭐
动态构造正则	new RegExp(str)	re.compile(str)
查看模式串	re.source	pat.pattern
查看标志	re.flags	pat.flags

语义差异（易踩坑）：

差异点	JS	Python
替换范围	无 g 只换第一个	sub 默认全换，第一个需 count=1
match 的位置	无 g 时任意位置第一个	re.match 只认字符串开头
字符串中反斜杠	"\\d" 即可	建议 r"\d"，"\\d" 也行
split 含分组	捕获组保留在结果中	捕获组同样保留 ⭐
后行断言	现代浏览器支持变长	(?<=) 要求定长

## 常用模式速查表
```python
	import re
	# ① 邮箱
	r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
	re.findall(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text)
	# ② 中国手机号：1开头，第2位3-9，共11位
	r"1[3-9]\d{9}"
	re.findall(r"1[3-9]\d{9}", "电话13812345678")  # ['13812345678']
	# ③ 日期（2024-05-01 / 2024/5/1 / 2024.5.1）
	r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}"
	m = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", "2024-5-1")
	m.groups()   # ('2024', '5', '1')
	# ④ URL
	r"https?://[^\s]+"
	r"https?://(?:[\w.-]+)(?:/[\w./?%&=-]*)?"
	# ⑤ 去HTML标签（sub 的经典应用）
	re.sub(r"<[^>]+>", "", "<p>你好</p>")        # '你好'
	re.sub(r"<[^>]*>", "", s)
	re.sub(r"<.*?>", "", s, flags=re.S)          # 非贪婪 + 跨行版本

    # 中文提取
    r"[\u4e00-\u9fa5]+"
    
    # IP 地址（简单版 + 严格校验版）
    r"(\d{1,3}\.){3}\d{1,3}"
    r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
    
    # 18位身份证
    r"\d{17}[\dXx]"
    
    # 金额/数字（含负号、小数）
    r"-?\d+\.?\d*"
    
    # 十六进制颜色
    r"#[0-9a-fA-F]{6}"
    
    # 中文邮编 / QQ号
    r"[1-9]\d{5}"
    r"[1-9]\d{4,10}"
    
    # 清洗空白字符
    re.sub(r"\s+", " ", "a   b\n\nc").strip()
    
    # 密码强度（环视组合拳：大小写+数字+特殊字符，≥8位）
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$"
    
    # 千分位（环视经典题）
    re.sub(r"(?<=\d)(?=(\d{3})+$)", ",", "1234567")  # '1,234,567'
    
    # 重复词去重（反向引用）
    re.sub(r"\b(\w+) \1\b", r"\1", "hello hello world")  # 'hello world'
```

## 两行自检
- ①我说不出出处的知识点:无
- ②学了但没落进任何行为的知识点:
- match 、零宽断言、非捕获分组,fullmatch/finditer/flags 等

## 卡点与解决(非必填)
<可留空>
