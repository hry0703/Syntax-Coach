# AI Agent 开发 · 岗位导向分段学习计划

> 依据 Boss 直聘 / 猎聘 / 大厂 JD，以及约 101 份 Agent 岗位技能统计整理  
> 目标：达到可投递 **AI Agent / 大模型应用开发** 的水平  
> 建议总时长：**3～4 个月**（每周约 10～15 小时）  
> 用法：按段学习，完成一项就勾选 `- [ ]` → `- [x]`

---

## 市场在招什么（先建立预期）

### 几乎必提
- [ ] 了解：Python 是绝对主语言
- [ ] 了解：RAG + 向量库 ≈ 标配
- [ ] 了解：LangChain / LangGraph 被点名最多
- [ ] 了解：Prompt / Tool Calling / Agent 编排
- [ ] 了解：要能从 0 到 1 落地业务，不是只会调 Chat API

### 明显加分 / 中高级
- [ ] 了解：多 Agent 协作
- [ ] 了解：MCP / OpenAPI 工具标准化
- [ ] 了解：评测体系、可观测（tracing）
- [ ] 了解：FastAPI、Docker、流式、稳定性与成本
- [ ] 了解：第二语言 Java / Go（后端岗常见）

### 多数应用岗「了解即可」（别一上来深挖）
- [ ] 知道：深度学习炼丹不是入门重点
- [ ] 知道：LoRA / SFT 多出现在高薪岗

**岗位本质**：把不确定的模型输出，工程化成可靠业务流程。

---

## 优先级总表

| 优先级 | 内容 | 状态 |
|--------|------|------|
| **P0** | Python、FastAPI、LLM API、Prompt、RAG、Tool Calling、Agent 循环 | 必学 |
| **P1** | LangGraph/LangChain、流式、评测、Docker、多轮记忆 | 简历核心 |
| **P2** | MCP、Multi-Agent、Rerank、可观测与成本 | 拉开差距 |
| **P3** | 深度训练 / 复杂微调 | 以后再说 |

---

## 每周节奏

- 理论 ≤ 30%：文档 + 少量文章
- 动手 ≥ 70%：只服务「当前阶段作品」
- 周末至少 1 次：能演示给别人看 + 写几行复盘

---

## 第 0 段｜地基（约 2 周）

### 学什么
- [ ] Python：函数 / 类 / 异常 / 模块
- [ ] 类型提示（Type Hints）基础
- [ ] 虚拟环境（venv / Poetry 任选其一；本仓库后端用 **uv**）
- [ ] HTTP / JSON、REST 基本概念
- [ ] Git：clone / commit / push / 分支基础
- [ ] `async` / `await` 入门

### 动手任务（你来写，按顺序做）

建议目录：仓库外自建 `learn-py0/`，或本仓库 `doc/exercises/w0/`（勿提交密钥）。  
每题写完在旁边记一句话：「对应前端的 ___」。

#### Day 1～3｜Python 语法手感
- [x] **T0-1 函数**：写 `normalize(text: str) -> str`，去掉首尾空白；空串返回 `""`。再写测试：`"  hi  "` → `"hi"`
- [x] **T0-2 类**：写 `Scene` 类，字段 `id / title_zh / level`；实现 `__str__` 打印可读一行
- [x] **T0-3 异常**：读一个不存在的文件路径，用 `try/except FileNotFoundError` 打印友好中文，不要让进程裸崩
- [x] **T0-4 模块**：把上面函数/类拆成 `utils.py` + `main.py`，用 `from utils import ...` 调用

#### Day 4～5｜类型提示
- [x] **T0-5**：给 T0-1～T0-2 全部补上 Type Hints（参数、返回值）
- [x] **T0-6**：写函数 `load_scenes(path: str) -> list[dict[str, str]]`，用 `json.load` 读本仓库 `backend/data/scenes.json`（只读，别改文件）
- [x] **T0-7**：用 `str | None` 写一个可选参数：`find_scene(scenes, scene_id) -> dict | None`

#### Day 6～7｜虚拟环境与依赖
- [x] **T0-8**：用 `uv`（或 venv）新建环境；`pip/uv add httpx`（或 `requests`），`uv sync` / 冻结依赖
- [ ] **T0-9**：写脚本请求公开 API（如 `https://httpbin.org/get`），打印 status code + JSON 里某个字段
- [ ] **T0-10**：故意写错包名安装，看报错；再故意 `import` 未安装的包，看报错 —— 笔记里各记一行「怎么读」

#### Day 8～10｜HTTP / JSON / REST
- [ ] **T0-11 概念笔记**：用自己的话写清 GET vs POST、JSON body、状态码 200/400/404/500（半页即可）
- [ ] **T0-12**：用 curl 或脚本打本仓库后端（需先 `uv run uvicorn ...`）：`GET /api/health`、`GET /api/scenes`，把响应 JSON 存成文件
- [ ] **T0-13**：对照前端 `fetchScenes()`，画一张「浏览器 → Vite 代理 → FastAPI → JSON」箭头图（可贴在笔记）

#### Day 11～12｜async 入门
- [ ] **T0-14**：写 `async def fetch_twice()`：用 `httpx.AsyncClient`（或 `asyncio.sleep` 模拟）并发等两个「慢请求」，对比同步版耗时（打印秒数即可）
- [ ] **T0-15 笔记**：回答——为什么读文件/调 LLM 适合 async？为什么算斐波那契不一定适合？

### 练到什么程度
- [ ] 能独立写脚本、调第三方 HTTP API
- [ ] 会建虚拟环境、装依赖、读懂常见报错
- [ ] T0-1～T0-15 多数能独立完成（卡住查文档，不靠复制整题答案）

### 本段不做
- 框架深挖、RAG、Agent、Pydantic 细节（第 1 段再上）

### 推荐笔记
- `01-Python基础.md`
- `Python虚拟环境配置指南.md`
- `Poetry常用命令.md`（若用 uv，可另开 `uv常用命令.md`）

### 段末自检
- [ ] 能解释：进程默认单线程执行；异步适合 I/O
- [ ] 能写一个带异常处理的小脚本
- [ ] 能不看笔记说出：`uv sync` ≈ `npm install`；Type Hints ≈ TS 类型但运行时默认不强制（除非 Pydantic/检查器）

---

## 第 1 段｜Web 服务 + LLM 调用（约 2～3 周）

### 学什么
- [ ] FastAPI + Pydantic
- [ ] `.env` 管理 API Key（不进 Git）
- [ ] OpenAI / 国产大模型 Chat Completions API
- [ ] 流式输出（SSE）概念与简单实现
- [ ] Prompt 基础：system / user、少样本、输出格式约束
- [ ] temperature、max_tokens、多轮 history

### 练到什么程度
- [ ] 做一个「对话 API」：`POST /chat`，支持多轮
- [ ] 能讲清：流式 vs 非流式的区别

### 作品里程碑 A
- [ ] **Chat API 服务**（本地可用 Swagger / curl 演示）

### 推荐笔记
- `02-FastAPI后端开发.md`
- `03-LLM基础与应用.md`
- `Uvicorn和ASGI详解.md`

### 段末自检
- [ ] 接口有请求体校验与错误返回
- [ ] Key 只放在环境变量里
- [ ] 能画一张「客户端 → FastAPI → LLM」流程图

---

## 第 2 段｜RAG（约 3～4 周）

> JD 里出现频率最高的一块之一

### 学什么
- [ ] Embedding 是什么、为什么要向量化
- [ ] 文本切分：chunk size / overlap
- [ ] 向量库任选其一：Chroma / FAISS / pgvector
- [ ] 检索 Top-K → 拼进 Prompt → 生成
- [ ] 「仅依据文档回答」与拒答策略
- [ ] （加分）混合检索或 Rerank，做一次效果对比

### 练到什么程度
- [ ] 本地文档可入库、可更新、可问答
- [ ] 能说明：为什么会胡编、检索差时怎么改

### 作品里程碑 B
- [ ] **文档问答 RAG**（知识库可重建）

### 推荐笔记
- `05-RAG系统开发.md`

### 段末自检
- [ ] 能解释：召回差 vs 生成胡编，分别怎么排查
- [ ] 换一种切分策略，并记录效果差异（哪怕很简陋）

---

## 第 3 段｜Agent 核心（约 4～5 周）

> 和「聊天 Bot」拉开差距的关键段

### 学什么
- [ ] Function Calling / Tool Calling
- [ ] Agent 循环：ReAct（思考 → 工具 → 观察 → 再答）
- [ ] 短期记忆（对话 history）
- [ ] 长期记忆概念（摘要 / 向量记忆，先概念后实现）
- [ ] **先手写一版**小循环，再学框架
- [ ] LangChain **或** LangGraph（先精通一个）
- [ ] （了解）MCP、OpenAPI 工具封装是为了什么

### 练到什么程度
- [ ] Agent 至少挂 **2～3 个工具**（如：搜知识库、HTTP API、计算器）
- [ ] 能画架构图：何时检索、何时调工具、失败怎么处理

### 作品里程碑 C
- [ ] **带工具的任务型 Agent**（不只是问答）

### 推荐笔记
- `04-LangChain框架.md`
- `06-Agent开发实战.md`

### 段末自检
- [ ] 能口述一轮完整 ReAct 例子
- [ ] 工具失败时有降级或明确报错，而不是卡死
- [ ] 能说清：什么时候不该用 Agent（简单问答直接调模型即可）

---

## 第 4 段｜工程化与评测（约 3～4 周）

> 中高级 JD 很看重「能量化、能上线」

### 学什么
- [ ] 日志与 tracing（每次 prompt / tool 可复盘）
- [ ] 简单评测集（20～50 题：正确率、拒答率、延迟）
- [ ] Docker 打包部署
- [ ] 限流、超时、重试
- [ ] Token / 成本意识
- [ ] （选做）多 Agent：规划者 + 执行者

### 练到什么程度
- [ ] 一套服务：Docker 可启动
- [ ] README 有架构图与效果说明
- [ ] 面试能讲：「输出不确定，我怎么做成可靠流程」

### 作品里程碑 D
- [ ] **可展示的完整 Agent 项目**（GitHub + 演示）

### 推荐笔记
- `07-全栈项目实战.md`
- `08-工具与资源.md`

### 段末自检
- [ ] 别人按 README 能跑起来
- [ ] 有至少一页「评测结果 / 已知局限」

---

## 第 5 段｜按岗位选修（持续）

### 互联网应用岗
- [ ] 再补一门 Go 或 Java
- [ ] 系统设计基础
- [ ] 高并发 / 缓存基础概念

### 平台 / 低代码智能体
- [ ] Dify 或同类工作流编排
- [ ] 权限与多租户概念

### 冲高薪 / 偏算法
- [ ] LoRA / SFT 入门
- [ ] 更系统的评测与数据飞轮

### 对标最新 JD
- [ ] MCP 实战小 demo
- [ ] Multi-Agent 协作小 demo

---

## 四段作品线（投简历用）

按顺序完成，简历/作品集直接用：

| 序号 | 作品 | 对应阶段 | 完成 |
|------|------|----------|------|
| 1 | Chat API（多轮 + 流式） | 第 1 段 | [ ] |
| 2 | RAG 文档问答 | 第 2 段 | [ ] |
| 3 | Tool Agent（检索 + 外部工具） | 第 3 段 | [ ] |
| 4 | 工程化（Docker + 评测 + 架构图 README） | 第 4 段 | [ ] |

市场要的组合：**Python + RAG + Agent 编排 + 能落地**。

---

## 学习记录（自己填）

| 日期 | 学了哪段 | 做了什么 | 卡点 | 下周计划 |
|------|----------|----------|------|----------|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

---

## 相关笔记索引

| 文件 | 内容 |
|------|------|
| [01-Python基础.md](./01-Python基础.md) | Python 基础 |
| [02-FastAPI后端开发.md](./02-FastAPI后端开发.md) | FastAPI |
| [03-LLM基础与应用.md](./03-LLM基础与应用.md) | LLM API / Prompt |
| [04-LangChain框架.md](./04-LangChain框架.md) | LangChain |
| [05-RAG系统开发.md](./05-RAG系统开发.md) | RAG |
| [06-Agent开发实战.md](./06-Agent开发实战.md) | Agent |
| [07-全栈项目实战.md](./07-全栈项目实战.md) | 全栈整合 |
| [08-工具与资源.md](./08-工具与资源.md) | 工具资源 |
| [README.md](./README.md) | 原完整学习路线（可对照） |
| [uv常用命令.md](./uv常用命令.md) | T0-8：虚拟环境、uv add / sync、锁文件 |

---

## 一句话提醒

先把 **P0 → 作品 A/B/C** 做完，再追框架和新名词。  
散学数据库方言、多进程细节，不如把 Agent 作品线做深。
