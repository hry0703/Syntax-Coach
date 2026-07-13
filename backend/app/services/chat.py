"""
对话编排服务（非 HTTP）。

View 调用这里；这里再决定走 Agent 还是 stub。
≈ 前端的 composable / store action：管会话状态，不直接碰 DOM。

会话目前仍在进程内存 `_SESSIONS`（重启会丢）；错题/偏好走 SQLAlchemy → SQLite。
"""

from __future__ import annotations

import logging
import uuid

from app.config import llm_configured
from app.kb.loader import get_grammar_point, load_scenes
from app.schemas.models import (
    ChatMessageResponse,
    CreateSessionResponse,
    ErrorSpan,
    GrammarCard,
)
from app.services.agent import run_coach_turn

logger = logging.getLogger(__name__)

# session_id → { scene, history, turn... }；多 worker 部署时需换 Redis/DB
_SESSIONS: dict[str, dict] = {}


def _find_scene(scene_id: str) -> dict:
    for scene in load_scenes():
        if scene.get("id") == scene_id:
            return scene
    return {
        "id": scene_id,
        "title_zh": scene_id,
        "title_en": scene_id,
        "role": "Coach",
        "level": "B1",
        "description": "General English practice",
    }


def create_session(scene_id: str, level: str | None = None) -> CreateSessionResponse:
    """开一场陪练：生成 session_id，前端后续发消息都带它。"""
    scene = _find_scene(scene_id)
    session_id = str(uuid.uuid4())
    _SESSIONS[session_id] = {
        "scene_id": scene_id,
        "scene": scene,
        "level": level or scene.get("level") or "B1",
        "turn": 0,
        "history": [],
    }
    return CreateSessionResponse(session_id=session_id, scene_id=scene_id)


def stub_grammar_card(user_text: str) -> GrammarCard:
    """
    LLM 未配置或 Agent 抛错时的兜底卡。

    why：接口不能因模型挂了就 500；前端仍能看到一版语法卡 UI。
    """
    point = get_grammar_point("past_vs_present_perfect") or {}
    original = user_text.strip() or "I have went here yesterday, so medium is fine."
    span_text = "have went"
    start = original.find(span_text)
    if start < 0:
        start = 0
        end = min(len(original), 9)
        label = "语法问题"
    else:
        end = start + len(span_text)
        label = "have + V-ed / 过去式冲突"

    return GrammarCard(
        grammar_point_id=point.get("id", "past_vs_present_perfect"),
        title_zh=point.get("title_zh", "现在完成时 vs 一般过去时"),
        cefr=point.get("cefr", "A2"),
        original=original,
        corrected="I went here yesterday, so medium is fine.",
        error_spans=[ErrorSpan(start=start, end=end, label=label)],
        rule_zh=point.get("rule_zh", ""),
        examples=point.get("examples", []),
        severity="error",
    )


def handle_message(session_id: str, content: str) -> ChatMessageResponse:
    """
    一轮对话：
      有密钥 → LangGraph Agent
      失败/无密钥 → stub 卡 + 友好英文回复
    最后把 user/assistant 写入 history（截断最近 20 条）。
    """
    session = _SESSIONS.get(session_id)
    if session is None:
        # 容错：未知 session 仍继续聊，避免前端刷新后整页挂掉
        session = {
            "scene_id": "unknown",
            "scene": _find_scene("unknown"),
            "level": "B1",
            "turn": 0,
            "history": [],
        }
        _SESSIONS[session_id] = session

    session["turn"] = int(session.get("turn", 0)) + 1
    history: list[dict[str, str]] = session.setdefault("history", [])

    reply: str
    card: GrammarCard | None

    if llm_configured():
        try:
            reply, card = run_coach_turn(
                user_text=content,
                scene=session.get("scene") or _find_scene(session["scene_id"]),
                history=history,
                level=session.get("level") or "B1",
            )
        except Exception:
            logger.exception("Coach agent failed; falling back to stub")
            reply = (
                "Sorry — I had a brief hiccup analyzing that. "
                "Let's continue: could you say that another way?"
            )
            card = stub_grammar_card(content)
    else:
        reply = (
            "Got it. (LLM not configured — using stub grammar card. "
            "Set OPENAI_API_KEY in backend/.env)"
        )
        card = stub_grammar_card(content)

    history.append({"role": "user", "content": content})
    history.append({"role": "assistant", "content": reply})
    session["history"] = history[-20:]

    return ChatMessageResponse(reply=reply, grammar_card=card, turn=session["turn"])
