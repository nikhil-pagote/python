---
title: Agentic RAG — Multi-Orchestrator
description: >-
  A RAG application laid out as an agentic project: a shared Groq + Pinecone core
  driven by swappable orchestrators (LangChain and LangGraph today; CrewAI and
  Google ADK as extension points), with a timed benchmark.
category: reference
stack:
  reasoning_model: groq/llama-3.1-8b-instant
  embeddings_model: pinecone/llama-text-embed-v2
  vector_db: pinecone (serverless)
  frameworks:
    - langchain
    - langgraph
  planned:
    - crewai
    - google-adk
tags:
  - rag
  - agentic
  - orchestrators
  - langchain
  - langgraph
  - groq
  - pinecone
last_updated: 2026-06-27
---

# Agentic RAG — Multi-Orchestrator

A retrieval-augmented-generation app organized with an **agentic project
structure**, so the same retrieve → generate task can be driven by **swappable
orchestrators** and compared head-to-head. The RAG core (ingestion, embeddings,
vector memory, retrieval, prompt, LLM) is shared; each orchestrator only differs
in *how* it coordinates that core.

- **Reasoning:** Groq `llama-3.1-8b-instant` (`services/llm_service.py`)
- **Embeddings:** Pinecone hosted `llama-text-embed-v2`, 1024-dim (`services/embedding_service.py`)
- **Vector DB / memory:** Pinecone serverless (`services/vector_store_service.py`, `memory/vector_memory.py`)

## Orchestrators (`orchestrators/`)

| Orchestrator | Status | Doc |
|---|---|---|
| LangChain (LCEL chain) | ✅ working — fixed retrieve→generate | [docs/orchestrators/langchain.md](docs/orchestrators/langchain.md) |
| LangGraph (agentic) | ✅ working — **doc-grading + query-rewrite loop** | [docs/orchestrators/langgraph.md](docs/orchestrators/langgraph.md) |
| CrewAI | 🧩 stub — extension point | [docs/orchestrators/crewai.md](docs/orchestrators/crewai.md) |
| Google ADK | 🧩 stub — extension point | [docs/orchestrators/google-adk.md](docs/orchestrators/google-adk.md) |

All implement the same `BaseOrchestrator.answer()` contract, so adding a new
framework is one new file — drop it in `orchestrators/`, reuse the shared
`services/` and `memory/`, and it's instantly comparable in the benchmark. The
LangGraph orchestrator is **agentic**: it grades its own retrieval and rewrites
the query on a weak result (see its doc).

## Documentation

| Doc | What's in it |
|-----|--------------|
| **[docs/architecture.md](docs/architecture.md)** | The agentic layout, RAG-vs-agentic explained, the orchestrator contract, extension points, and the LangChain-vs-LangGraph comparison |
| **[docs/orchestrators/](docs/orchestrators/README.md)** | **Per-library docs** — one per orchestrator (LangChain, LangGraph, CrewAI, Google ADK): the library, the files it touches, and what the RAG app does through it |
| **[docs/setup.md](docs/setup.md)** | Full directory tree, dependencies, secrets, building the index, run commands |
| [configs/config.yaml](configs/config.yaml) | All tunables (models, index, chunking, k) — config separate from code |

> **Known issue (this env):** Python 3.14.6 makes the `groq` SDK ~24s/call
> (the API itself is fast — verified via curl). Pin Python to 3.12/3.13 for
> normal speed. See the bottom of this file.

## Quick start

```bash
cp .env.example .env                 # set GROQ_API_KEY and PINECONE_API_KEY
uv sync                              # install deps
uv run AgenticAI/main.py ingest            # build vector memory (once)
uv run AgenticAI/main.py ask "What does LangGraph add on top of LangChain?" --orchestrator langgraph
uv run AgenticAI/main.py benchmark         # time all orchestrators
```

See **[docs/setup.md](docs/setup.md)** for the full guide and
**[docs/architecture.md](docs/architecture.md)** for the design and how to add a
CrewAI or Google ADK orchestrator.
