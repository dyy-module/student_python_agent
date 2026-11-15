在实际项目中，`pathlib` 的价值远不止于简化路径拼接。它通过将路径抽象为对象，在**项目结构管理、批量文件处理、数据管道、安全防护**等场景下，能显著提升代码的健壮性与可维护性。以下是它在真实项目中的典型使用场景与方式。

---

下面分别讲 `pathlib` 和 `os` 的主要内容、常用 API 和区别。

---

## 一、`pathlib`：面向对象的路径操作

`pathlib` 是 Python 3.4+ 引入的标准库，用“路径对象”表示文件/目录路径，代码更直观、跨平台。核心类：

- `PurePath`：纯路径计算，不访问文件系统
- `Path`：实际路径操作，会根据系统实例化为 `PosixPath` 或 `WindowsPath`

```python
from pathlib import Path

p = Path("data") / "a.txt"   # 路径拼接
print(p)                     # data/a.txt
```

### 1. 常用属性

```python
p = Path("/home/user/data/a.tar.gz")

p.parent        # /home/user/data
p.parents       # 所有父目录
p.name          # a.tar.gz
p.stem          # a.tar
p.suffix        # .gz
p.suffixes      # ['.tar', '.gz']
p.parts         # ('/', 'home', 'user', 'data', 'a.tar.gz')
p.anchor        # /
p.drive         # Windows 下如 C:
p.root          # /
```

### 2. 路径拼接与转换

```python
Path("a") / "b" / "c.txt"
Path("a").joinpath("b", "c.txt")

str(p)          # 转字符串
p.as_posix()    # 转 POSIX 风格字符串
p.absolute()    # 绝对路径，不一定解析符号链接
p.resolve()     # 解析为绝对路径，处理 .. 和符号链接
```

### 3. 判断与信息

```python
p.exists()
p.is_file()
p.is_dir()
p.is_symlink()
p.is_absolute()
p.stat()        # 类似 os.stat
p.samefile(other)
```

### 4. 读写文件

```python
p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")

p.read_bytes()
p.write_bytes(b"hello")

with p.open("r", encoding="utf-8") as f:
    ...
```

### 5. 目录遍历与匹配

```python
for child in Path("data").iterdir():
    print(child)

for py in Path(".").rglob("*.py"):
    print(py)

for txt in Path(".").glob("*.txt"):
    print(txt)

p.match("*.txt")
```

### 6. 创建、删除、重命名

```python
Path("out/sub").mkdir(parents=True, exist_ok=True)

p.unlink(missing_ok=True)   # 删除文件
Path("empty_dir").rmdir()   # 只能删空目录

p.rename("new.txt")
p.replace("new.txt")
p.touch()                   # 创建空文件或更新时间
```

注意：`pathlib` 没有递归删除目录的方法，递归删除用：

```python
import shutil
shutil.rmtree("dir")
```

### 7. 修改路径字符串

```python
p.with_name("b.txt")
p.with_suffix(".json")
p.with_stem("new")
```

### 8. 权限、链接等

```python
p.chmod(0o644)
p.symlink_to("target")
p.hardlink_to("target")
```

---

## 二、`os`：与操作系统交互的标准库

`os` 更底层、范围更广，包含路径操作、环境变量、进程、文件描述符、系统信息等。路径相关主要在 `os.path` 子模块中。

### 1. 当前目录与环境变量

```python
import os

os.getcwd()
os.chdir("data")

os.environ["MY_VAR"] = "1"
os.environ.get("HOME")
os.getenv("HOME")

os.name          # 'posix' / 'nt'
os.sep           # 路径分隔符
os.pathsep       # PATH 分隔符
os.linesep       # 换行符
```

### 2. 目录与文件操作

```python
os.listdir(".")
os.mkdir("dir")
os.makedirs("a/b/c", exist_ok=True)
os.rmdir("empty_dir")       # 只能删空目录
os.removedirs("a/b/c")      # 逐级删空目录
os.remove("a.txt")          # 删除文件
os.unlink("a.txt")
os.rename("a.txt", "b.txt")
os.replace("a.txt", "b.txt")
```

递归删除目录用：

```python
import shutil
shutil.rmtree("dir")
```

### 3. 遍历目录

```python
for name in os.listdir("."):
    print(name)

for entry in os.scandir("."):
    print(entry.name, entry.is_file(), entry.is_dir())

for root, dirs, files in os.walk("."):
    print(root, dirs, files)
```

`os.scandir()` 通常比 `os.listdir()` 更高效，因为 `DirEntry` 可缓存文件类型信息。

### 4. `os.path` 常用函数

```python
import os

os.path.join("data", "a.txt")
os.path.basename("/a/b/c.txt")   # c.txt
os.path.dirname("/a/b/c.txt")    # /a/b
os.path.splitext("a.tar.gz")     # ('a.tar', '.gz')

os.path.exists(p)
os.path.isfile(p)
os.path.isdir(p)
os.path.islink(p)

os.path.abspath("a.txt")
os.path.realpath("a.txt")
os.path.relpath("/a/b/c", "/a")
os.path.normpath("a/../b")
os.path.expanduser("~/a.txt")
os.path.expandvars("$HOME/a.txt")

os.path.getsize(p)
os.path.getmtime(p)
os.path.commonpath(["/a/b", "/a/c"])
```

### 5. 权限、链接、状态

```python
os.stat(p)
os.chmod(p, 0o644)
os.symlink("target", "link")
os.readlink("link")
os.link("a.txt", "hardlink.txt")
os.utime(p, None)
os.access(p, os.R_OK)
```

### 6. 进程与系统相关

`os` 还包含：

```python
os.getpid()
os.getppid()
os.cpu_count()
os.urandom(16)
os.system("ls")       # 简单执行命令，复杂场景用 subprocess
os.popen("ls")        # 旧式接口，推荐 subprocess
```

执行外部命令更推荐：

```python
import subprocess
subprocess.run(["ls", "-l"], check=True)
```

---

## 三、`pathlib` 与 `os` 怎么选

| 场景 | 推荐 |
|---|---|
| 路径拼接、判断、读写、遍历 | `pathlib.Path` |
| 老代码兼容、字符串路径函数 | `os.path` |
| 环境变量 | `os.environ` / `os.getenv` |
| 进程、PID、系统信息 | `os` |
| 复制、移动、递归删除 | `shutil` |
| 执行外部命令 | `subprocess` |

简单原则：

- **新代码做路径操作优先用 `pathlib`**
- **环境变量、进程、底层文件系统操作仍用 `os`**
- **复制/移动/递归删除用 `shutil`**
- **调用外部命令用 `subprocess`，不要优先用 `os.system`**

一个综合例子：

```python
from pathlib import Path
import os

base = Path(os.getenv("DATA_DIR", "."))
out = base / "output"
out.mkdir(parents=True, exist_ok=True)

for f in base.glob("*.txt"):
    text = f.read_text(encoding="utf-8")
    (out / f.name).write_text(text.upper(), encoding="utf-8")
```


### 场景一：构建清晰、可移植的项目结构

这是 `pathlib` 最基础也最广泛的应用。通过 `Path(__file__)` 可以动态定位项目根目录，避免依赖硬编码的绝对路径或容易出错的相对路径。

```python
from pathlib import Path

# 无论从哪个目录运行脚本，都能准确定位项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG_FILE = PROJECT_ROOT / "config" / "settings.toml"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"

# 一次性创建所需目录，无需担心中间层级不存在或已存在
LOG_DIR.mkdir(parents=True, exist_ok=True)
```

这种模式在需要读取配置、写入日志或定位静态资源的 Web 应用、CLI 工具中几乎是标准做法。

---

###  场景二：批量化文件查找与处理

在日志清理、数据导入、批量重命名等任务中，`glob()` 和 `rglob()` 返回的是 `Path` 对象列表，可以链式调用 `.stat()`、`.open()`、`.unlink()` 等方法，代码非常紧凑。

**示例：找出所有超过 10KB 的 Python 文件并按大小排序**
```python
from pathlib import Path

large_files = sorted(
    (p for p in Path(".").rglob("*.py") if p.stat().st_size > 10_000),
    key=lambda p: p.stat().st_size,
    reverse=True
)
```
对比 `os.walk()` 需要手动拼接路径和判断文件类型，`rglob` 一行就能完成递归遍历。

---

### 场景三：数据科学与实验工作流

数据科学项目通常涉及读取多个目录的数据集、创建输出文件夹、管理实验产物。`pathlib` 能让这些流程的路径管理变得清晰可靠。

```python
from pathlib import Path

EXPERIMENT_ROOT = Path("experiments") / "run_2026_11_15"
EXPERIMENT_ROOT.mkdir(parents=True, exist_ok=True)

# 为每个数据集创建独立的输出子目录
for dataset_path in Path("datasets").glob("*.csv"):
    output_dir = EXPERIMENT_ROOT / dataset_path.stem
    output_dir.mkdir(exist_ok=True)
    # ... 处理数据并写入 output_dir ...
```

在 Notebook 环境中，`Path.cwd()` 和 `Path.home()` 也能可靠地用于定位工作目录或用户主目录，避免因内核工作目录变化导致的路径失效。

---

###  场景四：安全写文件（原子替换）

直接覆盖写入的风险是，一旦程序在中途崩溃，原文件和新内容可能同时损坏。一个成熟的模式是**先写临时文件，再原子替换**。`pathlib` 的 `.with_suffix()` 可以方便地生成临时文件名。

```python
import os
from pathlib import Path

def atomic_write(target: Path, text: str) -> None:
    tmp_path = target.with_suffix(target.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, target)  # 同一文件系统内是原子操作
```

这个技巧在处理配置文件、数据库索引、日志快照等“要么完整，要么没有”的场景中非常重要。

---

###  场景五：路径安全校验与防穿越

在处理用户上传的文件名或拼接来自外部的路径片段时，路径穿越攻击是一个真实威胁。`resolve()` 可以解析 `..` 和符号链接，得到真实绝对路径，从而进行安全边界检查。

```python
from pathlib import Path

BASE_UPLOAD_DIR = Path("/var/www/uploads").resolve()

def safe_join(user_input: str) -> Path:
    target = (BASE_UPLOAD_DIR / user_input).resolve()
    if not str(target).startswith(str(BASE_UPLOAD_DIR)):
        raise ValueError("非法的路径访问")
    return target
```

这是 Web 后端、文件服务中处理用户提交路径时的必备防护措施。

---

### 场景六：与现有代码和第三方库无缝集成

`Path` 对象实现了 `__fspath__` 协议，可以直接传递给 `open()`、`os.stat()`、`shutil.copy()` 等接受路径字符串的标准库函数或第三方库，无需手动 `str()` 转换。

```python
import shutil
from pathlib import Path

src = Path("data") / "raw.csv"
dst = Path("backup") / "raw.csv.bak"

shutil.copy(src, dst)        # 直接接受 Path 对象
with src.open("rb") as f:    # open 也接受 Path 对象
    ...
```

这意味着你可以逐步将项目中的路径处理迁移到 `pathlib`，而不需要一次性重写所有涉及文件操作的代码。

---

###  实践中的注意事项

在实际项目中使用 `pathlib` 时，有几个细节值得留意：

- **递归删除目录**：`Path.rmdir()` 只能删除**空目录**。删除非空目录需要 `shutil.rmtree(path)`，不要尝试用 `pathlib` 手动实现递归删除。
- **`resolve()` 的严格性**：在 Python 3.6+ 中，`resolve()` 默认 `strict=False`，不会因为路径不存在而报错；但在某些旧版本或特定场景下，它的行为可能需要留意。
- **性能敏感场景**：对于极大量路径的频繁遍历，`os.scandir()` 可能比 `Path.iterdir()` 稍快，因为 `DirEntry` 会缓存文件类型信息。但在绝大多数项目中，`pathlib` 的可读性收益远大于这点性能差异。
- **与 `os.path` 混用**：在维护老代码时，不必强行将所有 `os.path` 调用一次性替换。新代码用 `pathlib`，老代码逐步迁移，两者通过 `str(path)` 或 `Path(str_path)` 可以顺畅互转。

---

总的来说，在真实项目中，`pathlib` 的最佳用法是**把它当作路径的“一等公民”来对待**：路径从产生、传递到使用，全程保持为 `Path` 对象，而不是在字符串和函数调用之间来回转换。这样代码会更短、更安全，也更易于理解和维护。

## 选型结论与 SDK 记录(当日产出硬项,2026-11-15 助教按产物实测代补,结论摘自你本人产物 reason 字段)
- 四家对比结论(详见 output/model_compare.txt):DeepSeek 3星(便宜、足够用)、通义千问 3星(lite 便宜、足够用)、智谱GLM 1星(套餐偏贵但量大)、Kimi 不推荐(太贵)
- 学习期主力端点:DeepSeek 与通义千问二选一(均 3 星;Day30 建客户端时 base_url 定哪家,在此补一行最终决定)
- SDK 状态:openai 3.51.0 已在 venv 内安装(2026-11-15 第三轮实测,自检走"打印版本"分支);requirements.txt 尚未建,freeze 后在此补记