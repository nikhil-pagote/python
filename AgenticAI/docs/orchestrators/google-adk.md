---
title: Google ADK orchestrator (planned)
description: >-
  Extension point for a Google Agent Development Kit orchestrator over the shared
  RAG core.
category: reference
framework: google-adk
tags: [google-adk, orchestrator, rag, extension-point]
last_updated: 2026-06-27
---

# Google ADK orchestrator (planned)

## Library

[Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) — an
open-source framework for building agents with tools and workflows. Package:
`google-adk`.

## Directory structure it touches

| File | Role |
|---|---|
| **`orchestrators/google_adk_orchestrator.py`** | **owned** — currently a stub raising `NotImplementedError` |
| `memory/vector_memory.py` | retrieval (reuse for parity) |
| `services/llm_service.py` | LLM (reuse for parity) |
| `prompts/prompt_templates.py` | prompts (reuse) |

## What the RAG application would do through it

Build an ADK agent that uses retrieval as a tool, to compare Google's ADK against
the LangChain, LangGraph, and CrewAI orchestrators on the identical RAG task.

## How to implement

1. `uv add google-adk` (then uncomment it in `requirements.txt`).
2. In `orchestrators/google_adk_orchestrator.py`, implement `answer(question) -> Timing`:
   define an ADK agent + a retrieval tool backed by `VectorMemory`, run it, and
   return a `Timing`.
3. Register it in `main.py` (`_orchestrator`) and `scripts/benchmark.py`.

## Run

> Not yet implemented — `google_adk_orchestrator.py` raises `NotImplementedError`.
> Once implemented, the commands will be:

```bash
# Ingest documents from AgenticAI/data/documents/ into Pinecone
uv run AgenticAI/main.py ingest

# Ask a question using the Google ADK orchestrator
uv run AgenticAI/main.py ask "What is Pinecone used for?" --orchestrator google_adk

# Benchmark all orchestrators side by side
uv run AgenticAI/main.py benchmark
```

Docs: https://google.github.io/adk-docs/
