"""
统一响应信封 ≈ 前端 Axios 拦截器约定的 { code, data, errorMsg }。

成功：code === 0，业务在 data，errorMsg 为 null
失败：code 为 HTTP 状态数字（400/404/422/500…），data 为 null，说明在 errorMsg
前端只看 code === 0，再取 data。
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

SUCCESS_CODE = 0


class ApiEnvelope(BaseModel):
    code: int = Field(..., description="成功为 0；失败为 HTTP 状态码数字")
    data: Any | None = Field(None, description="成功时的业务数据；失败为 null")
    errorMsg: str | None = Field(None, description="失败时的说明；成功为 null")

    @classmethod
    def ok(cls, data: Any = None) -> ApiEnvelope:
        return cls(code=SUCCESS_CODE, data=data, errorMsg=None)

    @classmethod
    def fail(cls, code: int, error_msg: str) -> ApiEnvelope:
        return cls(code=code, data=None, errorMsg=error_msg)
