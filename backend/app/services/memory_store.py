"""
错题 / 偏好读写门面。

Views/Routers 只调这里；底层是 SQLAlchemy（换库时尽量只改本文件）。
"""

from __future__ import annotations

import uuid

from app.db.database import get_session
from app.db.models import MistakeRow, ProfileRow
from app.schemas.models import Mistake, MistakeCreate, MistakePatch, UserProfile

_PROFILE_ID = 1


def _mistake_from_row(row: MistakeRow) -> Mistake:
    return Mistake(
        id=row.id,
        grammar_point_id=row.grammar_point_id,
        original=row.original,
        corrected=row.corrected,
        scene_id=row.scene_id,
        rule_zh=row.rule_zh,
        mastered=row.mastered,
    )


def _profile_from_row(row: ProfileRow) -> UserProfile:
    return UserProfile(
        level=row.level,  # type: ignore[arg-type]
        goal=row.goal,  # type: ignore[arg-type]
        correction_strictness=row.correction_strictness,  # type: ignore[arg-type]
        explanation_detail=row.explanation_detail,  # type: ignore[arg-type]
        show_terms=row.show_terms,
    )


def list_mistakes() -> list[Mistake]:
    with get_session() as session:
        rows = session.query(MistakeRow).order_by(MistakeRow.created_at.desc()).all()
        return [_mistake_from_row(row) for row in rows]


def create_mistake(payload: MistakeCreate) -> Mistake:
    with get_session() as session:
        row = MistakeRow(
            id=str(uuid.uuid4()),
            grammar_point_id=payload.grammar_point_id,
            original=payload.original,
            corrected=payload.corrected,
            scene_id=payload.scene_id,
            rule_zh=payload.rule_zh,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return _mistake_from_row(row)


def patch_mistake(mistake_id: str, payload: MistakePatch) -> Mistake | None:
    with get_session() as session:
        row = session.get(MistakeRow, mistake_id)
        if row is None:
            return None
        if payload.mastered is not None:
            row.mastered = payload.mastered
            session.commit()
            session.refresh(row)
        return _mistake_from_row(row)


def get_profile() -> UserProfile:
    with get_session() as session:
        row = session.get(ProfileRow, _PROFILE_ID)
        if row is None:
            row = ProfileRow(id=_PROFILE_ID)
            session.add(row)
            session.commit()
            session.refresh(row)
        return _profile_from_row(row)


def update_profile(payload: UserProfile) -> UserProfile:
    with get_session() as session:
        row = session.get(ProfileRow, _PROFILE_ID)
        if row is None:
            row = ProfileRow(id=_PROFILE_ID)
            session.add(row)
        row.level = payload.level
        row.goal = payload.goal
        row.correction_strictness = payload.correction_strictness
        row.explanation_detail = payload.explanation_detail
        row.show_terms = payload.show_terms
        session.commit()
        session.refresh(row)
        return _profile_from_row(row)
