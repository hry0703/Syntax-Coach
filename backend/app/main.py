from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, grammar, mistakes, profile, review, scenes
from app.schemas.models import HealthResponse

OPENAPI_TAGS = [
    {
        "name": "health",
        "description": "服务探活，用于确认后端进程可用。",
    },
    {
        "name": "scenes",
        "description": "口语陪练场景列表（角色 + 情境），开聊前先选场。",
    },
    {
        "name": "chat",
        "description": "会话与消息：创建场景会话、发送用户话轮，返回角色回复与结构化语法卡片。",
    },
    {
        "name": "grammar",
        "description": "本地语法点知识库（JSON）。Agent 出卡后会按 id 合并稳定规则与例句。",
    },
    {
        "name": "mistakes",
        "description": "错题本：按 grammar_point_id 沉淀薄弱点，支持标记已掌握。当前为内存存储。",
    },
    {
        "name": "review",
        "description": "基于薄弱语法点的复习抽题与提交（部分接口仍为占位）。",
    },
    {
        "name": "profile",
        "description": "用户偏好：难度、学习目标、纠错严格度与讲解详略。",
    },
]

app = FastAPI(
    title="SyntaxCoach API",
    description=(
        "语法解析型口语陪练后端。\n\n"
        "**主路径**：选场景 → 对话 → 右侧语法卡片 → 加入错题 → 复习。\n\n"
        "- 对话是入口，**结构化 GrammarCard** 是卖点（改对 + 讲规则）。\n"
        "- `severity: error` 表示明确错误；`suggestion` 表示更好说法。\n"
        "- 错题按 `grammar_point_id` 归档，不是只存聊天记录。\n"
        "- Agent：LangGraph（`llm_turn` → `enrich_kb`）；失败时 chat 回退 stub。\n\n"
        "交互文档：`/docs`（Swagger）与 `/redoc`。"
    ),
    version="0.1.0",
    openapi_tags=OPENAPI_TAGS,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/api/health",
    response_model=HealthResponse,
    tags=["health"],
    summary="健康检查",
    description="返回服务是否存活。前端或部署探活可轮询此接口；不依赖外部 LLM / 密钥。",
    response_description="正常时 `status` 为 `ok`。",
)
def health() -> HealthResponse:
    return HealthResponse()


app.include_router(scenes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(grammar.router, prefix="/api")
app.include_router(mistakes.router, prefix="/api")
app.include_router(review.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
