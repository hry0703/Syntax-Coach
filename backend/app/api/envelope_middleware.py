"""
成功响应包装中间件：把业务 JSON 包成 { code: 0, data, errorMsg: null }。
"""

from __future__ import annotations

import json
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.schemas.errors import ApiEnvelope

# Swagger / OpenAPI 原样返回，不要包信封
_SKIP_PREFIXES = ("/docs", "/redoc", "/openapi.json", "/favicon.ico")


def _already_enveloped(payload: object) -> bool:
    return (
        isinstance(payload, dict)
        and "code" in payload
        and "data" in payload
        and "errorMsg" in payload
    )


class ResponseEnvelopeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        if any(path == p or path.startswith(p + "/") for p in _SKIP_PREFIXES):
            return await call_next(request)

        response = await call_next(request)

        content_type = response.headers.get("content-type", "")
        if "application/json" not in content_type:
            return response

        body = b""
        async for chunk in response.body_iterator:
            body += chunk if isinstance(chunk, bytes) else chunk.encode()

        try:
            payload = json.loads(body.decode() or "null")
        except json.JSONDecodeError:
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        if _already_enveloped(payload):
            return JSONResponse(status_code=response.status_code, content=payload)

        # 仅包装成功态；4xx/5xx 若未信封（少见）也收成 fail
        if 200 <= response.status_code < 300:
            enveloped = ApiEnvelope.ok(payload).model_dump()
            return JSONResponse(status_code=response.status_code, content=enveloped)

        msg = None
        if isinstance(payload, dict):
            raw_code = payload.get("code")
            msg = payload.get("errorMsg") or payload.get("detail")
            code = raw_code if isinstance(raw_code, int) else response.status_code
        else:
            code = response.status_code
        enveloped = ApiEnvelope.fail(code, str(msg or "request failed")).model_dump()
        return JSONResponse(status_code=response.status_code, content=enveloped)
