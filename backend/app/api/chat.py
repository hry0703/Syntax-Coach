"""
FastAPI 路由 ≈ 前端 endpoints.ts / vue-router。

每个 APIRouter 一组资源；在 main.py 里 include，前缀 /api。
"""

from __future__ import annotations

from fastapi import APIRouter, Path

from app.exceptions import AppError
from app.schemas.models import (
    ChatMessageRequest,
    ChatMessageResponse,
    CreateSessionRequest,
    CreateSessionResponse,
)
from app.services import chat as chat_service

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "/sessions",
    response_model=CreateSessionResponse,
    summary="创建对话会话",
)
def create_session(body: CreateSessionRequest) -> CreateSessionResponse:
    """对应前端 createSession(sceneId)。"""
    return chat_service.create_session(body.scene_id, body.level)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse,
    summary="发送用户消息并获取回复",
)
def post_message(
    body: ChatMessageRequest,
    session_id: str = Path(..., description="创建会话时返回的 session_id"),
) -> ChatMessageResponse:
    """对应前端 sendMessage()；真正 Agent 在 services/chat.py。"""
    if not body.content.strip():
        raise AppError("content is required", status_code=400)
    return chat_service.handle_message(session_id, body.content)
