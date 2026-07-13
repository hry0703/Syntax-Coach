from __future__ import annotations

from fastapi import APIRouter

from app.kb.loader import load_scenes
from app.schemas.models import Scene

router = APIRouter(prefix="/scenes", tags=["scenes"])


@router.get(
    "",
    response_model=list[Scene],
    summary="列出全部陪练场景",
    description=(
        "读取 `data/scenes.json`，返回可选场景列表。\n\n"
        "每个场景含角色（`role`）、建议难度（`level`）与简介。"
        "前端选场后，用场景 `id` 调用 `POST /api/chat/sessions` 开聊。"
    ),
    response_description="场景数组；当前为静态配置，无分页。",
)
def get_scenes() -> list[Scene]:
    return [Scene(**s) for s in load_scenes()]
