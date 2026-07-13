"""场景列表路由 — 对应前端 fetchScenes()。"""

from __future__ import annotations

from fastapi import APIRouter

from app.kb.loader import load_scenes
from app.schemas.models import Scene

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.get("", response_model=list[Scene], summary="列出全部陪练场景")
def get_scenes() -> list[Scene]:
    return [Scene(**s) for s in load_scenes()]
