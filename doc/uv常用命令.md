# uv 怎么用 · Uvicorn 是什么

对应 **T0-8**。本仓库后端：`cd backend && uv sync`。

练习时在独立目录做（如 `doc/exercises/w0/t0-8/`），**不要**在 `backend/` 里乱 `uv add`。

---

## uv 是干什么的

给当前项目单独一份 Python 和包（虚拟环境），避免和别的项目抢版本。

| 前端 | uv |
|------|-----|
| `package.json` | `pyproject.toml` |
| lock 文件 | `uv.lock`（提交 Git） |
| `npm install` | `uv sync` |
| `npm add xxx` | `uv add xxx` |
| `npx` / `npm run` | `uv run ...` |
| `node_modules` | `.venv/` |

---

## 命令（够用这些）

```bash
uv --version          # 有没有装上
uv init               # 新建项目（生成 pyproject.toml、.venv 等）
uv venv               # 只建 .venv，不建项目文件
uv add httpx          # 安装并写入依赖
uv remove httpx       # 卸掉
uv sync               # 按锁文件把环境装齐
uv lock               # 只更新 uv.lock
uv run python main.py # 用这个环境跑
uv export             # 导出成 requirements.txt 风格
```

T0-8 最短路径：

```bash
mkdir -p doc/exercises/w0/t0-8 && cd doc/exercises/w0/t0-8
uv init
uv add httpx
uv run python -c "import httpx; print(httpx.__version__)"
```

跑 SyntaxCoach 后端：

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

`uv run` 会自动用 `.venv`，一般不用先 `source .venv/bin/activate`。

冻结依赖 = 把精确版本记在 **`uv.lock`** 里；别人 `uv sync` 就能装成一样的。  
`pyproject.toml` 只写你直接需要的包；整棵依赖树锁在 lock 里。

---

## Uvicorn 是什么（和 uv 不是一类东西）

**uv** 管「Python 环境和装包」。  
**Uvicorn** 管「把 FastAPI 跑成一个能被浏览器访问的网站」。

没有 Uvicorn，你只有一堆 Python 文件，浏览器打不开 `http://127.0.0.1:8000`。

可以类比：

```text
Vue 代码  →  Vite 开发服务器  →  浏览器打开 :5173
FastAPI   →  Uvicorn 服务器    →  浏览器/前端打开 :8000
```

FastAPI 是「应用」（路由、JSON 怎么返回）。  
Uvicorn 是「服务器」（占端口、收 HTTP、转给 FastAPI）。

这套约定叫 **ASGI**：异步 Python Web 应用和服务器之间的接口。FastAPI 按它写，Uvicorn 按它跑。同类还有 Hypercorn 等，本仓库用 Uvicorn。

### 这句命令在干什么

```bash
uv run uvicorn app.main:app --reload --port 8000
```

| 片段 | 含义 |
|------|------|
| `uv run` | 用 backend 的 `.venv` 执行后面的程序 |
| `uvicorn` | 启动这个 Web 服务器（包已写在 `backend/pyproject.toml`） |
| `app.main:app` | 模块 `app/main.py` 里的变量 `app`（那个 `FastAPI()` 实例） |
| `--reload` | 改代码自动重启，只适合开发 |
| `--port 8000` | 监听 8000 端口 |

`app.main:app` 读法：`文件路径.模块 : 对象名`，中间是冒号，不是斜杠。

启动成功后：

- 接口：http://127.0.0.1:8000/api/health
- 文档：http://127.0.0.1:8000/docs

关掉终端或 Ctrl+C 就停服。

---

## 别混的三件事

| 名字 | 角色 |
|------|------|
| **uv** | 装包、建 `.venv`、`uv run` |
| **Uvicorn** | 跑 FastAPI 的 HTTP 服务器 |
| **FastAPI** | 你写的 API 应用 |

所以：`uv run` 只是「用对的环境去启动」；真正听端口的是 **uvicorn**。

---

## 不用 uv 时（了解即可）

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install httpx
pip freeze > requirements.txt
```

本仓库标准流程仍是 uv。

---

## T0-8 勾选

- 独立目录有 `pyproject.toml` + `.venv`
- `uv add httpx` 成功（不要写进 `backend/pyproject.toml`）
- 知道 `uv sync` ≈ npm install，`uv.lock` = 冻结依赖

下一步 **T0-9**：在该环境里请求 `https://httpbin.org/get`，打印 status code 和 JSON 某个字段。
