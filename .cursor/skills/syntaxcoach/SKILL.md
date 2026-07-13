---
name: syntaxcoach
description: >-
  Guides development of SyntaxCoach, a grammar-focused English speaking coach
  (Vue 3 + FastAPI). Use when working in the syntaxCoach repo, editing frontend
  chat/grammar-card UI, backend API/schemas/kb, scenes, mistakes/review flows,
  or wiring LangChain/LangGraph agents for GrammarCard output.
---

# SyntaxCoach

语法解析型口语陪练：对话是入口，**结构化语法卡片**是卖点；错题按**语法点**沉淀，再带动复习。

## Product rules

- 输出「改对 + 讲规则」，不是大段自由文本润色。
- 区分 **明确错误**（`severity: error`）与 **更好说法**（`suggestion`）。
- 错题本按 `grammar_point_id` 归档，不要只存聊天记录。
- MVP 不做：完整课程体系、游戏化、社交、原生 App、大而全 RAG。
- 知识库优先「语法点卡片库」（JSON 按 id）；向量 RAG 等语法点很多后再加。

## Stack (locked)

| Layer | Choice |
|-------|--------|
| Frontend | Vue 3 + Vite + TypeScript + Vue Router |
| Backend | FastAPI + Uvicorn + Pydantic（uv + `pyproject.toml`）|
| Persist | SQLite + SQLAlchemy（`app/db/`，错题/偏好）|
| KB | `backend/data/grammar_points/*.json` |
| Node | 22（根目录 `.nvmrc`） |
| Agent | LangChain + LangGraph + langchain-openai（已接入） |

Do **not** introduce React, Next.js, Nest, Streamlit, Django, or agent-craft-specific SDKs unless the user explicitly asks.

## Layout

```
frontend/src/
  pages/          Home, Chat, Mistakes, Review, History, Settings
  components/     TopBar, ChatPane, GrammarCard, ScenePicker
  api/            client + endpoints（/api proxy → :8000）
  styles/tokens.css
backend/app/
  main.py         FastAPI 入口 + CORS + lifespan 建表
  api/            scenes, chat, grammar, mistakes, review, profile
  schemas/models.py
  services/chat.py     ← Agent 接入点
  services/agent.py
  services/memory_store.py
  db/             SQLAlchemy engine + MistakeRow / ProfileRow
  kb/loader.py
backend/data/
  scenes.json
  grammar_points/
  syntaxcoach.db  # runtime
```

## UI conventions

- Desktop-first：左对话 / 右语法卡片（设计稿视觉在 `tokens.css`）。
- 品牌色：teal `#0f6b5c`，字体 Instrument Sans + Libre Baskerville。
- 语法卡片模块顺序固定：标题+CEFR → 原句高亮跨度 → 正误对比 → 规则 → 例句 → 操作。
- 样式用现有 CSS 变量；不要换成紫色渐变 / Inter 默认风。
- Vue SFC 块顺序：`<template>` 在上，`<script setup>` 在下。

## API / schema

`GrammarCard` 字段必须对齐前后端（见 [reference.md](reference.md)）：

`grammar_point_id`, `title_zh`, `cefr`, `original`, `corrected`, `error_spans[]`, `rule_zh`, `examples[]`, `severity`

改契约时：**同时**改 `backend/app/schemas/models.py` 与 `frontend/src/types/index.ts`。

## Agent wiring

已实现于 `backend/app/services/agent.py`：

1. LangGraph：`llm_turn` → `enrich_kb`
2. 纯 JSON 输出（兼容 DeepSeek；不依赖 json_schema / tool_choice）
3. 按 `grammar_point_id` 从 KB 合并稳定 `rule_zh` / `examples`
4. 失败时 `chat.py` 回退 stub；密钥用 `backend/.env`

改 Agent 时保持 `ChatMessageResponse` 形状不变。

## Workflow checklist

开发功能时：

1. 确认落在 P0（场景对话 / 语法卡片 / 错题 / 复习 / 设置）还是后置。
2. 后端先定 schema，再改前端类型与组件。
3. 新语法点：在 `backend/data/grammar_points/` 加 JSON，字段见 reference。
4. 本地验证：`cd backend && uv sync && uv run uvicorn app.main:app --reload --port 8000`；前端 `npm run dev` :5173；必要时打 `/docs`。

## References

- 分步 TODO：[TODO.md](../../../TODO.md)（仓库根目录）
- 契约与 JSON 示例：[reference.md](reference.md)
- 产品 README：仓库根目录 `README.md`
