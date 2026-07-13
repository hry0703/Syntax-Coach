# SyntaxCoach 开发 / 学习 TODO

边做边学：每项落地时在相关代码补「前端对照」注释。  
已完成的打 `[x]`，进行中的改 `[~]`，未开始保持 `[ ]`。

## 已完成

- [x] FastAPI + Pydantic API（路径与前端对齐）
- [x] 核心链路注释（main / api 路由 / schemas / chat / agent / kb / db）
- [x] SQLite + SQLAlchemy 持久化：`Mistake`、`UserProfile`
- [x] LangGraph Agent 基础：`llm_turn` → `enrich_kb`

---

## 下一步（按顺序做）

### M2 — Agent 加深

- [ ] 将 `UserProfile`（严格度 / 讲解详略）注入 Agent system prompt
- [ ] 新增图节点 `validate_spans`：校验 `error_spans` 下标合法，非法则修正或丢弃
- [ ] 小评测脚本：固定例句 → 检查 `grammar_point_id` 是否合理（可放 `backend/scripts/`）
- [ ] Agent 失败时打日志保留原始 LLM 文本，便于排查

### M3 — 复习闭环 + Tools

- [ ] `GET /api/review/today`：按未掌握错题（`mastered=false`）动态出题，去掉 stub
- [ ] `POST /api/review/submit`：真实判分（规则或 Agent），通过后可更新 `mastered`
- [ ] Agent Tool：`get_grammar_point(id)`，减少 prompt 里塞全量 catalog
- [ ] 会话小结：结束时汇总本场薄弱 `grammar_point_id`（可先 API，再接前端）

### M4 — 工程化

- [ ] 统一 API 错误格式（如 `{ "detail": "..." }`），前端错误提示对齐
- [ ] 基础测试：scenes / mistakes CRUD / chat stub 路径（pytest）
- [ ] 关键请求日志（session_id、turn、是否走 stub）
- [ ] （可选）会话持久化：`ChatSession` / 消息入 SQLite，替代内存 `_SESSIONS`
- [ ] （可选）Alembic 数据库迁移（表结构变更更规范）

---

## 刻意后置（先不做）

- [ ] 向量 RAG / 大而全知识检索
- [ ] 完整课程体系、游戏化、社交
- [ ] 多用户登录与权限
- [ ] 原生 App

---

## 技术栈（锁定）

| 层 | 技术 |
|---|---|
| 前端 | Vue 3 + Vite + TypeScript + Vue Router |
| 后端 | FastAPI + Uvicorn + Pydantic |
| 数据 | SQLite + SQLAlchemy |
| Agent | LangChain + LangGraph + langchain-openai |
| KB | `backend/data/grammar_points/*.json` |
| Node | 22（`.nvmrc`） |

## 建议阅读顺序（学的时候）

1. `backend/app/main.py` → `app/api/*.py`
2. `backend/app/schemas/models.py`
3. `backend/app/services/chat.py` → `agent.py`
4. `backend/app/db/` → `app/services/memory_store.py`
