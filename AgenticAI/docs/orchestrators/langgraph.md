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

## Code walkthrough

### Pipeline in one line

```
question → retrieve → grade → (relevant?) generate → END
                         └── (not relevant) rewrite → retrieve → ...
```

### Step 1 — `__init__`: build the three chains

```python
grader   = GRADER_PROMPT  | llm.with_structured_output(GradeDocuments)
rewriter = REWRITE_PROMPT | llm | StrOutputParser()
generator = RAG_PROMPT    | llm
```

Three LCEL chains, each built once at startup:

- `grader` — calls the LLM with `with_structured_output(GradeDocuments)` so the response is always a `GradeDocuments(relevant: bool)` — no string parsing needed.
- `rewriter` — rewrites a weak query; `StrOutputParser()` strips the `AIMessage` wrapper to return a plain string.
- `generator` — same `RAG_PROMPT | llm` as the LangChain orchestrator.

### Step 2 — `State`: the shared scratchpad

```python
class State(TypedDict):
    question: str   # original question, never mutated
    query: str      # current search query (rewritten on a miss)
    documents: list
    relevant: bool
    answer: str
    retries: int
    retrieval_ms / grading_ms / rewrite_ms / generation_ms: float
    trace: list
```

Every node receives the full `State` and returns only the keys it updates — LangGraph merges the returned dict back in. `question` stays fixed; `query` is the one that gets rewritten.

### Step 3 — four node functions

Each node times itself and appends to `trace`:

| Node | Key logic |
|---|---|
| `retrieve` | `retriever.invoke(state["query"])` — uses `query`, not `question` |
| `grade` | `grader.invoke({context, question})` → `verdict.relevant` bool; accumulates `grading_ms` |
| `rewrite` | `rewriter.invoke({question: state["query"]})` → new query string; `retries += 1` |
| `generate` | `generator.invoke({context, question})` → `message.content`; records `output_tokens` |

Note: `retrieve` and `grade` accumulate their ms counters (`+= `) because they may run more than once per question in the retry loop.

### Step 4 — `decide`: the conditional edge

```python
def decide(state: State) -> str:
    if state["relevant"]:
        return "generate"
    if state["retries"] < self.max_retries:
        return "rewrite"
    return "generate"  # give up; answer with what we have
```

This is what makes it agentic — the graph branches based on the LLM's own verdict. A fixed LCEL chain has no equivalent.

### Step 5 — build and compile the graph

```python
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")
builder.add_conditional_edges("grade", decide, {"generate": "generate", "rewrite": "rewrite"})
builder.add_edge("rewrite", "retrieve")
builder.add_edge("generate", END)
self.graph = builder.compile()
```

The `rewrite → retrieve` edge is what creates the loop. `compile()` validates the graph and returns a `Runnable`.

### Step 6 — `answer()`: run the graph, return `Timing`

```python
final = self.graph.invoke(
    {"question": question, "query": question, "retries": 0, "trace": []}
)
return Timing(..., trace=" -> ".join(final.get("trace", [])))
```

`graph.invoke()` runs the full state machine and returns the final `State` dict. `trace` is joined to a readable string like `retrieve -> grade:relevant -> generate`.

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
