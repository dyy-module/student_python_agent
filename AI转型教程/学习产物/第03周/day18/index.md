# 第03周 · Day18 学习笔记

> 说明:本文件由学习者本人在完成当天学习后填写,须覆盖当日全部学习内容。口径:标 `python` 的代码块须纯 Python 且可直接运行;JS 片段允许,但须单独成块并标注语言。末尾须做行为-知识点自证表(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
open  操作文件函数，及对应操作符号
with 语句，帮助兼容报错，自动调用close。
read/readline/redelines 文件读取方法
write/writelines 写入文件方法
遍历文件 for l in f:


## 知识点小结

open(file,mode='r',buffering=-1,encoding=None,error=None,newline=None,closefd=True,opener=None)
----常用------
file: 必需，文件路径（相对或者绝对路径）。
mode: 可选，文件打开模式
encoding: 一般使用utf8
----偶尔用----
errors: 报错级别
脏数据兜底，别让一个坏字符炸掉整个任务

```python
	open('legacy.txt', encoding='gbk')                    # 默认 strict → 整个读取失败
	open('legacy.txt', encoding='gbk', errors='ignore')   # 丢弃坏字符
	open('legacy.txt', encoding='gbk', errors='replace')  # 替换成 �，至少能定位问题
```

newline: 区分换行符。 CSV 空行、跨平台换行符

```python
	# ❌ 错误：Windows 下产生空行
	import csv
	with open('data.csv', 'w', encoding='utf-8') as f:
	    csv.writer(f).writerow(['姓名', '年龄'])
	    # csv 模块自己写 \r\n，文本模式又把 \n 转成 \r\n
	    # → 实际写入 \r\r\n → Excel 打开全是空行
	# ✅ 正确：官方文档钦点的惯例
	with open('data.csv', 'w', newline='', encoding='utf-8') as f:
	    csv.writer(f).writerow(['姓名', '年龄'])
```

----特殊需求----
buffering: 设置缓冲 .日志实时性、性能调优
要实时（tail -f 盯日志）：buffering=1 或关键点 flush()
要性能（百万次小写入）：调大如 buffering=65536
日常读写文件，默认 -1 不用动。

----基本不用-----
closefd: 传入的file参数类型.仅当 file 参数传的是整数文件描述符时才生效，决定 f.close() 时是否连底层描述符一起关掉：
opener: 设置自定义开启器，开启器的返回值必须是一个打开的文件描述符。 创建敏感文件时收紧权限（token、密钥、密码文件）：

mode参数:
r:读取 
r+ 读取文件，文件指针放在开头。
rb:读二进制
rb+：二进制，其余参考r
w:写入，如果文件存在，覆盖原内容，如果不存在，创建文件并写入
w+: 写入的同时，能够读取
wb:二进制写
wb+: 二进制读写
a:追加写。如果文件存在，在文件结尾追加，如果没有，创建文件
a+:a的基础上，可读
ab:二进制追加
ab+: 二进制追加，可读

read:读取整个文件
readline：一次只读取一行
readlines: 一次性按行读取文件，返回一个数组

write:文件写入，只能写字符串
writelines: 传入数组，一次性可写入多个内容。！！！坑点：输入的内容不会自己换行，换行还是需要换行符。只能接收字符串

with: 语法糖，主要帮助自动close 打开的文件，捕获错误
```python
    try: # try finally 超前
        f = open('/path/to/file', 'r')
        print(f.read())
    finally:
        if f:
            f.close()

    #等价于
    with open('/path/to/file', 'r') as f:
        print(f.read())
```

可以通过 for 循环便利文件每一行，惰性读取

## JS→Python 对照
- JS fs.readFileSync(p,'utf8') → Python with open(p, encoding='utf-8') as f: f.read()
- JS fs.writeFileSync(p,s) → Python with open(p,'w',encoding='utf-8') as f: f.write(s)
- JS 手动fd.close() → Python with自动关闭
- JS line.trim() → Python line.strip()
  
  nodejs写的比较少，暂时只知道教程对比

## 卡点与解决(非必填)
无

## 行为-知识点自证表(交检硬项 · 内容本人填)

> 行=file_reader.py / extra_diary.py 里的一个行为;3 列;表外补一行「当日学了但没落进任何行为的知识点」。用方法/行为名定位,不写行号(加代码行号会漂)。

| 行为 | 用到的知识点 | 其中我说不出出处的 |
|---|---|---|
|file_reader write_art，  |open w 一次性创建/复写文件|---|
|file_reader write_art_lines，  |open a 追加文件内容|---|
|file_reader write_art_lines，  |writelines 一次写入多个内容|---|
|file_reader read_art  |open r 读取文件|---|
|file_reader sum_art  |for 循环  获取文件内容数组，根据数组做统计|---|
|file_reader  file_a.write_art_lines(['这是一行','并不会换行','\n换行得加换行符'])  |测试writelines 多个内容不会自动换行，得写入换行符。只能接收字符串|---|

表外一行(学了但没落进任何行为的知识点):
with 的触发时机。__enter__ 函数触发后，返回self  as赋值 ,无论正常/或报错关闭，都会触发__exit__

## 今日越界索引(可选,不写不算欠项)
> 越界内容放 day18/beyond/ 即留痕,不在这载四栏;这里最多留一行文件名索引。
- (可选)beyond/with.md 内:with 相关
