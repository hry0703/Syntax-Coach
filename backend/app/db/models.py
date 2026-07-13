"""
数据库层（SQLAlchemy）≈ Django ORM / 前端「持久化 store」。

开发用 SQLite 单文件：backend/data/syntaxcoach.db
表结构在 models；session 在 database.py。
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MistakeRow(Base):
    """错题表；归档键 grammar_point_id。"""

    __tablename__ = "mistakes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    grammar_point_id: Mapped[str] = mapped_column(String(128), index=True)
    original: Mapped[str] = mapped_column(Text)
    corrected: Mapped[str] = mapped_column(Text)
    scene_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    rule_zh: Mapped[str | None] = mapped_column(Text, nullable=True)
    mastered: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ProfileRow(Base):
    """MVP 单用户偏好；固定 id=1。"""

    __tablename__ = "user_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(String(8), default="B1")
    goal: Mapped[str] = mapped_column(String(16), default="speaking")
    correction_strictness: Mapped[str] = mapped_column(String(16), default="standard")
    explanation_detail: Mapped[str] = mapped_column(String(16), default="standard")
    show_terms: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
