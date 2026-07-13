from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path

from app.kb.loader import get_grammar_point, list_grammar_points
from app.schemas.models import GrammarPoint

router = APIRouter(prefix="/grammar-points", tags=["grammar"])


@router.get(
    "",
    response_model=list[GrammarPoint],
    summary="列出语法点知识库",
    description=(
        "读取 `data/grammar_points/*.json`，返回全部语法点卡片。\n\n"
        "字段含规则、常见错例、例句等。"
        "对话出卡后，Agent 会按 id 用这里的稳定文案覆盖 `rule_zh` / `examples`。"
    ),
    response_description="语法点数组；无分页。",
)
def list_points() -> list[GrammarPoint]:
    return [GrammarPoint(**p) for p in list_grammar_points()]


@router.get(
    "/{point_id}",
    response_model=GrammarPoint,
    summary="按 id 获取单个语法点",
    description="用于错题详情、复习题干或前端直接展示某语法点说明。不存在则 404。",
    response_description="对应语法点卡片。",
    responses={404: {"description": "语法点不存在"}},
)
def get_point(
    point_id: str = Path(
        ...,
        description="语法点 id，与 JSON 文件名 / grammar_point_id 一致",
        examples=["past_vs_present_perfect"],
    ),
) -> GrammarPoint:
    point = get_grammar_point(point_id)
    if point is None:
        raise HTTPException(status_code=404, detail="grammar point not found")
    return GrammarPoint(**point)
