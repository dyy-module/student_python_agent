# ===== day24 产物任务说明 v3(实现由你本人盲写于本注释下方) =====
# 文件:regex_cleaner.py | ≤120 行 | 第三方库:无(标准库 re);re 本日首教
#
# 【需求】文本清洗与抽取器:对一段内置含噪声文本(混 HTML 标签、多余空白、邮箱、手机号)做四种正则操作
#   1 用 re.findall 提取全部邮箱并 print(结果是一个 list)
#   2 用 re.search + 分组把手机号拆成"号段"与"尾号",分别 print(m.group(1)/group(2))
#   3 用 re.sub 完成两件事:去掉 HTML 标签、把手机号中间四位脱敏为 *,各 print 结果
#   4 用 re.split 按空白/标点把文本切成词列表并 print 数量(len)
#   自证:python regex_cleaner.py 跑通、每步有可见 print、四类操作结果都对得上内置文本
# 【可用知识点】re.findall、re.search、re.sub、re.split、分组 group()/groups()、字符类(\d \w \s [] )、量词(+ * ? {m,n})、原始字符串 r""、str 方法、for、len、print、f-string
# 【越界→隔离目录】命名分组 (?P<name>...)、非捕获组 (?:...)、零宽断言 (?=)/(?!)、re.compile 预编译 属【超前】,本周仅识别,想试放 day24/beyond/,不写进交检产物
# 【教材·只读N节,读完即停】
#   廖雪峰 正则(match/split/group/compile):https://liaoxuefeng.com/books/python/reg-exp/index.html
#   ⚠ 该页不教 findall/sub,此两点查官方 re 模块页 https://docs.python.org/zh-cn/3/library/re.html 的 findall / sub 小节
# 【交检】跑通、每步 print;index.md 末两行自检;写模式一律加 r 前缀(勿漏,否则反斜杠被转义)
# 【加分可选】把邮箱/手机号正则做成"能匹配样例、也拒绝明显非法串"的更严谨版(文字说明取舍写进 index)
# ================= 以下开始盲写(壳不得改动下方实现行) =================
import re


def regex_clean(text):
    '''清洗文本'''
    email_re = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_re = r'(?<!\d)(1[3-9][0-9])[0-9]{4}([0-9]{4})(?!\d)' #【超前】 
    html_tag_re = re.compile(r'<[^>]+>')

    emails = re.findall(email_re, text)
    print(" 邮箱列表:", emails)
    f_phone = re.search(phone_re, text)
    if f_phone:
        print('号段：', f_phone.group(1), '尾号：', f_phone.group(2))

    no_comment = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    no_tags = html_tag_re.sub('', no_comment)
    no_tags = no_tags.replace('&nbsp;', ' ')
    print("去标签后:", no_tags)

    masked = re.sub(phone_re, r'\1****\2', no_tags)
    print('脱敏后:', masked)

    words = [w for w in re.split(r'[^\w]+', no_tags) if w]
    print("词列表:", words, "词数量:", len(words))


if __name__ == '__main__':
    test = ''' 
<section id="contact-list"  class="panel  dirty">
  <h2>  联系人清单&nbsp;&nbsp;（内部资料） </h2>

  <p>客户一：<b>张三</b>，邮箱：<a href="mailto:zhangsan@example.com">zhangsan@example.com</a>；
     手机：<span data-phone="13812345678">13812345678</span></p>

  <p>客户二：李四，邮箱 <i>li.si+test@mail.example.cn</i>；
     电话 15900001111；订单号 913812345678（不是手机号）</p>

  <!-- 历史备注：王五 wang_wu@corp-domain.com ，手机 18688889999 -->
  <div style="margin: 0;  padding: 12px;">
     客服邮箱：service@example.org&nbsp;&nbsp;&nbsp;
     备用邮箱：ops_team@sub.example.co.uk
     <br/>
     无效示例：name [at] example.com ；400-800-1234 不是手机号；编号 12345678901。
  </div>
</section>
'''
regex_clean(test)
