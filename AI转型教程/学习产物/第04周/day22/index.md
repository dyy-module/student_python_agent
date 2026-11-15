# day22 学习笔记(学习者本人填写)

> 口径:标 `python` 的代码块须纯 Python 且可直接运行;终端命令(python -m venv / pip ...)用文本或 `bash` 块标注,不混进 python 块。末尾须写两行自检(见 00_验证规则与里程碑.md 日级第3、5条)。

## 今日主题
venv
pip
requirements.txt

## 建环境命令备忘
venv 是什么：
python 为了适应不同项目适用不同开发环境，推出的工具。venv创建独立环境，放入独立文件夹，防止污染环境

venv 如何用
1.创建环境： python -m venv {文件夹地址和文件名}

2.需要激活，cd 到创建的文件夹，然后不同系统对应激活
liniux/mac  执行 source bin/activate
windows 执行 Scripts\activate

3.撤销激活
deactivate

4.安装不同的包：
python -m pip install requests

5.导出配置文件
pip freeze | Out-File -Encoding utf-8  requirements.txt
不加 Out-File -Encoding utf-8 可能因为 window PowerShell 环境问题变成utf-16 格式的。
问题：！！！ 加了 如果环境是window powershell 5 的版本，会有BOM 问题，既会在文档前加入不可见字符，会导致读取时崩溃。
解决：
1. 升级powershell 到7 python -m pip freeze | Out-File -Encoding utf8NoBOM requirements.txt
$PSVersionTable.PSVersion
pip freeze > requirements.txt

2.python -m pip freeze | Out-File -Encoding ascii requirements.txt 使用ascll 编码

业界统一约定 utf-8/ASCLL 字符格式

6.如何根据requirements.txt安装依赖
python -m pip install -r requirements.txt
和 pip install -r requirements.txt 的区别，python -m 指定了当前版本

pip 是什么
python 官方提供的包管理工具

requirements.txt 是什么
约定的项目依赖清单

## JS→Python 对照
- JS `npm init` + 本地 node_modules → Python `python -m venv .venv`(需手动激活)
- JS `npm install axios` → Python `pip install requests`
- JS package.json 的 dependencies → Python requirements.txt(`包名==版本` 每行一条)
- JS `npm install`(按 package-lock 还原)→ Python `pip install -r requirements.txt`
- JS `npm ls` / `npm info x` → Python `pip list` / `pip show x`
- JS 自动解析 node_modules 无需激活 → Python 必须先 activate 才走 .ve

## 两行自检
- ①我说不出出处的知识点:无
- ②学了但没落进任何行为的知识点:无

## 卡点与解决(非必填)
<可留空>
