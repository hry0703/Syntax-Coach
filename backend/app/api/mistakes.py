from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from app.schemas.models import Mistake, MistakeCreate, MistakePatch
from app.services import memory_store

router = APIRouter(prefix="/mistakes", tags=["mistakes"])


@router.get(
    "",
    response_model=list[Mistake],
    summary="列出错题本",
    description=(
        "返回当前用户（MVP：单机内存）全部错题。\n\n"
        "归档维度是 `grammar_point_id`，便于按语法点复习，而不是按聊天消息堆叠。"
    ),
    response_description="错题列表。",
)
def list_mistakes() -> list[Mistake]:
    return memory_store.list_mistakes()


@router.post(
    "",
    response_model=Mistake,
    status_code=201,
    summary="加入一条错题",
    description=(
        "通常来自语法卡片「加入薄弱点」操作。\n\n"
        "必填：`grammar_point_id`、`original`、`corrected`；"
        "`scene_id` / `rule_zh` 可选，便于回溯场景与规则快照。"
    ),
    response_description="已创建的错题记录（含生成的 id）。",
)
def create_mistake(body: MistakeCreate) -> Mistake:
    return memory_store.create_mistake(body)


@router.patch(
    "/{mistake_id}",
    response_model=Mistake,
    summary="更新错题（掌握状态）",
    description="目前仅支持更新 `mastered`。复习通过或用户手动标记后调用。不存在则 404。",
    response_description="更新后的错题。",
    responses={404: {"description": "错题不存在"}},
)
def patch_mistake(
    body: MistakePatch,
    mistake_id: str = Path(..., description="错题记录 id"),
) -> Mistake:
    updated = memory_store.patch_mistake(mistake_id, body)
    if updated is None:
        raise HTTPException(status_code=404, detail="mistake not found")
    return updated
