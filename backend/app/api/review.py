from __future__ import annotations

from fastapi import APIRouter

from app.schemas.models import ReviewFeedback, ReviewItem, ReviewSubmit

router = APIRouter(prefix="/review", tags=["review"])


@router.get(
    "/today",
    response_model=list[ReviewItem],
    summary="获取今日复习题",
    description=(
        "按薄弱语法点抽题，供复习页展示。\n\n"
        "**当前为 stub**：固定返回一道改错示例；"
        "后续会根据错题本 `mastered=false` 的语法点动态出题。"
    ),
    response_description="今日题目列表（可为空数组）。",
)
def today_review() -> list[ReviewItem]:
    # stub：后续按薄弱语法点抽题
    return [
        ReviewItem(
            id="stub-1",
            type="correct_error",
            prompt="改错：I have went there yesterday.",
            grammar_point_id="past_vs_present_perfect",
        )
    ]


@router.post(
    "/submit",
    response_model=ReviewFeedback,
    summary="提交复习答案",
    description=(
        "提交某道复习题的作答，返回对错与短评。\n\n"
        "**当前为 stub**：不真正判分，仅回显收到的答案片段；"
        "后续由 Agent / 规则引擎评分，并可能回写错题 `mastered`。"
    ),
    response_description="是否正确 + 中文反馈文案。",
)
def submit_review(body: ReviewSubmit) -> ReviewFeedback:
    return ReviewFeedback(
        correct=False,
        feedback=f"骨架占位点评（收到答案：{body.answer[:80]}）。后续由 Agent 评分。",
    )
