from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

# 缓存配置，避免重复读取环境变量
@lru_cache(maxsize=1)
def get_settings() -> dict[str, str | None]:
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1",
        "openai_model": os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
    }


def llm_configured() -> bool:
    key = get_settings()["openai_api_key"]
    return bool(key and key != "your_api_key" and not key.startswith("your_"))
