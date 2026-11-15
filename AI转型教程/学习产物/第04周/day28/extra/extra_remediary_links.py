# ===== day28 补救加练(非闸门评分项;换角度练同一闭包 requests+re+异常+结构化输出) =====
# 文件:extra_remediary_links.py | 位置:day28\extra\ | ≤120 行 | requests 可用(day22 解禁)
# 【题目】换个提取目标再走一遍 抓取→清洗→提取→输出:
#   1 requests GET 抓阮一峰《科技爱好者周刊》任一文章页(必须设 timeout,先判 status_code==200 再继续)
#   2 用 re 提取正文里全部 <a> 链接的 href 与锚文本(findall 多组返回元组 / finditer 返回 Match,择一,别把元组当 Match),print 链接总数
#   3 用 re.sub 把 HTML 实体(&nbsp; / &#160; 等)替换成空格,再压缩多余空白与空行
#   4 生成结构化摘要(标题清单 + 链接计数),print 摘要本身"及其字符数"(len,别只截断不报数)
#   5 try/except 兜 Timeout/HTTPError/RequestException;并守"提取结果为空 / 上游函数返回 None"再往下走(拔网或正则没匹配都不崩)
#   6 结果另存 .txt(不是 .md),每步有 print
# 【越界→隔离目录】禁 import json/bs4;aiohttp/httpx/asyncio.gather 属【超前】→ 放 day28/beyond/
# 【教材·只读】回查 requests 廖雪峰页、re 官方页 https://docs.python.org/zh-cn/3/library/re.html
# 【交检】python 跑通无未捕获异常;摘要与链接计数非空且来自真实抓取;顺带回填主 day28 index.md 第②行自检
# ================= 以下盲写(勿改动本注释) =================
