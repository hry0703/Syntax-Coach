from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

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
    description=(
        "按场景开启一轮口语陪练会话。\n\n"
        "- `scene_id` 须存在于场景列表。\n"
        "- `level` 可选，用于覆盖用户默认难度。\n"
        "- 返回的 `session_id` 用于后续发送消息。\n\n"
        "会话目前存于内存；重启后端会丢失。"
    ),
    response_description="新建会话的 id、绑定场景与状态。",
    status_code=200,
)
def create_session(body: CreateSessionRequest) -> CreateSessionResponse:
    return chat_service.create_session(body.scene_id, body.level)


@router.post(
    "/sessions/{session_id}/messages",
    response_model=ChatMessageResponse,
    summary="发送用户消息并获取回复",
    description=(
        "在指定会话中提交用户本轮英文输入。\n\n"
        "**处理流程**：\n"
        "1. Agent（LangGraph）生成场景角色英文回复；\n"
        "2. 尝试产出结构化 `grammar_card`（纯 JSON）；\n"
        "3. 按 `grammar_point_id` 用本地 KB 合并稳定 `rule_zh` / `examples`；\n"
        "4. Agent / 解析失败时回退 stub，保证接口仍可返回。\n\n"
        "`content` 不能为空或纯空白，否则 400。"
    ),
    response_description="角色回复、可选语法卡片、当前回合号。",
    responses={
        400: {"description": "content 为空或仅空白"},
    },
)
def post_message(
    body: ChatMessageRequest,
    session_id: str = Path(..., description="创建会话时返回的 session_id"),
) -> ChatMessageResponse:
    if not body.content.strip():
        raise HTTPException(status_code=400, detail="content is required")
    return chat_service.handle_message(session_id, body.content)
