# day29 笔记(学习者本人填写)
## openai openai==3.51.0

## pathlib 
```python
from pathlib import Path

# 项目内资源、配置文件：用 __file__
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

# 用户家目录：存放用户配置文件、下载、桌面等
# Windows: C:\Users\用户名 | Linux: /home/用户名 | macOS: /Users/用户名
p_home = Path.home()
print(p_home)

# 交互式脚本 用户希望“在哪个目录运行，就操作哪个目录”
p_cwd = Path.cwd()
print(p_cwd)

p= Path('.') #环境目录 只是相对路径,尽量少用
print(p)

# 批量化文件查找与处理
large_files = sorted(
    (p for p in Path.cwd().rglob("*.py") if p.stat().st_size > 10_000),
    key=lambda p: p.stat().st_size,
    reverse=True
)
print(large_files)
```


- JS `npm install xxx` → Python venv 内 `pip install xxx`(并写入 requirements.txt)
- JS `path.join(__dirname,"output")` → Python `Path.cwd() / "output"`(今日首教)
- JS `fs.mkdirSync(dir,{recursive:true})` → Python `Path.mkdir(parents=True, exist_ok=True)`(今日首教)
- JS `fs.writeFileSync(f, s)` → Python `Path.write_text(s, encoding="utf-8")`(今日首教)
- JS `import pkg from 'xxx'` → Python `import xxx` / `from xxx import Yyy`
- JS 用对象数组做选型表 → Python 用 dict / list[dict] + for 遍历
- JS `try{ require('x') }catch(e){}` → Python `try: import x / except ImportError:`
- JS 环境变量 `process.env.KEY` → Python `os.environ["KEY"]`(明天正式教)

## 两行自检
- ① 我说不出出处的知识点:无
- ② 学了但没落进任何行为的知识点:Path.cwd()
