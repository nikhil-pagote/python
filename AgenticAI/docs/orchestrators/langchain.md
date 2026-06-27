---
title: LangChain orchestrator (LCEL)
description: >-
  The LangChain (LCEL) orchestrator — a fixed retrieve→generate pipeline composed
  with the pipe operator over the shared RAG core.
category: reference
framework: langchain
tags: [langchain, lcel, orchestrator, rag]
last_updated: 2026-06-27
---

# LangChain orchestrator (LCEL)

## Library

[LangChain](https://python.langchain.com/) — LCEL (LangChain Expression Language)
composes Runnables with the pipe operator `|`. Packages: `langchain-core`,
`langchain-groq`, `langchain-pinecone`.

## Directory structure it touches

| File | Role |
|---|---|
| **`orchestrators/langchain_orchestrator.py`** | **owned** — the LCEL composition |
| `memory/vector_memory.py` | retriever (shared) |
| `services/llm_service.py` | Groq LLM (shared) |
| `prompts/prompt_templates.py` | `RAG_PROMPT` (shared) |
| `utils/helpers.py` | `Timing`, `format_docs` (shared) |

## What the RAG application does through it

A **fixed pipeline** — the code controls the flow, the LLM is called once:

```
question → retriever → format_docs → RAG_PROMPT → ChatGroq → answer
```

In code, the generation half is one expression: `RAG_PROMPT | get_llm()`. The
fully fused form would also pipe the retriever and a `StrOutputParser`. There is
no branching or looping — every question takes the same path.

## When to use it

Linear, predictable RAG. Lowest overhead, easiest to read. Cannot grade its own
retrieval or retry — for that, see the [LangGraph orchestrator](langgraph.md).

## Run

```bash
# Ingest documents from AgenticAI/data/documents/ into Pinecone
uv run AgenticAI/main.py ingest

# Ask a question using the LangChain orchestrator
uv run AgenticAI/main.py ask "What is Pinecone used for?" --orchestrator langchain

# Benchmark all orchestrators side by side
uv run AgenticAI/main.py benchmark
```

Docs: https://python.langchain.com/docs/concepts/lcel/
