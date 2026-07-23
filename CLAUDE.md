---
title: CLAUDE.md — Python Workspace
description: Project-level instructions and context for Claude Code in this Python monorepo
version: 1.0.0
author: Nikhil Pagote
date: 2026-06-22
tags: [claude-code, workspace, devcontainer, podman, zed, python, uv]
status: active
---

# CLAUDE.md — Python Workspace

## Environment

- **Editor**: Zed
- **Container runtime**: Podman (rootless)
- **Devcontainer name**: `python_devcontainer-devcontainer-1`
- **Package manager**: `uv` (see `uv-cheatsheet.md` for reference)
- **Linter/formatter**: `ruff`

## Devcontainer

This workspace runs inside a devcontainer. Zed opens it natively — select **"Open in Container"** when prompted.

To rebuild after config changes:
```bash
podman kill python_devcontainer-devcontainer-1
# Then reopen the project in Zed
```

See `devcontainer-podman-zed.md` for the full setup guide.
Use `/devcontainer` skill to scaffold devcontainer config in a new project.

## Port Mappings (host → container)

| Host | Container | Service |
|------|-----------|---------|
| 8000 | 8000      | FastAPI |
| 8080 | 8080      | —       |
| 5001 | 5000      | Flask   |

## Projects

### `my-fapi` — FastAPI app

- Layout: `src/my_fapi/app.py`
- Run: `uv run uvicorn my_fapi:app --app-dir src --host 0.0.0.0 --port 8000`
- Access: `http://localhost:8000`

### `my_flask` — Flask app

- Run from `/workspace/my_flask`

### `notebooks/` — Jupyter notebooks

- Data lives in `notebooks/data/`
- Run: `uv run jupyter notebook`

### `AgenticAI/` — Agentic RAG (multi-orchestrator)

- Modular agentic structure; same RAG core driven by swappable orchestrators (LangChain, LangGraph; CrewAI/Google ADK as extension points)
- Stack: Groq `llama-3.1-8b-instant` + Pinecone (hosted embeddings + vector DB)
- Entry: `uv run AgenticAI/main.py {ingest|ask --orchestrator|benchmark}`
- Backend: `AgenticAI/backend/` · UI: `AgenticAI/streamlit/` · Docs: `AgenticAI/README.md`, `AgenticAI/docs/`
- (formerly `RAG/`)

### `Claude_MVP/` — Shopping cart RAG project

- Python app: `Claude_MVP/python/`
- See `Claude_MVP/shopping_cart_rag_plan.md` for context

### `PyO3/` — PyO3 learning examples

- Standalone maturin projects under `PyO3/examples/` (Rust ↔ Python bindings)
- Build inside the devcontainer: `cd PyO3/examples/<name> && maturin develop`
- Docs: `PyO3/README.md`, `PyO3/docs/`

## Known Issues

- Old uvicorn processes bind to `localhost` instead of `0.0.0.0`, blocking host access. Find and kill with:
  ```bash
  lsof -i :8000
  kill <PID>
  ```
- Git author may default to wrong identity inside the container. Fix:
  ```bash
  git config --global user.name "Nikhil"
  git config --global user.email "nikhil.pagote@gmail.com"
  ```

## Available Skills

- `/devcontainer` — scaffold `.devcontainer/` config with Podman support for a project
