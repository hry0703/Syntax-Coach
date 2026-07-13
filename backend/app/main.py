"""
FastAPI 应用入口 ≈ 前端的 createApp() + 全局插件。

启动：uv run uvicorn app.main:app --reload --port 8000
文档：http://127.0.0.1:8000/docs （Swagger，自带）

请求链路：Router → Pydantic 校验 → services →（Agent / DB）→ JSON
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, grammar, mistakes, profile, review, scenes
from app.db.database import init_db
from app.schemas.models import HealthResponse

OPENAPI_TAGS = [
    {"name": "health", "description": "服务探活"},
    {"name": "scenes", "description": "口语陪练场景"},
    {"name": "chat", "description": "会话与消息（含 Agent 语法卡）"},
    {"name": "grammar", "description": "本地语法点知识库"},
    {"name": "mistakes", "description": "错题本（SQLite）"},
    {"name": "review", "description": "复习（部分 stub）"},
    {"name": "profile", "description": "用户偏好（SQLite）"},
]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 启动时建表（没有则创建）—— 类似 migrate 的极简版
    init_db()
    yield


app = FastAPI(
    title="SyntaxCoach API",
    description=(
        "语法解析型口语陪练后端。\n\n"
        "主路径：选场景 → 对话 → 语法卡片 → 错题 → 复习。\n"
        "Agent：LangGraph（llm_turn → enrich_kb）；失败回退 stub。"
    ),
    version="0.1.0",
    openapi_tags=OPENAPI_TAGS,
    lifespan=lifespan,
)

# why：Vite :5173 调 :8000 跨域，需显式放行
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
)
def health() -> HealthResponse:
    return HealthResponse()


app.include_router(scenes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(grammar.router, prefix="/api")
app.include_router(mistakes.router, prefix="/api")
app.include_router(review.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
