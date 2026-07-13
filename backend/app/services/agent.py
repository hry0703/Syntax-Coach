from __future__ import annotations

import json
import re
from typing import Any, Literal, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

from app.config import get_settings
from app.kb.loader import get_grammar_point, list_grammar_points
from app.schemas.models import ErrorSpan, GrammarCard


class LlmErrorSpan(BaseModel):
    start: int
    end: int
    label: str


class LlmGrammarCard(BaseModel):
    grammar_point_id: str
    title_zh: str
    cefr: str
    original: str
    corrected: str
    error_spans: list[LlmErrorSpan] = Field(default_factory=list)
    rule_zh: str = ""
    examples: list[str] = Field(default_factory=list)
    severity: Literal["error", "suggestion"] = "error"


class CoachTurn(BaseModel):
    reply: str
    has_grammar_issue: bool = False
    grammar_card: LlmGrammarCard | None = None


class CoachState(TypedDict):
    user_text: str
    scene: dict[str, Any]
    history: list[dict[str, str]]
    level: str
    reply: str
    grammar_card: GrammarCard | None


def _build_llm() -> ChatOpenAI:
    settings = get_settings()
    kwargs: dict[str, Any] = {
        "model": settings["openai_model"],
        "api_key": settings["openai_api_key"],
        "base_url": settings["openai_base_url"],
        "temperature": 0.4,
    }
    # DeepSeek V4 thinking 模型不支持 tool_choice；关闭 thinking，要求纯 JSON 文本
    base = (settings["openai_base_url"] or "").lower()
    if "deepseek" in base:
        kwargs["extra_body"] = {"thinking": {"type": "disabled"}}
    return ChatOpenAI(**kwargs)


def _grammar_catalog() -> str:
    lines: list[str] = []
    for point in list_grammar_points():
        lines.append(
            f"- id={point['id']} | {point['title_zh']} | CEFR {point['cefr']} | "
            f"patterns: {', '.join(point.get('wrong_patterns', [])[:3])}"
        )
    return "\n".join(lines)


def _system_prompt(scene: dict[str, Any], level: str) -> str:
    schema_hint = {
        "reply": "string, in-character English",
        "has_grammar_issue": True,
        "grammar_card": {
            "grammar_point_id": "past_vs_present_perfect",
            "title_zh": "string",
            "cefr": "A2",
            "original": "learner sentence",
            "corrected": "fixed sentence",
            "error_spans": [{"start": 0, "end": 4, "label": "short label"}],
            "rule_zh": "Chinese rule",
            "examples": ["example 1"],
            "severity": "error",
        },
    }
    return f"""You are SyntaxCoach, an English speaking partner with a grammar-teaching side panel.

Scene: {scene.get('title_en')} ({scene.get('title_zh')})
Your role: {scene.get('role')}
Scene goal: {scene.get('description')}
Learner level: {level}

Rules:
1. Stay in character for `reply` — natural English, 1–3 short sentences, push the conversation forward.
2. Analyze ONLY the learner's latest English utterance for grammar/wording.
3. If there is a clear issue, set has_grammar_issue=true and fill grammar_card.
4. If the sentence is fine, set has_grammar_issue=false and grammar_card=null. Do not invent errors.
5. grammar_point_id MUST be one of the allowed ids below when a card is produced.
6. error_spans are character offsets into `original` (half-open [start, end)).
7. Prefer Chinese for rule_zh; keep corrected sentence in English.
8. Never lecture inside `reply`; put teaching into grammar_card.
9. Respond with ONE JSON object only. No markdown fences. No extra text.
   Schema example: {json.dumps(schema_hint, ensure_ascii=False)}

Allowed grammar points:
{_grammar_catalog()}
"""


def _history_messages(history: list[dict[str, str]]) -> list:
    messages = []
    for item in history[-8:]:
        role = item.get("role")
        content = item.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
    return messages


def _extract_json(text: str) -> dict[str, Any]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def llm_turn(state: CoachState) -> dict[str, Any]:
    llm = _build_llm()
    scene = state["scene"]
    messages = [
        SystemMessage(content=_system_prompt(scene, state.get("level") or "B1")),
        *_history_messages(state.get("history") or []),
        HumanMessage(
            content=(
                "Learner just said:\n"
                f"{state['user_text']}\n\n"
                "Return ONE JSON object with reply + optional grammar_card."
            )
        ),
    ]
    raw_msg = llm.invoke(messages)
    content = raw_msg.content if isinstance(raw_msg.content, str) else str(raw_msg.content)
    result = CoachTurn.model_validate(_extract_json(content))

    card: GrammarCard | None = None
    if result.has_grammar_issue and result.grammar_card is not None:
        raw = result.grammar_card
        card = GrammarCard(
            grammar_point_id=raw.grammar_point_id,
            title_zh=raw.title_zh,
            cefr=raw.cefr,
            original=raw.original or state["user_text"],
            corrected=raw.corrected,
            error_spans=[
                ErrorSpan(start=s.start, end=s.end, label=s.label) for s in raw.error_spans
            ],
            rule_zh=raw.rule_zh,
            examples=raw.examples,
            severity=raw.severity,
        )

    return {"reply": result.reply, "grammar_card": card}


def enrich_kb(state: CoachState) -> dict[str, Any]:
    card = state.get("grammar_card")
    if card is None:
        return {}

    point = get_grammar_point(card.grammar_point_id)
    if point is None:
        return {}

    return {
        "grammar_card": GrammarCard(
            grammar_point_id=point["id"],
            title_zh=point.get("title_zh") or card.title_zh,
            cefr=point.get("cefr") or card.cefr,
            original=card.original,
            corrected=card.corrected,
            error_spans=card.error_spans,
            rule_zh=point.get("rule_zh") or card.rule_zh,
            examples=point.get("examples") or card.examples,
            severity=card.severity,
        )
    }


def build_coach_graph():
    graph = StateGraph(CoachState)
    graph.add_node("llm_turn", llm_turn)
    graph.add_node("enrich_kb", enrich_kb)
    graph.add_edge(START, "llm_turn")
    graph.add_edge("llm_turn", "enrich_kb")
    graph.add_edge("enrich_kb", END)
    return graph.compile()


_GRAPH = None


def get_coach_graph():
    global _GRAPH
    if _GRAPH is None:
        _GRAPH = build_coach_graph()
    return _GRAPH


def run_coach_turn(
    *,
    user_text: str,
    scene: dict[str, Any],
    history: list[dict[str, str]],
    level: str,
) -> tuple[str, GrammarCard | None]:
    graph = get_coach_graph()
    result = graph.invoke(
        {
            "user_text": user_text,
            "scene": scene,
            "history": history,
            "level": level,
            "reply": "",
            "grammar_card": None,
        }
    )
    return result["reply"], result.get("grammar_card")
