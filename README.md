# SyntaxCoach

语法解析型口语陪练 Web：边聊边拆句，按语法点沉淀错题并带动复习。

> 当前为 **骨架阶段**：可启动前后端、展示双栏对话 + 语法卡片；业务 Agent / 持久化尚未接入。

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + TypeScript + Vue Router |
| 后端 | FastAPI + Uvicorn + Pydantic |
| 语法知识库 | 本地 JSON（按 id 读取） |
| Node | **22**（见根目录 `.nvmrc`） |
| 下一阶段 Agent | **LangChain + LangGraph + langchain-openai**（结构化输出 GrammarCard） |

前后端分离：`frontend/` 与 `backend/` 独立启动；开发时 Vite 将 `/api` 代理到 `http://127.0.0.1:8000`。

## 目录

```
syntaxCoach/
  frontend/          # Vue3 应用
  backend/
    app/             # FastAPI 路由 / schema / stub services
    data/
      scenes.json
      grammar_points/  # 语法点知识库示例
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

### 前端

```bash
cd frontend
npm install
npm run dev
```

页面：http://127.0.0.1:5173

## 主路径（产品）

选场景 → 对话 → 右侧语法卡片 → 加入薄弱语法点 → 复习（占位）

## 下一阶段已接入：Agent

入口：`backend/app/services/chat.py` → `app/services/agent.py`（LangGraph：`llm_turn` → `enrich_kb`）

行为：
1. 场景角色英文回复
2. 结构化语法卡片 JSON（失败则 stub 回退）
3. 按 `grammar_point_id` 用本地 KB 覆盖稳定 `rule_zh` / `examples`

配置见 `backend/.env`（参考 `.env.example`）。DeepSeek 兼容端点已适配（关闭 thinking + 纯 JSON 输出）。

后续可做：错题持久化、复习引擎、会话小结。
