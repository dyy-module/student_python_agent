# 第14周 · 云端部署:云服务器 + 域名 + HTTPS + 备案(阶段5闸门)

> 与主计划的差异说明:本周严格对应修订版路线图「阶段5后段」(17周映射第14周),**day98 为阶段5闸门**(验证规则:作品公网可点开,前端→FastAPI→LLM/RAG 全链路在线可用,含 HTTPS)。主题为云服务器(ECS/轻量应用服务器)、域名与 DNS 解析、HTTPS(TLS 证书/Let's Encrypt)、ICP 备案、Nginx 反向代理与进程守护、上线部署。本周把第13周你在本地容器化跑通的 AI 后端**真正部署到公网、可被面试官点开**,直接支撑主计划作品集**项目1「商品知识库导购问答」上线**与简历"在线可访问 URL"这一硬证据。云端部署/域名/HTTPS/备案/Nginx/进程守护均在本周首教,与 reference 日程表第14周完全一致,不增删。备案据主计划已于第7周提交(周期2-4周),本周应已下发;如未下发按 day98 补救方案用 IP+端口临时演示并标注。
> 变更记录:首版(基于2026市场修订版生成)。
> 本周产物约定:固定产物置于 学习产物/第14周/dayN/,含部署脚本(.sh)/配置(.conf/.yml)/生产 compose/上线记录(.md);跟练统一命名 extra_* 放入 学习产物/第14周/dayN/extra/ 子目录,严禁混放;每日笔记为同目录 index.md。**服务器上的大模型 key 一律用环境变量/secrets 注入、零硬编码、不写进代码/镜像/仓库**(.env 不入库、被 .dockerignore 排除,compose 用 env_file 注入);证书私钥同样不入库;安全组最小开放(仅 22/80/443)。

## 本周概览

- 主题:把第13周容器化的 AI 后端真正搬上公网——买云服务器、配域名解析、上 HTTPS 证书、走备案、Nginx 反向代理 + 进程守护,最终交付一个"公网 HTTPS 可点开"的完整 AI 应用。
- 为什么对拿offer有用:能独立上线一个 HTTPS 可访问的 AI 应用,是"能交付"最硬的证据——它让项目1的 README 能放上**在线 URL + 架构图 + 成本数据**(主计划/验证规则的作品集验收清单项),面试官点开即用,远胜"本地能跑"。招聘 JD 高频要求"Linux + Git + Docker + 部署运维",本周正是补齐"部署上线"这最后一环。面试时你能完整讲:"我用 docker compose 把 FastAPI+RAG 部署到云服务器,配了域名 DNS、Let's Encrypt HTTPS、Nginx 反代和进程守护,7×24 稳定在线,月成本约 XX 元"——这是从"会写"到"会上线"的关键跃迁,也是六阶段技术栈闭环的收官。
- 教材使用策略:本周无可信中文视频直出,以**云厂商官方文档(阿里云帮助中心)+ Nginx/Let's Encrypt 官方 + 中文搜索词**为主(约70%),尚硅谷 Docker(A级视频)复用其"购买云服务器/安装/部署"章节(约20%),菜鸟/廖雪峰做 Linux/Python 语法速查(约10%)。运维操作优先照官方文档分步执行,重点理解概念(域名解析/TLS 握手/反向代理/进程守护),而非死记命令;腾讯云文档本环境不可直出,一律用中文搜索词定位。
- 本周结束时应能做到:
  1. 选购并初始化一台云服务器:SSH 密钥免密登录、安全组最小开放(22/80/443)、装好 Docker 与 compose 环境。
  2. 买域名并配 DNS A 记录解析到服务器 IP,用 Let's Encrypt(或云免费证书)给站点上 HTTPS,并确认证书自动续期。
  3. 把第13周的 FastAPI+RAG 容器化服务用生产 docker compose 部署上云,配 Nginx 反向代理 + 进程守护,通过 (https://域名) 稳定访问全链路。
  4. day98 阶段5闸门:限时独立产出"公网 HTTPS 可访问的 AI 应用 demo(前端→FastAPI→LLM/RAG 全链路在线)+ 可复现部署步骤记录 + 月度成本",并确认备案已下发。

## 前置知识点闭包(截至第13周已学)

Python 全栈基础:基础类型/print-input/f-string/控制流/for-while-range-enumerate/字符串切片与方法/list-tuple-dict-set/推导式/生成器表达式/random-datetime、def-docstring/参数全体系/lambda/map-filter/模块与包/import/闭包/nonlocal/装饰器、OOP(class/继承/多态/魔术方法/isinstance-type)/文件读写(open-with)/异常全体系(try-except-else-finally/raise/自定义异常)、venv-pip/requirements.txt/requests/正则 re/类型提示 typing/asyncio。
AI 应用线:大模型 API 调用/**环境变量读 key(零硬编码)**/Prompt 工程/JSON Mode、流式 Streaming/Function Calling、LangChain/LCEL/RAG 全链路/向量库(Chroma/Milvus/Faiss)/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP(认知)。
前端线(TS):TS SSE/流式渲染/打字机、Vercel AI SDK(useChat)/LangChain.js/工具调用可视化、Agent 交互模式/React 流式对话组件。
后端工程线(第13周):FastAPI 路由/依赖注入 Depends/Pydantic/SSE 流式接口(StreamingResponse+异步生成器)、Docker 镜像/容器/Dockerfile/.dockerignore、docker-compose 多服务编排/env_file 注入/depends_on、后端项目分层拆分。

本周新增(首教):云服务器(ECS/轻量应用服务器选型)、Linux 基础命令与 SSH 密钥登录、安全组最小开放、域名与 DNS 解析(A 记录/CNAME)、HTTPS(TLS 证书原理/Let's Encrypt/Certbot 申请与自动续期/HTTP→HTTPS 跳转)、ICP 备案流程、反向代理(Nginx proxy_pass,认知+最小配置)、上线部署(代码/镜像上云、生产 docker-compose)、进程守护(systemd / docker compose restart、开机自启、崩溃重启)、部署成本核算。
【超前】预警:Kubernetes(K8s)编排、CI/CD 自动部署流水线(GitHub Actions 部署)、负载均衡(多实例/Nginx upstream 集群)、监控告警(Prometheus/Grafana)、日志聚合(ELK)、CDN 加速、WAF/DDoS 高防、数据库主从与备份策略、蓝绿/金丝雀发布、IaC(Terraform/Ansible)——本周均不作正式教学,若产物需要仅以【超前】最小片段出现并标注。

---

## Day92(周一,7h)· 云服务器选购与初始化(SSH 密钥 / 安全组 / Docker 环境)

今天迈出上线第一步——拥有一台属于你自己的云服务器。你部署过前端到 Vercel/Netlify(点几下就上线),但 AI 后端是**有状态的常驻服务**(要 7×24 跑 FastAPI + 向量库),需要一台一直在线的 Linux 机器。这台机器就是你的"云端电脑",你通过 SSH 远程登录、在上面装 Docker、跑容器。产出:一台初始化好、能 SSH 免密登录、装好 Docker 环境的云服务器 + 初始化记录与脚本。

💡 JS开发者速读:云服务器 ≈ 一台你 SSH 上去的 Linux 电脑(比你用过的 CI runner 更持久、可长期驻留);SSH 密钥登录 ≈ 你 git 用 SSH key 免密 push 的**同一套公钥/私钥心智**(私钥留本地、公钥放服务器);安全组 ≈ 云上的防火墙/端口白名单(只开 22 SSH、80 HTTP、443 HTTPS,其余端口外网进不来,比你本地防火墙更严格、更要最小开放);"轻量应用服务器"≈ 打包好镜像、简化计费的 ECS(个人项目更便宜够用);装 Docker ≈ 把第13周你本地的 Docker 环境搬到服务器。

### 学习内容

- 云服务器选型:ECS(弹性、可自定义)vs 轻量应用服务器(打包镜像、简化),按主计划成本核算选轻量约 50-100 元/月(JS对应 选托管平台套餐)
- Linux 基础命令:cd/ls/cat/vim/mkdir/ps/top/systemctl/journalctl(够部署运维用即可,JS对应 你偶尔用的终端命令)
- SSH 密钥登录:本地生成密钥对、上传公钥到服务器、禁用密码登录(JS对应 git SSH key 免密)
- 安全组配置:入站最小开放 22/80/443,关闭其余端口(JS对应 严格的端口白名单)
- 安装 Docker 与 docker compose 环境并验证(复用第13周能力,JS对应 在服务器装运行时)

### 讲解

结论先行:云服务器初始化的标准动线是"SSH 登录 → 更新系统 → 装 Docker → 设开机自启 → 验证",而**安全组必须在控制台先收敛到只开 22/80/443**(暴露过多端口是被扫描攻击的头号原因)。下面是一段初始化命令序列(教学演示,**不是**产物答案;完整可复现脚本与选购决策由你在产物中整理)。

```bash
# 教学演示:云服务器初始化命令序列(非产物答案,完整脚本由你整理进产物)
ssh root@                  # SSH 密钥登录(配好公钥后免密)
apt update && apt upgrade -y            # 更新系统包(Debian/Ubuntu 系)
curl -fsSL (https://get.docker.com) | sh  # Docker 官方一键安装脚本
systemctl enable --now docker           # 启动 Docker 并设为开机自启
docker --version && docker compose version   # 验证 Docker 与 compose
# 控制台安全组:入站仅开放 22(SSH)/80(HTTP)/443(HTTPS),其余全部关闭
```

### 教材与章节

- 云厂商官方文档:阿里云帮助中心 (https://help.aliyun.com/) (轻量应用服务器/ECS 快速入门,具体产品用站内搜索)
- 视频(A级,已核验):尚硅谷 3 小时速通 Docker (https://www.atguigu.com/video/307) (含"购买云服务器/安装 Docker"章节)
- 中文搜索词:「轻量应用服务器 购买 初始化 教程」「云服务器 SSH 密钥登录 免密 配置」「安全组 最小开放 22 80 443」「Linux 常用命令 部署 运维」;腾讯云文档用搜索词「腾讯云 轻量应用服务器 初始化」定位(本环境不杜撰具体链接)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 云服务器选型、Linux 基础命令、SSH 密钥登录、安全组最小开放、装 Docker 精读+实操 |
| 技术练习 | 2h | 完成服务器初始化、整理 setup 脚本与记录、extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Docker/云厂商英文文档片段 |
| 输出 | 1h | GitHub commit(脚本/记录,确认无敏感信息);整理选购决策为博客素材 |
| 复盘 | 0.5h | 补 index.md,写前端部署→云服务器迁移对照,自检安全组最小开放 |

### 当日产出

- [ ] 完成 学习产物/第14周/day92/server_init.md:云服务器选购与初始化记录
  - 记录选型决策(轻量 vs ECS、地域、规格、月度费用估算,对齐主计划成本核算 50-100 元/月)
  - 记录初始化步骤要点:系统版本、创建/绑定 SSH 密钥、禁用密码登录、安全组入站规则(仅 22/80/443)、安装 Docker 与 compose 的验证结果
  - 验收点:本地能 `ssh` 免密登录服务器;`docker --version`/`docker compose version` 有正常输出;安全组截图或规则清单入档
  - 所用知识点清单:云服务器选型、SSH 密钥登录、安全组最小开放、Linux 基础命令、Docker 环境安装(第13周)、systemctl 开机自启
- [ ] 完成 学习产物/第14周/day92/setup_server.sh:服务器初始化脚本(简洁可用为准,把上述命令整理成可复现脚本;不含任何密钥/密码明文)
- [ ] 补记 学习产物/第14周/day92/index.md:覆盖全部学习内容(命令用文本标注,不混入敏感信息)

### JS→Python对照笔记

- JS 部署到 Vercel/Netlify(平台托管)→ 云服务器自己 SSH 上去装环境、跑容器(自管)
- JS git 用 SSH key 免密 push → 服务器 SSH 密钥登录(同一套公钥/私钥)
- JS 本地 devServer 端口随意 → 服务器安全组严格白名单(仅 22/80/443)
- JS `npm i -g pm2` 装全局工具 → 服务器 `curl get.docker.com | sh` 装 Docker
- JS CI runner 临时环境 → 云服务器长期驻留(7×24)

### 跟练清单(放extra/)

- extra_firewall.md:整理一份"安全组/防火墙最小开放清单"——逐条列出应开放(22/80/443)与应关闭的端口及理由,并记录一次"从外网访问未开放端口应被拒绝"的验证结果,强化最小权限意识。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 云服务器选型/SSH 密钥/安全组/Linux 命令/装 Docker | 阿里云帮助中心;尚硅谷Docker;搜索词 | server_init.md + setup_server.sh | 云服务器选型、SSH 密钥登录、安全组最小开放、Linux 命令、Docker 安装、systemctl |

【超前】标注集中区:CI/CD 自动部署、IaC(Terraform/Ansible)批量初始化、K8s 集群属【超前】,本日仅手动初始化单机,不深入。
硬约束复查:仅用 day92 闭包知识点 ✓ key 零硬编码/不入库(脚本不含密钥明文)✓ 配置安全(安全组仅开 22/80/443)✓ 交付物达成 ✓ extra/命名正确 ✓

---

## Day93(周二,7h)· 域名购买与 DNS 解析(A 记录指向服务器)

今天给你的服务一个"人话地址"。IP(如 47.x.x.x)没人记得住,也不能体面地写进简历;域名(如 yourname.com)才是能发给面试官、印在 README 上的入口。买域名 + 配 DNS 解析(A 记录把域名指向服务器公网 IP),让浏览器输入域名就能找到你的机器。同时确认国内特有的前置——ICP 备案状态。产出:一个已解析到服务器、可访问的域名 + DNS 配置与备案状态记录。

💡 JS开发者速读:域名解析 ≈ 你在 Vercel/Netlify 给自定义域名配 CNAME/A 记录的那套(只是这次你自己在 DNS 控制台管);A 记录 ≈ 把域名( apex 根域)直接指向一个 IP,CNAME ≈ 指向另一个域名(如 www 指向 apex);DNS 生效有 TTL 延迟 ≈ 你改 CDN/缓存要等刷新,不是瞬时;`nslookup`/`dig` ≈ 你查 DNS 的 devtools;**备案是国内特有环节**——域名指向境内服务器必须完成 ICP 备案,否则会被拦截,这是海外部署平台(Vercel)完全没有的一步。

### 学习内容

- 域名购买与实名:选后缀、在云厂商注册、完成实名(JS对应 买自定义域名)
- DNS 解析原理:A 记录(域名→IP)、CNAME(域名→域名)、TTL 生效延迟(JS对应 你配过的 DNS 记录)
- 把根域/apex 与 www 用 A 记录指向服务器公网 IP(JS对应 自定义域名绑定)
- 解析生效验证:nslookup/dig/ping(JS对应 DNS 排查工具)
- ICP 备案:域名指向境内服务器的前置义务、备案状态确认(主计划第7周已提交、周期2-4周,本周应已下发)

### 讲解

结论先行:上线的域名链路是"买域名 → 加 A 记录指向服务器公网 IP → 等 TTL 生效 → 用 dig/nslookup 验证解析到正确 IP";国内还须确认 ICP 备案已下发(否则境内访问被拦)。下面是解析验证的命令演示(教学演示,**不是**产物答案;完整 DNS 配置与备案状态由你在产物中记录)。

```bash
# 教学演示:验证域名 A 记录是否解析到服务器(非产物答案)
# 前提:已在域名 DNS 控制台添加 A 记录  yourname.com -> 服务器公网IP
dig yourname.com +short          # 只看解析结果 IP(应等于服务器公网 IP)
nslookup yourname.com            # 查询域名解析到的 IP
ping -c 4 yourname.com           # 验证连通(Linux 用 -c 限定次数)
# 解析未生效?多为 TTL 缓存延迟,等待或降低 TTL 后重试
# 备案:域名指向境内服务器须完成 ICP 备案,否则 80/443 访问会被拦截
```

### 教材与章节

- 云厂商官方文档:阿里云帮助中心 (https://help.aliyun.com/) (域名注册/云解析 DNS/ICP 备案,具体产品用站内搜索)
- 中文搜索词:「域名 购买 实名 流程」「DNS A记录 CNAME 解析 配置」「域名 解析 服务器 IP 生效」「ICP 备案 流程 周期 查询」;腾讯云用搜索词「腾讯云 域名 DNSPod 解析 备案」定位(不杜撰链接)
- 语法速查:菜鸟教程 Python3 (https://www.runoob.com/python3/) (如需写解析检查小脚本)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 域名购买实名、DNS 解析原理(A/CNAME/TTL)、A 记录配置、解析验证、备案确认 精读+实操 |
| 技术练习 | 2h | 完成域名购买与 A 记录解析、验证生效、整理记录、extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 DNS/云厂商英文文档片段 |
| 输出 | 1h | GitHub commit(DNS/备案记录,无敏感信息);整理"备案踩坑"为博客素材 |
| 复盘 | 0.5h | 补 index.md,写前端自定义域名→自管 DNS 迁移对照,自检备案状态 |

### 当日产出

- [ ] 完成 学习产物/第14周/day93/dns_setup.md:域名购买与 DNS 解析记录
  - 记录:域名选择与实名、在 DNS 控制台添加的 A 记录(根域与 www → 服务器公网 IP)、TTL 设置
  - 记录解析生效验证结果(dig/nslookup 输出摘要,证明已解析到正确 IP)
  - 记录 ICP 备案状态(备案号/是否已下发;若未下发,标注"进行中"并说明 day98 补救走 IP 临时演示)
  - 验收点:浏览器输入 (http://域名(或) (http://服务器IP))能命中服务器上的服务(本日先不要求 HTTPS,day94 补)
  - 所用知识点清单:域名购买实名、DNS A 记录/CNAME、TTL 生效、dig/nslookup/ping 验证、ICP 备案流程
- [ ] 补记 学习产物/第14周/day93/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS Vercel 配自定义域名(平台代管 DNS)→ 自己在云 DNS 控制台加 A 记录(自管)
- JS `CNAME www → apex` → DNS A 记录(根域→IP)/CNAME(www→根域)
- JS 改 CDN 等缓存刷新 → DNS TTL 生效延迟(非瞬时)
- JS 无备案概念(海外平台)→ 境内服务器必须 ICP 备案
- JS 前端 `window.location` 域名 → 后端服务绑定域名入口(简历可放 URL)

### 跟练清单(放extra/)

- extra_subdomain.md:为后端 API 单独规划并解析一个子域名(如 api.yourname.com 用 A 记录指向同一服务器),记录配置与验证结果,体会"前端主域 + API 子域"的常见线上架构(为 day96 Nginx 按域名/路径分流做铺垫)。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 域名购买/DNS A 记录解析/生效验证/ICP 备案 | 阿里云帮助中心;搜索词 | dns_setup.md | 域名实名、A 记录/CNAME、TTL、dig/nslookup/ping、ICP 备案状态 |

【超前】标注集中区:DNSPod 智能解析/多线路、CDN 接入、域名 DNSSEC 属【超前】,本日仅配基础 A 记录,不深入。
硬约束复查:仅用 day93 闭包知识点 ✓ key 零硬编码/不入库(记录不含敏感凭据)✓ 配置安全(备案状态如实标注)✓ 交付物达成 ✓ extra/命名正确 ✓

---

## Day94(周三,7h)· HTTPS 证书(Let's Encrypt / 云免费证书,配置 TLS)

今天给你的站点加上那把"安全锁"。HTTP 明文传输会被浏览器标"不安全",也不满足 day98 闸门"含 HTTPS"的硬要求;HTTPS 用 TLS 证书加密传输。你在 Vercel 部署时 HTTPS 是全自动的,这次你要**自己申请证书并配置**——用 Let's Encrypt(免费、自动化)或云厂商免费 SSL 证书。产出:一个能通过 https:// 访问(浏览器显示锁)的站点 + 证书申请与配置记录。

💡 JS开发者速读:HTTPS ≈ 你配过的前端部署平台自动 HTTPS(只是这次手动走一遍);Let's Encrypt ≈ 免费 CA(证书颁发机构),Certbot ≈ 自动申请+续期证书的 CLI(≈ npm 装个工具跑一条命令);TLS 证书 ≈ 一对公钥/私钥(和你 SSH key、git 提交签名同源心智),私钥**绝不能泄露/入库**;证书 90 天到期须自动续期 ≈ 你续过的域名/SSL;浏览器地址栏的锁 ≈ TLS 握手成功;HTTP→HTTPS 301 跳转 ≈ 你配过的强制 HTTPS 重定向。

### 学习内容

- HTTPS/TLS 原理认知:对称/非对称加密、证书链、握手过程(认知级,不深挖密码学)
- Let's Encrypt 免费证书 + Certbot:申请、验证域名所有权、自动写入配置(JS对应 自动化证书工具)
- 证书自动续期:90 天到期,certbot renew + 定时任务(JS对应 证书续期)
- 云厂商免费 SSL 证书作为备选(申请后手动配到 Nginx)
- HTTP→HTTPS 301 跳转与 HSTS 认知(JS对应 强制 HTTPS)

### 讲解

结论先行:最省心的路径是用 Certbot 的 Nginx 插件——它会自动向 Let's Encrypt 证明你对域名的控制权、签发证书、并把 HTTPS 配置写进 Nginx,还顺带装好自动续期。关键是**证书私钥必须留在服务器、绝不入库/进镜像**。下面是 Certbot 申请流程演示(教学演示,**不是**产物答案;完整配置与续期验证由你在产物中记录)。

```bash
# 教学演示:用 Certbot 申请 Let's Encrypt 免费证书(非产物答案)
# 前提:域名已解析到本机(day93)、80 端口可访问、已装 Nginx(day96 详解)
apt install -y certbot python3-certbot-nginx   # 装 Certbot 及 Nginx 插件
certbot --nginx -d yourname.com -d www.yourname.com   # 申请并自动配置 HTTPS
certbot renew --dry-run                        # 演练自动续期(不真签发)
# 完成后 (https://yourname.com) 浏览器显示锁标志;私钥在 /etc/letsencrypt,不入库
```

### 教材与章节

- Let's Encrypt 官方中文(已核验):(https://letsencrypt.org/zh-cn/) (入门 /getting-started、文档 /docs、ACME 客户端 /docs/client-options)
- Nginx 官方文档(已核验):(https://nginx.org/en/docs/) (Configuring HTTPS servers、ngx_http_ssl_module)
- 中文搜索词:「Let's Encrypt Certbot 免费 HTTPS 证书 nginx」「certbot 自动续期 定时任务」「云 免费 SSL 证书 申请 配置」;阿里云 SSL 证书文档在 (https://help.aliyun.com/) 站内搜索

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | HTTPS/TLS 原理、Let's Encrypt/Certbot、证书续期、云免费证书、HTTP→HTTPS 跳转 精读+实操 |
| 技术练习 | 2h | 申请证书并配置 HTTPS、验证锁标志与续期、整理记录、extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Let's Encrypt/Nginx 英文文档片段 |
| 输出 | 1h | GitHub commit(记录/配置,确认无私钥);整理"免费 HTTPS 上手"为博客素材 |
| 复盘 | 0.5h | 补 index.md,写平台自动 HTTPS→手动证书迁移对照,自检私钥未入库 |

### 当日产出

- [ ] 完成 学习产物/第14周/day94/https_setup.md:HTTPS 证书申请与 TLS 配置记录
  - 记录:证书来源(Let's Encrypt/Certbot 或云免费证书)、申请命令要点、域名所有权验证方式、证书与私钥在服务器的存放路径
  - 记录 Nginx 启用 HTTPS 的配置要点(listen 443 ssl、证书路径、HTTP→HTTPS 跳转),配置片段给要点即可,不要求贴完整答案
  - 验收点:浏览器访问 (https://域名) 显示锁标志、无"不安全"警告;http:// 自动 301 跳到 https://
  - 所用知识点清单:HTTPS/TLS 原理、Let's Encrypt、Certbot 申请与验证、证书/私钥路径、Nginx SSL 配置、HTTP→HTTPS 跳转
  - 安全要求:证书私钥留服务器、**不写入仓库/镜像**;记录中不粘贴私钥内容
- [ ] 补记 学习产物/第14周/day94/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS Vercel 自动 HTTPS(平台代签)→ 自己用 Certbot 向 Let's Encrypt 申请(自管)
- JS npm 装工具跑命令 → `apt install certbot` + `certbot --nginx`
- JS 强制 HTTPS 重定向配置 → Nginx 80→443 301 跳转
- JS 私钥/secret 放平台环境变量 → 证书私钥留服务器文件系统,不入库
- JS 证书到期平台自动续 → Certbot renew + 定时任务自动续期

### 跟练清单(放extra/)

- extra_cert_renew.md:配置并记录证书自动续期方案(certbot renew 的定时任务/systemd timer),用 `--dry-run` 演练一次并记录结果,说明"为什么 90 天证书必须自动化续期",避免线上证书过期导致 HTTPS 失效。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| HTTPS/TLS/Let's Encrypt/Certbot/证书续期/跳转 | Let's Encrypt官方;Nginx官方;搜索词 | https_setup.md | TLS 原理、Let's Encrypt、Certbot 申请、Nginx SSL 配置、HTTP→HTTPS 跳转、自动续期 |

【超前】标注集中区:通配符证书、OCSP Stapling、HSTS 预加载、TLS 版本/加密套件深度调优属【超前】,本日仅申请单域证书并启用 HTTPS,不深入。
硬约束复查:仅用 day94 闭包知识点 ✓ key 零硬编码/不入库(证书私钥不入库、大模型 key 仍走 env)✓ 配置安全(仅开 80/443)✓ 交付物达成 ✓ extra/命名正确 ✓

---

## Day95(周四,7h)· 把第13周容器化服务部署上云(docker compose 生产起服务)

今天把上周的成果真正搬上云。第13周你在本地用 docker compose 起了 FastAPI + 向量库;今天把这套代码/镜像部署到云服务器,用**生产模式**的 compose 在服务器上后台跑起来,通过服务器 IP:端口能访问到接口。Docker 的镜像可移植性在这里发挥价值——"本地能跑"= "服务器也能跑"。产出:云服务器上运行的容器化 AI 后端(可访问 /docs)+ 生产部署记录。

💡 JS开发者速读:部署上云 ≈ 你把本地 docker-compose 搬到服务器再 `up` 一次(镜像可移植正是 Docker 的核心价值);生产 compose ≈ 你区分过的 dev/prod 配置(生产**关掉 `--reload`**、加 `restart: always`、key 走 `env_file`);把代码弄上服务器 ≈ `git clone` 后在服务器 build,或推镜像到 registry 再拉(≈ 你推 npm 包/docker image);`env_file` 注入 key ≈ 你在服务器配环境变量,代码零硬编码(与第13周完全一致);`up -d` 后台运行 ≈ 你 `pm2 start` 后台起服务。

### 学习内容

- 代码/镜像上服务器两种方式:`git clone` 后在服务器 build vs 推镜像到 registry 再拉(JS对应 源码部署 vs 制品部署)
- 生产 docker-compose.yml:`restart: always`、无 `--reload`、`env_file` 注入 key、端口映射(JS对应 prod 配置)
- 服务器上的 `.env`/环境变量管理:手动创建、**不入库**、被 .dockerignore 排除(承接第13周)
- `docker compose up -d` 后台起服务、`docker compose ps/logs` 查看状态(JS对应 pm2 后台/日志)
- 通过服务器本机 `curl` 与外网 IP:端口验证访问

### 讲解

结论先行:上云部署的标准动线是"拉代码 → 在服务器创建 .env 注入 key(不入库)→ 用生产 compose build → up -d 后台起 → 验证";生产 compose 与本地的关键差异是**去掉热重载、加 restart 策略、key 走 env_file**。下面是部署命令序列演示(教学演示,**不是**产物答案;生产 compose 与部署记录由你完成)。

```bash
# 教学演示:把第13周容器化服务部署上云(非产物答案)
ssh root@
git clone  app && cd app        # 拉代码(仓库内无 .env)
# 在服务器上手动创建 .env 注入 key(零硬编码、不入库、不进镜像)
printf 'LLM_API_KEY=%s\n' '' > .env
docker compose -f docker-compose.prod.yml build    # 构建生产镜像
docker compose -f docker-compose.prod.yml up -d    # 后台起服务
docker compose ps && curl (http://localhost:8000/docs)   # 确认运行并本机验证
```

### 教材与章节

- 视频(A级,已核验):尚硅谷 3 小时速通 Docker (https://www.atguigu.com/video/307) (部署/compose 章节)
- FastAPI 官方中文(已核验):(https://fastapi.tiangolo.com/zh/) (部署 Deployment 章节)
- 中文搜索词:「docker compose 生产部署 服务器 restart env_file」「git clone 服务器 docker build 上线」「docker compose up -d 后台 日志」;阿里云部署实践在 (https://help.aliyun.com/) 站内搜索

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | 代码/镜像上云方式、生产 compose(restart/env_file/无 reload)、服务器 .env 管理、up -d/ps/logs 精读+实操 |
| 技术练习 | 2h | 把第13周服务部署上云、生产 compose 起服务、验证访问、整理记录、extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Docker/FastAPI 部署英文文档片段 |
| 输出 | 1h | GitHub commit(生产 compose + .env.example,确认 .env 未上传);整理部署流程为项目1 README 素材 |
| 复盘 | 0.5h | 补 index.md,写本地→生产部署迁移对照,自检 key 走 env_file 零硬编码 |

### 当日产出

- [ ] 完成 学习产物/第14周/day95/docker-compose.prod.yml:生产多服务编排(简洁可用为准)
  - 基于第13周 compose 改造为生产版:api 服务去掉 `--reload`、加 `restart: always`、通过 `env_file: .env` 注入大模型 key 与向量库连接配置;向量库服务用生产卷持久化数据
  - compose 文件中**不出现任何明文 key**;真实 .env 只在服务器手动创建、不入库,仓库仅提交 .env.example
  - 验收点:`docker compose -f docker-compose.prod.yml up -d` 后 `docker compose ps` 显示服务健康;服务器本机 `curl (http://localhost:8000/docs`) 正常;外网 `(http://服务器IP:端口`) 可访问(HTTPS/域名 day94/day96 打通)
  - 所用知识点清单:docker compose 生产配置、restart 策略、env_file 注入、depends_on、卷持久化、代码上云(git clone/build)、up -d/ps/logs(均承接第13周)
- [ ] 完成 学习产物/第14周/day95/deploy.md:部署步骤记录(从拉代码到 up -d 到验证的可复现步骤;命令用文本标注,不含真实 key)
- [ ] 补记 学习产物/第14周/day95/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS 本地 docker-compose dev → 服务器 docker-compose.prod(去 reload、加 restart)
- JS `git push` + CI 部署 → `git clone` 上服务器手动 build/up(本周手动,CI/CD 属【超前】)
- JS 平台环境变量注入 secret → 服务器 `.env` + compose `env_file`(不入库)
- JS `pm2 start` 后台常驻 → `docker compose up -d` 后台运行
- JS `pm2 logs` → `docker compose logs -f`

### 跟练清单(放extra/)

- extra_env_prod.md:整理一份"生产环境变量注入清单"——列出服务所需的全部环境变量名(大模型 key、向量库地址、端口等)与其来源(服务器 .env / secrets),逐项标注"是否敏感、是否入库",并说明为什么敏感项只能通过 env_file/secrets 注入而不能写进 compose 明文或镜像。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 代码上云/生产 compose/env_file/up -d 部署验证 | 尚硅谷Docker;FastAPI官方中文;搜索词 | docker-compose.prod.yml + deploy.md | 生产 compose、restart、env_file 注入、卷持久化、git clone/build、up -d/ps/logs |

【超前】标注集中区:CI/CD 自动部署(GitHub Actions)、镜像 registry 私有仓库、多阶段构建瘦身、蓝绿发布属【超前】,本日手动 git clone + build 部署,不深入。
硬约束复查:仅用 day95 闭包知识点 ✓ **key 零硬编码/不入库(env_file 注入,.env 不入库/不进镜像,compose 无明文)** ✓ 配置安全(生产端口按需映射)✓ 交付物达成 ✓ extra/命名正确 ✓

---

## Day96(周五,7h)· 反向代理 Nginx + 进程守护(systemd / compose restart)

今天让服务"体面又抗造"。目前服务跑在 IP:8000,端口暴露、不美观也没上 HTTPS 入口。用 Nginx 做**反向代理**:用户访问标准的 80/443,Nginx 把请求转发给后端容器(≈ 你前端 devServer 里 proxy 的生产版),并在这一层整合昨天的 HTTPS 证书;再配**进程守护**,让服务崩溃自动重启、开机自启,做到 7×24 稳定。产出:Nginx 反向代理 + HTTPS 配置 + 进程守护方案,服务通过 (https://域名) 稳定访问(不再暴露 IP:端口)。

💡 JS开发者速读:Nginx 反向代理 ≈ 你 webpack/vite `devServer.proxy` 把 `/api` 转发到后端的**生产版**;`proxy_pass` ≈ 你 proxy 的 `target`;80/443 标准端口 ≈ 浏览器默认端口(用户不用写 `:8000`);进程守护 ≈ 你用过的 pm2(崩溃重启/开机自启),Docker 里用 `restart: always` 或 systemd service 实现;Nginx 还能同时托管前端静态 dist、终结 HTTPS(昨天证书)、对 SSE 关闭 `proxy_buffering`(否则流式被缓冲、打字机失效——这点你第13周踩过)。

### 学习内容

- Nginx 反向代理:`server`/`location`/`proxy_pass` 转发到后端容器(JS对应 devServer proxy 生产版)
- Nginx 整合 HTTPS:listen 443 ssl + 证书路径(承接 day94)、80→443 跳转、托管前端静态 dist
- SSE 关键项:`proxy_buffering off`(否则流式被缓冲,打字机失效,承接第13周 day86)
- 进程守护:docker compose `restart: always` vs systemd service、开机自启、崩溃重启
- 运维查看:`docker compose logs`/`journalctl`/`systemctl status` 排查(JS对应 pm2 logs)

### 讲解

结论先行:Nginx 作为统一入口,对外只暴露 80/443、终结 HTTPS,再把请求 `proxy_pass` 给内网的后端容器(后端端口不再对公网开放,更安全);对 SSE 接口务必 `proxy_buffering off`。进程守护用 compose 的 `restart: always` 最省心(崩溃/重启机器后自动拉起)。下面是最小 Nginx server 配置演示(教学演示,**不是**产物答案;完整配置与守护方案由你完成)。

```nginx
# 教学演示:Nginx 反向代理 + HTTPS 最小 server 配置(非产物答案)
server {
    listen 443 ssl;                       # HTTPS 端口
    server_name yourname.com;
    ssl_certificate     /etc/letsencrypt/live/yourname.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourname.com/privkey.pem;
    location / {
        proxy_pass (http://127.0.0.1:8000;)  # 转发给后端容器(≈ devServer proxy)
        proxy_set_header Host $host;
        proxy_buffering off;               # SSE 流式必须关缓冲,否则打字机失效
    }
}
```

### 教材与章节

- Nginx 官方文档(已核验):(https://nginx.org/en/docs/) (ngx_http_proxy_module、Configuring HTTPS servers、WebSocket proxying)
- 中文搜索词:「Nginx 反向代理 proxy_pass 配置」「Nginx HTTPS 证书 配置 443」「Nginx SSE proxy_buffering off 流式」「systemd service 开机自启 进程守护」「docker compose restart always」
- 视频(A级,已核验):尚硅谷 Docker (https://www.atguigu.com/video/307) (compose restart/部署运维)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习 | 3h | Nginx 反代 proxy_pass、整合 HTTPS、SSE proxy_buffering、80→443、进程守护(restart/systemd)精读+实操 |
| 技术练习 | 2h | 配 Nginx 反代+HTTPS、设进程守护、验证域名 HTTPS 访问与崩溃自恢复、整理配置记录、extra 跟练 |
| 英语 | 0.5h | AI 辅助精读 Nginx 英文文档片段 |
| 输出 | 1h | GitHub commit(Nginx 配置/守护记录,无私钥);整理"反代+守护"为博客素材 |
| 复盘 | 0.5h | 补 index.md,写 devServer proxy→Nginx 生产反代迁移对照,自检后端端口不外露 |

### 当日产出

- [ ] 完成 学习产物/第14周/day96/nginx_proxy.conf:Nginx 反向代理 + HTTPS 配置(简洁可用为准,给要点)
  - 一个 `server` 块:listen 443 ssl + 证书路径(day94)、`server_name` 你的域名、`location /` 用 `proxy_pass` 转发到后端容器内网地址、对 SSE 路径 `proxy_buffering off`
  - 一个 80 端口 server 块:把 http 请求 301 跳转到 https
  - 可选:托管前端静态 dist(前端首页)与 `/api` 转发后端(前后端同域)
  - 验收点:浏览器 `(https://域名`) 命中服务(锁标志)、SSE 流式接口逐字到达不被缓冲;后端 8000 端口不再需要对公网开放(安全组可只留 443)
  - 所用知识点清单:Nginx server/location/proxy_pass、SSL 证书配置(day94)、HTTP→HTTPS 跳转、proxy_buffering off(SSE,承接第13周)、静态资源托管
  - 安全要求:证书私钥路径引用即可、**不粘贴私钥内容**;配置不含明文 key
- [ ] 完成 学习产物/第14周/day96/service_daemon.md:进程守护方案记录(compose `restart: always` 或 systemd 二选一,记录配置要点与"崩溃/重启服务器后自动恢复"的验证结果)
- [ ] 补记 学习产物/第14周/day96/index.md:覆盖全部学习内容

### JS→Python对照笔记

- JS devServer `proxy: {'/api': target}` → Nginx `location / { proxy_pass ... }`
- JS 平台自动 HTTPS 入口 → Nginx listen 443 ssl 终结证书 + 反代后端
- JS SSE 需关闭代理缓冲 → Nginx `proxy_buffering off`(否则打字机失效)
- JS pm2 崩溃重启/开机自启 → compose `restart: always` / systemd service
- JS `pm2 logs` 排查 → `docker compose logs -f` / `journalctl -u`

### 跟练清单(放extra/)

- extra_systemd_unit.md:写一个最小的 systemd service unit 示例(把 compose 或后端进程托管为系统服务:描述、启动命令、开机自启 WantedBy、重启策略),记录 `systemctl enable --now` 与 `systemctl status` 的验证结果,对比 compose `restart: always` 两种守护方式的适用场景。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| Nginx 反向代理/整合 HTTPS/SSE 缓冲/进程守护 | Nginx官方;尚硅谷Docker;搜索词 | nginx_proxy.conf + service_daemon.md | proxy_pass、SSL 配置、80→443、proxy_buffering off、restart/systemd、开机自启 |

【超前】标注集中区:Nginx upstream 负载均衡(多后端)、限流 limit_req、WAF、Gzip/HTTP2 深度调优、监控告警属【超前】,本日仅单后端反代 + 基础守护,不深入。
硬约束复查:仅用 day96 闭包知识点 ✓ key 零硬编码/不入库(私钥/ key 均不入配置明文)✓ 配置安全(后端端口不外露,仅开 80/443)✓ 交付物达成 ✓ extra/命名正确 ✓

---

## Day97(周六,7h)· 综合项目日:RAG/Agent 应用完整上线(访问地址 + 成本记录)

今天是项目日,把本周(服务器 + 域名 + HTTPS + 部署 + Nginx + 守护)与第13周容器化后端、第07-09周 RAG/Agent 能力拧成一个**公网可点开的完整 AI 应用**——这就是作品集项目1/项目2 的正式上线:面试官点开你的域名,能看到"前端提问 → FastAPI → RAG 检索 → 大模型流式回答"的全链路在线跑通。产出:公网 HTTPS 可访问的完整 AI 应用 + 上线记录(URL + 架构图 + 月度成本)。

💡 JS开发者速读:这就是你做过无数次的"项目上线",只是这次全栈自己扛——前端(第10-12周 React)+ 后端(第13周 FastAPI 容器)+ 云(本周)三层贯通,像一次完整的全栈发布;差异在于 DNS/证书/反代/守护/成本以前是平台代劳,现在你自己管;上线记录(URL + 架构图 + 成本)≈ 你写过的发布文档,但这次要进项目 README,是求职"在线可访问 + 成本数据"的硬证据(验证规则的作品集验收清单项)。

### 学习内容(综合复用,无全新理论)

- 前端上线:把第10-12周 React 流式前端 build 出 dist,用 Nginx 托管(或容器化),与后端同域/子域(JS对应 前端静态部署)
- 后端上线:生产 compose 起 FastAPI + 向量库(复用 day95),RAG 检索接大模型流式(复用第07-09、13周)
- 全链路打通:域名 + HTTPS(day93/94)+ Nginx 反代(day96)让"前端→FastAPI→RAG→大模型"公网可跑
- 进程守护确保 7×24 稳定(复用 day96);异常兜底与日志排查
- 成本核算:云服务器月度(对齐主计划 50-100 元/月)+ 大模型 token 成本;整理架构图/URL/成本为 README 素材

### 讲解

结论先行:完整上线的关键是"三层贯通 + 统一入口 + 守护兜底 + 成本可量化"——前端 dist 与后端容器都挂在 Nginx 这个统一 HTTPS 入口后,全链路走内网转发,进程守护保证稳定,最后把 URL/架构/成本沉淀进 README。下面只演示**公网全链路部署拓扑**(教学演示,**不是**产物答案,各层部署由你完成)。

```text
# 教学演示:公网 AI 应用全链路部署拓扑(结构演示,非产物答案)
用户浏览器
   │  (https://yourname.com(443,TLS) 加密)
   ▼
云服务器 Nginx(反向代理 + HTTPS 终结 + 托管前端 dist)
   │  proxy_pass (http://127.0.0.1:8000(SSE) 关缓冲)
   ▼
FastAPI 容器(SSE 流式接口,key 从 env 注入,零硬编码)
   ├──▶ 向量库容器(pgvector / Chroma:RAG 检索,卷持久化)
   └──▶ 国产大模型 API(通义千问 / DeepSeek / GLM)
进程守护:compose restart:always / systemd(崩溃自启、开机自启)
成本:轻量云 ~50-100 元/月 + 大模型 token(学习期 <200 元)
```

### 教材与章节

- 视频(A级,已核验):尚硅谷 Docker (https://www.atguigu.com/video/307) (综合部署);黑马 FastAPI (https://yun.itheima.com/course/1084.html) (服务综合)
- Nginx 官方文档(已核验):(https://nginx.org/en/docs/) (反代/静态托管综合);FastAPI 官方中文 (https://fastapi.tiangolo.com/zh/) (部署)
- 语法速查:廖雪峰 Python (https://liaoxuefeng.com/books/python/) (综合回顾);阿里云帮助中心 (https://help.aliyun.com/) (部署实践搜索)

### 时间分配

| 时段 | 时长 | 内容 |
| ---- | ---- | ---- |
| 技术学习/设计 | 2h | 画全链路拓扑、规划前后端上线与 Nginx 入口、想清异常/守护/成本口径(含英语 0.5h) |
| 项目实战 | 3.5h | 前端 dist 上线、后端生产 compose 起服务、域名 HTTPS 反代打通全链路、验证公网可访问 |
| 输出 | 1h | GitHub commit(确认 .env/私钥未上传);把架构图/在线 URL/成本整理为项目1 README 素材 |
| 复盘 | 0.5h | 补 index.md,自检闭包合规/key 安全/安全组,列可改进点 |

### 当日产出

- [ ] 完成 学习产物/第14周/day97/deploy_full.md:完整上线记录(核心交付)
  - 记录:公网 HTTPS 访问 URL、全链路部署步骤(前端 dist + 后端 compose + Nginx 反代 + HTTPS + 守护,可复现)、架构拓扑图(文字/简图)
  - 记录:月度成本核算(云服务器费用 + 大模型 token 估算,对齐主计划成本核算),作为项目 README 的"成本数据"
  - 验收点:面试官视角——浏览器打开 (https://域名,前端提问能流式收到"带) RAG 检索依据"的大模型回答;服务经进程守护,重启服务器后自动恢复
  - 所用知识点清单:前端静态部署、生产 docker compose(day95)、Nginx 反代+HTTPS(day94/96)、进程守护(day96)、RAG 检索(第07-08周)、大模型 API(第05-06周)、SSE 流式(第13周)、成本核算
- [ ] 完成 学习产物/第14周/day97/docker-compose.prod.yml:项目完整生产编排(项目日,相关配置/脚本 ≤150 行;整合前端/后端/向量库服务,key 走 env_file,.dockerignore 排除 .env)
- [ ] 补记 学习产物/第14周/day97/index.md:覆盖分层上线设计思路与全部学习内容

### JS→Python对照笔记

- JS 前端 build dist 部署静态托管 → Nginx 托管 dist(或前端容器化)
- JS 前后端分离各自部署 → Nginx 统一入口按域名/路径分流(前端 + /api 后端)
- JS 全栈发布文档 → deploy_full.md(URL + 架构图 + 成本,进 README)
- JS 平台自动扩缩/监控 → 本周单机 compose + 守护(K8s/监控属【超前】)
- JS `process.env` 平台注入 → 服务器 env_file 注入(key 零硬编码)

### 跟练清单(放extra/)

- extra_cost_report.md:做一份"月度运行成本核算表"——分项列出云服务器、域名、证书(免费/付费)、大模型 token(按预估调用量)的月度成本与合计,对齐主计划成本核算口径(轻量云 50-100 元/月、学习期 API <200 元),并给出 1-2 条降本建议(如小模型路由/缓存),作为项目 README 的成本数据支撑。

### 当日验收(合规区)

| 学习内容 | 教材章节 | 当日产物 | 产物所用知识点 |
| --- | --- | --- | --- |
| 前后端上线/Nginx 入口/HTTPS/守护/RAG 全链路/成本 | 尚硅谷Docker;Nginx官方;FastAPI官方中文;廖雪峰 | deploy_full.md + docker-compose.prod.yml | 前端静态部署、生产 compose、Nginx 反代+HTTPS、进程守护、RAG、大模型 API、SSE、成本核算 |

【超前】标注集中区:负载均衡/多实例、CI/CD 自动上线、监控告警(Prometheus/Grafana)、日志聚合、CDN、自动扩缩属【超前】,本日单机完整上线即可,不深入。
硬约束复查:仅用 day97 闭包知识点 ✓ **key 零硬编码/不入库(env_file 注入,.env/私钥不入库不进镜像)** ✓ 配置安全(安全组仅开 80/443)✓ 项目日交付物达成(相关配置/脚本 ≤150 行)✓ extra/命名正确 ✓

---

## Day98(周日,7h)· 周检测 / 阶段5闸门 + 对账

今天是本周闸门,也是**阶段5闸门**——六阶段技术栈闭环的最后一关(验证规则:day98 作品公网可点开,前端→FastAPI→LLM/RAG 全链路在线可用,含 HTTPS)。目标是限时独立把一个最小 FastAPI+SSE 服务用 docker compose 部署到云服务器,配好域名与 HTTPS,产出"公网 HTTPS 可访问 URL + 可复现部署步骤记录"。通过后即证明你能独立交付一个在线 AI 应用,六阶段技术栈(Python→大模型→RAG→Agent→前端 TS→FastAPI/Docker→云端部署)全部闭环,可正式进入阶段6(作品集打磨 + 求职)。

### 周检测(限时任务)

任务:45 分钟内,不翻教材、不照抄本周产物,独立完成 学习产物/第14周/day98/gate5_deploy.md(闸门交付:公网 HTTPS 可访问 URL + 可复现部署步骤记录)与配套最小 compose/配置:

1. 把一个最小 FastAPI 服务(含一个 SSE 流式接口,后端从环境变量读 key 调国产大模型;可复用第13周成果)用 docker compose 部署到云服务器并后台运行。
2. 配好域名 DNS 解析(A 记录指向服务器)+ HTTPS 证书(Let's Encrypt/云免费证书),浏览器 https 访问显示锁标志。
3. 用 Nginx 反向代理,使用户通过 `(https://域名`) 访问(而非直接暴露 IP:端口);SSE 接口 `proxy_buffering off` 保证流式。
4. 配进程守护(`restart: always` 或 systemd),服务崩溃/服务器重启后能自动恢复。
5. key 从服务器环境变量读、**零硬编码**,`.env` 不入库/不进镜像;安全组仅开放 22/80/443。
6. 产出 gate5_deploy.md:公网 HTTPS 可访问 URL + 从"拉代码/起容器 → 域名 HTTPS → 反代 → 守护"的可复现部署步骤 + 月度成本一行。

通过标准(须全部满足):

- 公网可通过 **HTTPS 域名**访问(浏览器锁标志、无"不安全"警告),SSE 流式接口逐字可用;
- 服务稳定运行(已配进程守护,重启服务器后自动恢复);
- **key 从服务器环境变量读取、零硬编码**,`.env`/证书私钥未入库、未进镜像;
- **备案已下发**(第7周提交、周期2-4周;境内域名访问未被拦截);
- 部署步骤可复现(gate5_deploy.md 记录完整,他人照做能重现同一在线服务);
- 仅用截至 day98 的闭包知识点;涉及的 .py(如检测服务)≤180 行(周末检测放宽),配置/脚本以简洁可用为准。

未通过补救方案:

- 个别配置错误(DNS 未生效/证书路径/Nginx 转发)→ 当天用缓冲 1h 对照 Day93/Day94/Day96 订正,重新部署并验证;
- **备案未下发** → 用 `IP + 端口` 临时演示并**明确标注"备案进行中"**,阶段5闸门**顺延但不取消**(备案下号后再补域名 + HTTPS 复验);
- HTTPS/反向代理不通 → 重做 Day94 + Day96,再走一次完整部署;
- 严重问题(服务器/网络不可用、结构混乱)→ 本周降级:阶段6前 2 天先补云端部署欠账,再进入作品集打磨,阶段5闸门顺延但不取消。

### 周日对账清单(4步)

1. 产物核对(逐项 ✅/❌/⚠️):
   - day92/server_init.md ☐ day92/setup_server.sh ☐ day92/extra/extra_firewall.md ☐ day92/index.md ☐
   - day93/dns_setup.md ☐ day93/extra/extra_subdomain.md ☐ day93/index.md ☐
   - day94/https_setup.md ☐ day94/extra/extra_cert_renew.md ☐ day94/index.md ☐
   - day95/docker-compose.prod.yml ☐ day95/deploy.md ☐ day95/extra/extra_env_prod.md ☐ day95/index.md ☐
   - day96/nginx_proxy.conf ☐ day96/service_daemon.md ☐ day96/extra/extra_systemd_unit.md ☐ day96/index.md ☐
   - day97/deploy_full.md ☐ day97/docker-compose.prod.yml ☐ day97/extra/extra_cost_report.md ☐ day97/index.md ☐
   - day98/gate5_deploy.md(闸门交付:公网 HTTPS URL + 部署步骤)☐
2. 填 README 进度跟踪表:完成%/自评 1-5/卡点/补救(第14周行);**阶段5闸门达成情况专项填 README**(公网 URL/是否 HTTPS/备案状态/是否全链路在线);**记录月度云成本,对齐主计划成本核算(轻量云 50-100 元/月)**。
3. 缺产物处理:缺 1-2 项用缓冲日补;缺 ≥3 项 → 阶段6前 2 天改补欠账。
4. 验收:公网 HTTPS URL 可访问、全链路(前端→FastAPI→LLM/RAG)在线跑通、进程守护生效(重启服务器自动恢复)、备案已下发;**确认全周无任何明文 key/证书私钥入库或进镜像**(.env 被 .gitignore/.dockerignore 排除)、**安全组仅开放 22/80/443**。

## 周尾附录:完整知识点累计清单(截至第14周day98)

第01-04周(已有):Python 基础(类型/控制流/数据结构/推导式/生成器表达式)、函数/模块/闭包/装饰器、OOP/魔术方法/文件读写/异常全体系、venv/pip/requirements.txt/requests/正则 re/类型提示 typing/asyncio。
第05-09周(已有):大模型 API 调用/环境变量读 key(零硬编码)/Prompt 工程/JSON Mode、流式 Streaming/Function Calling、LangChain/LCEL/RAG 全链路/向量库(Chroma/Milvus/Faiss)/Dify-Coze、引用标注/rerank/RAG 评测、Agent/Tool/Memory/LangGraph/MCP(认知)。
第10-12周(已有):TS SSE/流式渲染/打字机、Vercel AI SDK(useChat)/LangChain.js/工具调用可视化、Agent 交互模式/React 流式对话组件。
第13周(已有):FastAPI 路由/依赖注入 Depends/Pydantic/SSE 流式(StreamingResponse+异步生成器)、Docker 镜像/容器/Dockerfile/.dockerignore、docker-compose 多服务编排/env_file/depends_on、后端项目分层。

第14周(本周新增):

- 云服务器:ECS/轻量应用服务器选型、Linux 基础命令、SSH 密钥免密登录、安全组最小开放(22/80/443)、Docker 环境安装
- 域名与 DNS:域名购买实名、A 记录/CNAME 解析、TTL 生效、dig/nslookup/ping 验证、ICP 备案流程与状态确认
- HTTPS:TLS 原理(认知)、Let's Encrypt 免费证书、Certbot 申请与域名验证、证书自动续期、Nginx SSL 配置、HTTP→HTTPS 301 跳转
- Nginx 反向代理:server/location/proxy_pass、整合 HTTPS 终结、SSE `proxy_buffering off`、静态资源托管、80→443 跳转
- 上线部署与守护:代码/镜像上云(git clone/build)、生产 docker-compose(restart:always/env_file/无 reload/卷持久化)、进程守护(systemd/compose restart)、开机自启/崩溃重启、docker compose up -d/ps/logs 运维
- 成本与安全:部署成本核算(云服务器 + 大模型 token)、key 环境变量/secrets 注入零硬编码、.env 与证书私钥不入库/不进镜像、安全组最小开放
- **至此六阶段技术栈闭环完成(Python→大模型 API→RAG→Agent→前端 TS 流式→FastAPI/Docker→云端部署),阶段6转入作品集打磨与求职**
- 【超前】识别项(不要求掌握):Kubernetes、CI/CD 自动部署、负载均衡(Nginx upstream/多实例)、监控告警(Prometheus/Grafana)、日志聚合(ELK)、CDN、WAF/DDoS 高防、数据库主从与备份、蓝绿/金丝雀发布、IaC(Terraform/Ansible)

下周预告(第15周day99-105):阶段6作品集——完成旗舰项目1「商品知识库导购问答」并上线、写达标 README(架构图/成本数据/真实数据/在线可访问 URL/技术选型)、开源到 GitHub(累计 commits 冲 150+)。注:据 2026 市场修订版,阶段6转入求职,项目1需公网可访问且 README 含架构图与成本数据;同步启动项目3「电商素材优化微工具」(9.9 元/月付费闭环验证,不设收入 KPI);求职侧本周(第14周)已建立公司雷达池,第15周继续完善简历与 GitHub Profile。
