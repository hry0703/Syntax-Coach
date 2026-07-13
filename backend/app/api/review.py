"""复习路由 — 当前仍为 stub，见 TODO.md M3。"""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas.models import ReviewFeedback, ReviewItem, ReviewSubmit

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/today", response_model=list[ReviewItem], summary="获取今日复习题")
def today_review() -> list[ReviewItem]:
    return [
        ReviewItem(
            id="stub-1",
            type="correct_error",
            prompt="改错：I have went there yesterday.",
            grammar_point_id="past_vs_present_perfect",
        )
    ]


@router.post("/submit", response_model=ReviewFeedback, summary="提交复习答案")
def submit_review(body: ReviewSubmit) -> ReviewFeedback:
    return ReviewFeedback(
        correct=False,
        feedback=f"骨架占位点评（收到答案：{body.answer[:80]}）。后续由 Agent 评分。",
    )
