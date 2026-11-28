# day33 笔记

## 模型格式化输出。
模型参数：response_format = 'text'| 'json_object' | 'json_schema'

'text':
    默认值，文本输出，不保证任何结构。如何提示词里要求json格式，大概率会返回json字符串。
    但可能带  json  围栏、前后解释文字、尾随逗号、单引号，作为json解析不保险
'json_object': 
    1.的 Prompt 里必须出现 “json” 这个词,否则 API 会直接返回 400 错误
    2.能保证返回的一定是json,但不保障编造数据。模型依然可能自由发挥，添加不存在的键、遗漏必填字段、或者把数字写成字符串
    3.数据可能会空，需要逻辑兜底
'json_schema':
    1.本质底层也是调用的create。sdk 封装了“Pydantic 模型 → JSON Schema → API 请求 → Pydantic 对象” 过程
    2.一般用parse 请求，schema 通过 response_format 传入
    3.它是一套强制系统。你提供了完整的 Schema，模型在生成时被物理限制，只能输出完全符合该 Schema 的 token


## json_object 和 json_schema 本质差异
    底层机制：约束解码
    json_schema 之所以能提供 100% 的保证，是因为它在模型的采样层进行了拦截。
    推理引擎（Inference Engine）会把你的 JSON Schema 编译成一个有限状态机（FSM）或上下文无关文法（CFG）。在模型生成每一个 token 之前，引擎会检查当前状态，将所有会导致“违反 Schema”的候选 token 的概率屏蔽（logit masking） 掉（设为负无穷）。模型只能在剩下的、合法的 token 里选择。因此，从物理构造上，输出就不可能偏离你定义的轨道

### 实际差异
    json_object 的强制“咒语”：使用 json_object 时，你的 Prompt 里必须出现 “json” 这个词（不区分大小写），否则 API 会直接返回 400 错误。而 json_schema 没有这个限制。

    Refusal 字段：当模型因安全原因拒绝回答时，json_schema 模式会返回一个结构化的 refusal 字段，让你能优雅地处理拒绝；json_object 模式则可能返回一段难以解析的文本或格式错误的内容。

    SDK 集成：json_schema 与 Pydantic 深度集成，OpenAI SDK 的 .parse() 方法可以自动完成“Pydantic 模型 → JSON Schema → API 请求 → Pydantic 对象”的全流程。而 json_object 通常需要你手动 json.loads() 和 Model.model_validate()


- 疑问：为什么开json模式和不开json模式，返回的都是json。
- 答：因为提示词里明确要求了json格式。response_format=json_object 不是返回值是不是json的开关，是保证返回值一定是json。
    json_object：保证合法，json.loads 基本必过，高，适合程序直接解析
    text:"自觉"写的，可能带  json  围栏、前后解释文字、尾随逗号、单引号，会抛 JSONDecodeError，不保障json
    ！！！坑点，这里解析的是list,提示词最好把json list 的结构写清楚，防止意外回复，可能会导致 items 解析失败，做兜底容错

## max_tokens 与 JSON 截断
- 不设 max_tokens 不等于安全：服务端仍有默认上限，超出照样截断。
- 正确做法是按预期输出长度留余量，设一个足够大的合理上限，而不是不设。
- 截断的 JSON 是非法 JSON，json.loads 必抛 JSONDecodeError；可结合 finish_reason == "length" 判断是否被截断（day31 已学）。

## 两行自检
- ① 我说不出出处的知识点: 无
- ② 学了但没落进任何行为的知识点:空 content 兜底（DeepSeek 口径：输出无法被识别为 JSON 时，内容会被替换为空格，finish_reason 仍是 stop）——产物未对空 content 做判断或重试
