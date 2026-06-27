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

## Code walkthrough

### Pipeline in one line

```
question → retriever.invoke() → format_docs() → RAG_PROMPT | get_llm() → answer
```

### Step 1 — `__init__`: wire up the two halves

```python
self.retriever = VectorMemory().as_retriever()
self.generate = RAG_PROMPT | get_llm()
```

Two objects built at startup, reused per question:

- `self.retriever` — a LangChain `VectorStoreRetriever` backed by Pinecone; `as_retriever()` wraps `similarity_search()` with `k` from config.
- `self.generate` — an LCEL chain: `|` fuses `RAG_PROMPT` and `ChatGroq` into one `Runnable`. Calling `.invoke({context, question})` runs both in sequence.

### Step 2 — retrieval (timed)

```python
t0 = ms()
docs = self.retriever.invoke(question)
t1 = ms()
```

Hits Pinecone, returns the top-k `Document` objects. Timed independently so the benchmark separates retrieval latency from generation latency.

### Step 3 — generation (timed)

```python
message = self.generate.invoke(
    {"context": format_docs(docs), "question": question}
)
t2 = ms()
```

- `format_docs(docs)` joins `doc.page_content` with newlines into one string.
- `self.generate.invoke(...)` fills the prompt template then calls Groq. Returns an `AIMessage`.
- `RAG_PROMPT` injects a system message ("answer using only the context") and a human message with `{context}` and `{question}`.

### Step 4 — return a `Timing`

```python
return Timing(
    question=question,
    answer=message.content,
    retrieval_ms=round(t1 - t0, 1),
    generation_ms=round(t2 - t1, 1),
    total_ms=round(t2 - t0, 1),
    output_tokens=output_tokens(message),
)
```

`Timing` is a shared dataclass — every orchestrator returns the same shape so the benchmark can compare them fairly. `trace` is left blank (no agentic path to record).

### Supporting pieces

| Piece | What it does |
|---|---|
| `get_llm()` | Returns a `ChatGroq` instance with an IPv4-only httpx client (avoids a 24s IPv6 stall on this machine) |
| `VectorMemory.as_retriever()` | Wraps Pinecone's `similarity_search` as a LangChain `Retriever` |
| `RAG_PROMPT` | System + human message template; shared with LangGraph |
| `ms()` | `perf_counter * 1000` — millisecond timestamps |

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
