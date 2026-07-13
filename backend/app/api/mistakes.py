"""错题本路由 — 数据经 memory_store 落 SQLite。"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from app.schemas.models import Mistake, MistakeCreate, MistakePatch
from app.services import memory_store

router = APIRouter(prefix="/mistakes", tags=["mistakes"])


@router.get("", response_model=list[Mistake], summary="列出错题本")
def list_mistakes() -> list[Mistake]:
    return memory_store.list_mistakes()


@router.post("", response_model=Mistake, status_code=201, summary="加入一条错题")
def create_mistake(body: MistakeCreate) -> Mistake:
    return memory_store.create_mistake(body)


@router.patch("/{mistake_id}", response_model=Mistake, summary="更新错题（掌握状态）")
def patch_mistake(
    body: MistakePatch,
    mistake_id: str = Path(..., description="错题记录 id"),
) -> Mistake:
    updated = memory_store.patch_mistake(mistake_id, body)
    if updated is None:
        raise HTTPException(status_code=404, detail="mistake not found")
    return updated
