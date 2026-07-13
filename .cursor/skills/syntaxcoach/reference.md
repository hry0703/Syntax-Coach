# SyntaxCoach reference

## GrammarCard (API)

```json
{
  "grammar_point_id": "past_vs_present_perfect",
  "title_zh": "现在完成时 vs 一般过去时",
  "cefr": "A2",
  "original": "I have went here yesterday, so medium is fine.",
  "corrected": "I went here yesterday, so medium is fine.",
  "error_spans": [
    { "start": 2, "end": 11, "label": "have + V-ed / 过去式冲突" }
  ],
  "rule_zh": "……中文规则说明……",
  "examples": [
    "I went to this café yesterday.",
    "I have been here before."
  ],
  "severity": "error"
}
```

- `error_spans.start` / `end`：相对 `original` 的 Unicode 下标（半开区间 `[start, end)`）。
- `severity`：`error` | `suggestion`。

## Grammar point KB file

Path: `backend/data/grammar_points/<id>.json`

```json
{
  "id": "articles_a_an_the",
  "title_zh": "冠词 a / an / the",
  "cefr": "A2",
  "category": "冠词",
  "rule_zh": "……",
  "wrong_patterns": ["I want latte", "an university"],
  "examples": ["I want a latte, please."],
  "contrast": "a/an = 某一个；the = 那个已知的"
}
```

`id` 必须与文件名（不含 `.json`）及卡片里的 `grammar_point_id` 一致。

## Key HTTP routes

| Method | Path | Notes |
|--------|------|-------|
| GET | `/api/health` | |
| GET | `/api/scenes` | `data/scenes.json` |
| POST | `/api/chat/sessions` | `{ scene_id, level? }` |
| POST | `/api/chat/sessions/{id}/messages` | `{ content }` → reply + grammar_card |
| GET | `/api/grammar-points` | list KB |
| GET | `/api/grammar-points/{id}` | one point |
| GET/POST/PATCH | `/api/mistakes` | in-memory stub |
| GET/POST | `/api/review/today`, `/submit` | stub |
| GET/PATCH | `/api/profile` | in-memory stub |

## Priority grammar points (MVP set)

1. `past_vs_present_perfect`
2. `articles_a_an_the`
3. `prepositions_in_on_at`
4. `subject_verb_agreement`
5. `countable_uncountable`

扩展时优先中国学习者高频点；每个点保持短 `rule_zh` + 2–3 例句即可。

## Dev commands

```bash
# Node 22
nvm use

# backend
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

# frontend
cd frontend && npm run dev
```

## Design tokens (summary)

- `--teal: #0f6b5c` / `--teal-deep: #0a4f44` / `--paper: #f3f6f4`
- Error / OK：`--error` / `--ok` 及对应 soft 背景
- 双栏：`.workspace` → chat | panel；卡片：`.card`
