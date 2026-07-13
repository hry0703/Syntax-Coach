from __future__ import annotations

import uuid

from app.schemas.models import Mistake, MistakeCreate, MistakePatch, UserProfile

_MISTAKES: dict[str, Mistake] = {}
_PROFILE = UserProfile()


def list_mistakes() -> list[Mistake]:
    return list(_MISTAKES.values())


def create_mistake(payload: MistakeCreate) -> Mistake:
    item = Mistake(
        id=str(uuid.uuid4()),
        grammar_point_id=payload.grammar_point_id,
        original=payload.original,
        corrected=payload.corrected,
        scene_id=payload.scene_id,
        rule_zh=payload.rule_zh,
    )
    _MISTAKES[item.id] = item
    return item


def patch_mistake(mistake_id: str, payload: MistakePatch) -> Mistake | None:
    item = _MISTAKES.get(mistake_id)
    if item is None:
        return None
    data = item.model_dump()
    if payload.mastered is not None:
        data["mastered"] = payload.mastered
    updated = Mistake(**data)
    _MISTAKES[mistake_id] = updated
    return updated


def get_profile() -> UserProfile:
    return _PROFILE


def update_profile(payload: UserProfile) -> UserProfile:
    global _PROFILE
    _PROFILE = payload
    return _PROFILE
