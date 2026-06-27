---
title: LangGraph orchestrator (agentic)
description: >-
  The LangGraph orchestrator — agentic RAG as a self-correcting StateGraph that
  grades its own retrieval and rewrites the query on a miss.
category: reference
framework: langgraph
tags: [langgraph, agentic-rag, stategraph, orchestrator, rag]
last_updated: 2026-06-27
---

# LangGraph orchestrator (agentic)

## Library

[LangGraph](https://langchain-ai.github.io/langgraph/) — builds stateful,
graph-based agents (nodes + edges over a shared `State`), with branches, loops,
and persistence. Package: `langgraph`.

## Directory structure it touches

| File | Role |
|---|---|
| **`orchestrators/langgraph_orchestrator.py`** | **owned** — the StateGraph + agentic loop |
| `memory/vector_memory.py` | retriever (shared) |
| `services/llm_service.py` | Groq LLM — used for generate **and** grade **and** rewrite (shared) |
| `prompts/prompt_templates.py` | `RAG_PROMPT`, `GRADER_PROMPT`, `REWRITE_PROMPT` (shared) |
| `configs/config.yaml` | `agentic.max_retries` |
| `utils/helpers.py` | `Timing`, `format_docs` (shared) |

## What the RAG application does through it — agentic RAG

Unlike the LCEL chain, the **model controls the flow**. It judges its own
retrieval and self-corrects:

```
START → retrieve → grade ── relevant ──────────────▶ generate → END
                     └────── not relevant & retries ─▶ rewrite → retrieve
```

Nodes (each times itself; the path is recorded in `Timing.trace`):

| Node | What it does |
|---|---|
| `retrieve` | similarity search for the current query |
| `grade` | LLM gives a binary relevance verdict (`with_structured_output(GradeDocuments)`) |
| `rewrite` | LLM rewrites the query for better retrieval; `retries += 1` |
| `generate` | answers from the (relevant) documents |

A **conditional edge** after `grade` routes to `generate` when relevant, else to
`rewrite` (until `agentic.max_retries`, then it answers with what it has). This
loop — grade, rewrite, retry — is exactly what a fixed LCEL pipe cannot express.

## Extending toward more agentic behavior

This is the seed: add tool-calling, multi-source routing, or a `web_search` node
and conditional edges to choose between sources.

## Run

```bash
# Ingest documents from AgenticAI/data/documents/ into Pinecone
uv run AgenticAI/main.py ingest

# Ask a question using the LangGraph orchestrator
uv run AgenticAI/main.py ask "What does LangGraph add on top of LangChain?" --orchestrator langgraph
# the printed `trace:` line shows the path, e.g. retrieve -> grade:relevant -> generate

# Benchmark all orchestrators side by side
uv run AgenticAI/main.py benchmark
```

> Note: the agentic path makes extra LLM calls (grade, and rewrite on a miss),
> so it costs a little more than the LCEL chain — in the benchmark ~120ms for the
> grading step. That's the agentic tradeoff: more calls for self-correction.

Docs: https://langchain-ai.github.io/langgraph/  ·  Agentic RAG tutorial:
https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/
