# day31 笔记(学习者本人填写)

## 本日主题
多轮对话：
    ai没有记忆，需要人工把上下文一次性通过messages 投喂给它来实现多轮对话
    role 类型： 
        system:系统身份，一般在开头使用定语设置 角色/规则/行为
        user:用户输入的信息
        assistant: 模型返回的内容，加入message,实现对话上下文
    temperature：float 采样温度，控制模型的随机性。值0-1。越小两次一样的问题回答的越相似，越大随机性越大。每个模型可设置的返回不一样,
    max_tokens：输出最大token 值，超出则不再输出。qwen新模型不支持这个字段，使用max_completion_tokens

    ```python
     from my_client import creat_client
     
     messages=[
        {'role':'system','content':'你是一位资深的市场专家，从专业的角度，分析下方市场问题'},# system
        {'role':'user','content':'我国2026年经济走向分析'},# user
     ]
     client = creat_client()
     completion = client.chat.completions.create(
        model="qwen3.8-flash", # 模型名称
        messages=messages,
        temperature=0.7,
        max_tokens=100
     )
     content = completion.choices[0].message.content
     messages.append( {'role':'assistant','content':content}) # assistant
     print(content)

    ```
    

## 两行自检
- ① 我说不出出处的知识点:无
- ② 学了但没落进任何行为的知识点:无
