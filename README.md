# SyntaxCoach

语法解析型口语陪练 Web：边聊边拆句，按语法点沉淀错题并带动复习。

> 当前为 **骨架阶段**：可启动前后端、双栏对话 + 语法卡片；错题/偏好已 SQLite 持久化。  
> 后续任务清单见根目录 [TODO.md](TODO.md)，按 M2 → M3 → M4 逐步实现。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + TypeScript + Vue Router |
| 后端 | FastAPI + Uvicorn + Pydantic |
| 数据 | SQLite + SQLAlchemy |
| Agent | LangChain + LangGraph + langchain-openai |
| 语法知识库 | 本地 JSON（按 id 读取） |
| Node | **22**（见根目录 `.nvmrc`） |

前后端分离：`frontend/` 与 `backend/` 独立启动；开发时 Vite 将 `/api` 代理到 `http://127.0.0.1:8000`。

## 目录

```
syntaxCoach/
  frontend/          # Vue3 应用
  backend/
    app/
      main.py        # FastAPI 入口
      api/           # 路由（≈ endpoints）
      schemas/       # Pydantic 模型
      services/      # chat + agent + memory_store
      db/            # SQLAlchemy
      kb/
    data/
      scenes.json
      grammar_points/
      syntaxcoach.db # 运行后自动生成
```

## 启动

### Node

```bash
nvm use   # 使用仓库 .nvmrc → Node 22
```

### 后端

需安装 [uv](https://docs.astral.sh/uv/)。

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

文档：http://127.0.0.1:8000/docs  
探活：http://127.0.0.1:8000/api/health

### 前端

```bash
cd frontend
npm install
npm run dev
```

页面：http://127.0.0.1:5173

## 主路径（产品）

选场景 → 对话 → 右侧语法卡片 → 加入薄弱语法点 → 复习（占位）

## Agent

入口：`backend/app/services/chat.py` → `app/services/agent.py`（LangGraph：`llm_turn` → `enrich_kb`）

配置见 `backend/.env`（参考 `.env.example`）。

后续可做：见 [TODO.md](TODO.md)。
