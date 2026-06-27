---
title: Setup & Run — Agentic RAG
description: >-
  Directory tree, dependencies, secrets, index build, and run commands for the
  multi-orchestrator agentic RAG project (Groq + Pinecone).
category: setup
tags:
  - rag
  - agentic
  - setup
  - pinecone
  - groq
  - uv
last_updated: 2026-06-27
---

# Setup & Run

## Project structure

```
AgenticAI/
├── main.py                  entry point: ingest | ask --orchestrator | benchmark
├── requirements.txt         pinned deps (uv/pyproject is source of truth)
├── .env / .env.example      secrets (gitignored) / template
├── agents/                  agent definitions
│   ├── base_agent.py        common agent interface
│   └── rag_agent.py         wraps an orchestrator (real)
├── protocols/               agent communication (MCP/A2A) — extension point
│   └── base_protocol.py
├── tools/                   tools an agent can call
│   ├── base_tool.py
│   └── retrieval_tool.py    retrieval-as-a-tool (RAG→agent bridge, real)
├── memory/                  memory management
│   ├── base_memory.py
│   └── vector_memory.py     Pinecone-backed RAG memory (real)
├── ingestion/               load + chunk the corpus (real)
│   ├── loader.py            read data/documents/
│   └── chunker.py           RecursiveCharacterTextSplitter
├── workflows/               multi-agent sequencing — extension point
│   └── base_workflow.py
├── orchestrators/           coordination layer — the swap point
│   ├── base_orchestrator.py     shared contract
│   ├── langchain_orchestrator.py   ✅ LCEL chain
│   ├── langgraph_orchestrator.py   ✅ agentic StateGraph (grade + rewrite loop)
│   ├── crewai_orchestrator.py      🧩 stub
│   └── google_adk_orchestrator.py  🧩 stub
├── services/                external service wrappers
│   ├── llm_service.py           Groq
│   ├── embedding_service.py     Pinecone embeddings
│   └── vector_store_service.py  Pinecone index/store
├── prompts/prompt_templates.py  the RAG prompt
├── configs/                 config separate from code
│   ├── config.yaml          models, index, chunking, k, benchmark queries
│   └── __init__.py          config() + secret() loader
├── utils/helpers.py         Timing, logging, formatters
├── scripts/benchmark.py     time all orchestrators
├── tests/test_app.py        structure/config tests (no network)
├── data/documents/          source corpus (.md/.txt) — ingestion reads these
├── docs/                    architecture.md + setup.md (this file) + reference images
└── logs/                    app.log (gitignored)
```

Everything except `orchestrators/` (and the agent-layer extension points) is the
**shared core**. Config is separate from code (`configs/config.yaml`), secrets are
separate from both (`.env`), and ingestion is separate from serving.

## 1. Secrets

```bash
cp .env.example .env
```

| Variable | Purpose | Get one at |
|----------|---------|------------|
| `GROQ_API_KEY` | reasoning model (llama-3.1-8b-instant) | https://console.groq.com/keys |
| `PINECONE_API_KEY` | vector DB **and** hosted embeddings | https://app.pinecone.io |
| `PINECONE_INDEX` | optional, defaults to `rag-examples` | — |

## 2. Dependencies

```bash
uv sync                          # or: pip install -r requirements.txt
```

CrewAI / Google ADK are not installed — they're optional, for when you implement
those orchestrators (see `requirements.txt`).

## 3. Build the index (once)

Creates the Pinecone serverless index automatically:

```bash
uv run AgenticAI/main.py ingest
```

## Run

```bash
# Ask one question with a chosen orchestrator
uv run AgenticAI/main.py ask "What does LangGraph add on top of LangChain?" --orchestrator langchain
uv run AgenticAI/main.py ask "What is Pinecone used for?"                    --orchestrator langgraph

# Time all orchestrators side by side
uv run AgenticAI/main.py benchmark        # (or: uv run AgenticAI/scripts/benchmark.py)

# Structure tests (no network, no keys)
uv run pytest AgenticAI/tests
```

## Configuration

All tunables live in [`configs/config.yaml`](../configs/config.yaml). Change
behavior there, not in code.

See [architecture.md](architecture.md) for the design, the orchestrator contract,
and how to add a CrewAI or Google ADK orchestrator.
