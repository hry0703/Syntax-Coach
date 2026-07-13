from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
GRAMMAR_DIR = DATA_DIR / "grammar_points"
SCENES_PATH = DATA_DIR / "scenes.json"


@lru_cache(maxsize=1)
def load_scenes() -> list[dict[str, Any]]:
    with SCENES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_all_grammar_points() -> dict[str, dict[str, Any]]:
    points: dict[str, dict[str, Any]] = {}
    for path in sorted(GRAMMAR_DIR.glob("*.json")):
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        points[data["id"]] = data
    return points


def get_grammar_point(point_id: str) -> dict[str, Any] | None:
    return load_all_grammar_points().get(point_id)


def list_grammar_points() -> list[dict[str, Any]]:
    return list(load_all_grammar_points().values())
