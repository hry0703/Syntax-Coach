"""用户偏好路由 — SQLite 持久化。"""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.models import UserProfile
from app.services import memory_store

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=UserProfile, summary="获取用户偏好")
def get_profile() -> UserProfile:
    return memory_store.get_profile()


@router.patch("", response_model=UserProfile, summary="更新用户偏好")
def patch_profile(body: UserProfile) -> UserProfile:
    return memory_store.update_profile(body)
