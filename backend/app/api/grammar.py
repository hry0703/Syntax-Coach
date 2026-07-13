"""语法点 KB 路由。"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from app.kb.loader import get_grammar_point, list_grammar_points
from app.schemas.models import GrammarPoint

router = APIRouter(prefix="/grammar-points", tags=["grammar"])


@router.get("", response_model=list[GrammarPoint], summary="列出语法点知识库")
def list_points() -> list[GrammarPoint]:
    return [GrammarPoint(**p) for p in list_grammar_points()]


@router.get("/{point_id}", response_model=GrammarPoint, summary="按 id 获取单个语法点")
def get_point(
    point_id: str = Path(..., description="语法点 id"),
) -> GrammarPoint:
    point = get_grammar_point(point_id)
    if point is None:
        raise HTTPException(status_code=404, detail="grammar point not found")
    return GrammarPoint(**point)
