from __future__ import annotations

from fastapi import APIRouter

from app.schemas.models import UserProfile
from app.services import memory_store

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get(
    "",
    response_model=UserProfile,
    summary="获取用户偏好",
    description=(
        "返回难度、学习目标、纠错严格度、讲解详略、是否显示术语等。\n\n"
        "MVP 为单用户内存配置；重启后端会回到默认值（除非后续接持久化）。"
    ),
    response_description="当前用户配置。",
)
def get_profile() -> UserProfile:
    return memory_store.get_profile()


@router.patch(
    "",
    response_model=UserProfile,
    summary="更新用户偏好",
    description=(
        "用请求体整份覆盖写入偏好（字段均有默认值）。\n\n"
        "设置页保存时调用；影响后续对话纠错力度与卡片讲解风格（Agent 侧逐步读取）。"
    ),
    response_description="更新后的完整配置。",
)
def patch_profile(body: UserProfile) -> UserProfile:
    return memory_store.update_profile(body)
