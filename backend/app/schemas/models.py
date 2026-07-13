"""
领域模型（Pydantic）≈ TypeScript interface + 运行时校验。

FastAPI 路由直接用这些模型做请求/响应；
Agent 内部也用同一套（尤其 GrammarCard）。
前端类型：frontend/src/types/index.ts —— 改字段三处对齐。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ErrorSpan(BaseModel):
    """原句中需要高亮的错误区间（字符下标，左闭右开）。"""

    start: int = Field(..., description="错误起点下标（含），相对 original 字符串", ge=0, examples=[2])
    end: int = Field(..., description="错误终点下标（不含）", ge=0, examples=[6])
    label: str = Field(..., description="高亮标签，如时态 / 介词 / 冠词", examples=["时态"])


class GrammarCard(BaseModel):
    """对话回合产出的结构化语法卡片（产品核心输出）。"""

    grammar_point_id: str = Field(
        ...,
        description="关联知识库语法点 id，用于错题归档与复习",
        examples=["past_vs_present_perfect"],
    )
    title_zh: str = Field(..., description="语法点中文标题", examples=["一般过去时 vs 现在完成时"])
    cefr: str = Field(..., description="CEFR 级别，如 A2 / B1 / B2", examples=["B1"])
    original: str = Field(..., description="用户原句（含错误）", examples=["I have went there yesterday."])
    corrected: str = Field(..., description="改写后的正确句子", examples=["I went there yesterday."])
    error_spans: list[ErrorSpan] = Field(
        default_factory=list,
        description="原句中需高亮的错误跨度列表",
    )
    rule_zh: str = Field(..., description="中文规则讲解（宜短、可操作）")
    examples: list[str] = Field(default_factory=list, description="正确用法例句")
    severity: Literal["error", "suggestion"] = Field(
        "error",
        description="error=明确错误；suggestion=可接受但有更好说法",
    )


class Scene(BaseModel):
    """口语陪练场景（角色 + 情境）。"""

    id: str = Field(..., description="场景唯一 id", examples=["coffee_shop"])
    title_zh: str = Field(..., description="场景中文名", examples=["咖啡店点单"])
    title_en: str = Field(..., description="场景英文名", examples=["Coffee Shop Ordering"])
    role: str = Field(..., description="AI 扮演的角色", examples=["barista"])
    level: str = Field(..., description="建议难度级别", examples=["A2-B1"])
    description: str = Field(..., description="场景简介，用于选场展示")


class GrammarPoint(BaseModel):
    """本地知识库中的语法点卡片。"""

    id: str = Field(..., description="语法点唯一 id", examples=["past_vs_present_perfect"])
    title_zh: str = Field(..., description="中文标题")
    cefr: str = Field(..., description="CEFR 级别", examples=["B1"])
    category: str = Field(..., description="分类，如 tense / article / preposition", examples=["tense"])
    rule_zh: str = Field(..., description="稳定规则说明（Agent 会优先用 KB 覆盖）")
    wrong_patterns: list[str] = Field(default_factory=list, description="常见错误模式示例")
    examples: list[str] = Field(default_factory=list, description="正确例句")
    contrast: str | None = Field(None, description="易混淆对比说明，可选")


class CreateSessionRequest(BaseModel):
    """创建对话会话的请求体。"""

    scene_id: str = Field(..., description="要进入的场景 id", examples=["coffee_shop"])
    level: str | None = Field(
        None,
        description="可选覆盖用户默认难度；不传则用 profile.level",
        examples=["B1"],
    )


class CreateSessionResponse(BaseModel):
    """新建会话的返回。"""

    session_id: str = Field(..., description="会话 id，后续发消息时使用")
    scene_id: str = Field(..., description="已绑定的场景 id")
    status: Literal["active"] = Field("active", description="会话状态，目前固定为 active")


class ChatMessageRequest(BaseModel):
    """用户在会话中发送的一条消息。"""

    content: str = Field(..., description="用户英文口语输入（文本）", min_length=1, examples=["I want a coffee."])


class ChatMessageResponse(BaseModel):
    """Agent 回合响应：角色回复 + 可选语法卡片。"""

    reply: str = Field(..., description="场景角色的英文回复")
    grammar_card: GrammarCard | None = Field(
        None,
        description="若本轮检出语法问题则返回卡片；无明显问题可为 null",
    )
    turn: int = Field(1, description="当前回合序号（从 1 起）", ge=1)


class MistakeCreate(BaseModel):
    """将一条语法问题加入错题本。"""

    grammar_point_id: str = Field(..., description="语法点 id（归档维度）")
    original: str = Field(..., description="错误原句")
    corrected: str = Field(..., description="正确句子")
    scene_id: str | None = Field(None, description="来源场景 id，可选")
    rule_zh: str | None = Field(None, description="规则摘要快照，可选")


class Mistake(BaseModel):
    """错题本条目（按 grammar_point_id 沉淀，非纯聊天记录）。"""

    id: str = Field(..., description="错题记录 id")
    grammar_point_id: str = Field(..., description="关联语法点")
    original: str = Field(..., description="错误原句")
    corrected: str = Field(..., description="正确句子")
    scene_id: str | None = Field(None, description="来源场景")
    rule_zh: str | None = Field(None, description="规则摘要")
    mastered: bool = Field(False, description="是否已掌握（复习通过后可标记）")


class MistakePatch(BaseModel):
    """局部更新错题（目前仅支持掌握状态）。"""

    mastered: bool | None = Field(None, description="设为 true 表示已掌握；不传则不改")


class ReviewItem(BaseModel):
    """今日复习中的一道题。"""

    id: str = Field(..., description="题目 id")
    type: Literal["correct_error", "make_sentence"] = Field(
        ...,
        description="题型：改错 / 造句",
    )
    prompt: str = Field(..., description="题干文案")
    grammar_point_id: str = Field(..., description="考查的语法点 id")


class ReviewSubmit(BaseModel):
    """提交一道复习题的答案。"""

    item_id: str = Field(..., description="题目 id")
    answer: str = Field(..., description="用户作答文本")


class ReviewFeedback(BaseModel):
    """复习题即时反馈。"""

    correct: bool = Field(..., description="是否答对")
    feedback: str = Field(..., description="简短中文点评")


class UserProfile(BaseModel):
    """用户偏好：难度、目标、纠错与讲解强度。"""

    level: Literal["A2", "B1", "B2"] = Field("B1", description="当前目标难度")
    goal: Literal["speaking", "business", "exam"] = Field(
        "speaking",
        description="学习目标：口语 / 商务 / 考试",
    )
    correction_strictness: Literal["light", "standard", "strict"] = Field(
        "standard",
        description="纠错严格度：轻 / 标准 / 严",
    )
    explanation_detail: Literal["brief", "standard", "detailed"] = Field(
        "standard",
        description="规则讲解详略",
    )
    show_terms: bool = Field(False, description="是否在卡片中展示语法术语")


class HealthResponse(BaseModel):
    """健康检查响应。"""

    status: str = Field("ok", description="服务状态，正常为 ok")
