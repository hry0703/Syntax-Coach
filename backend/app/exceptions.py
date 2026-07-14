"""
业务异常：raise AppError("说明", status_code=400)
→ 信封 code 直接用 status_code 数字。
"""

from __future__ import annotations


class AppError(Exception):
    def __init__(self, detail: str, *, status_code: int = 400) -> None:
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
