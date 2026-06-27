---
title: Architecture — Agentic RAG (Multi-Orchestrator)
description: >-
  The agentic project layout, RAG vs agentic explained, the swappable
  orchestrator contract, extension points (CrewAI, Google ADK), and the
  LangChain-vs-LangGraph comparison.
category: design
framework:
  - langchain
  - langgraph
tags:
  - rag
  - agentic
  - orchestrators
  - architecture
last_updated: 2026-06-27
---

# Architecture

## RAG vs agentic — the distinction this layout is built on

The difference is **who controls the flow**:

- **RAG** is a *fixed pipeline*: your code always runs `retrieve → prompt →
  generate`. The LLM is called at one fixed spot; it does not decide what to do.
- **Agentic** is *model-driven*: the LLM is given tools and a goal and decides,
  in a loop, what to do next — when to retrieve, whether the result is good
  enough, when to retry, when it's done.

> Test: is the sequence of steps fixed in code (RAG) or decided by the model at
> runtime (agentic)?

Plain RAG is **not** agentic — but it's the core an agent uses. That's why this
project uses an agentic structure with RAG as the shared core: today the
orchestrators run a fixed `retrieve → generate`; the structure leaves room to
make them agentic (tool-calling, doc-grading loops) as you grow.

## The layout

Organized by **agent faculty** (the agentic convention), with the RAG pipeline
living inside it as the shared core:

```
shared core (used by every orchestrator)
  ingestion/  →  services/embedding_service  →  services/vector_store_service
   (load+chunk)        (embed)                      (Pinecone index)
                                                        │
                            memory/vector_memory  ◀─────┘   ("RAG embeddings")
                                   │
   services/llm_service · prompts/prompt_templates · utils/helpers
                                   │
        ┌──────────────────────────┴──────────────────────────┐
   orchestrators/  (the swap point — all share BaseOrchestrator)
   langchain · langgraph · crewai* · google_adk*      (*extension stubs)
        │
   agents/rag_agent  →  main.py / scripts/benchmark.py
```

## Data flow (shared by all orchestrators)

```mermaid
flowchart LR
    subgraph ingest["Ingestion — main.py ingest (offline, once)"]
        L[loader] --> C[chunker] --> EM[embedding_service] --> V[("Pinecone\nvector_memory")]
    end
    subgraph serve["Serving — an orchestrator (online, per query)"]
        Q([question]) --> RT[retriever] --> V
        V --> CX[context]
        CX --> GEN[RAG_PROMPT + llm_service] --> A([answer])
    end
```

## The orchestrator contract (the extension point)

Every framework implements the same tiny interface, so they're swappable and
comparable:

```python
class BaseOrchestrator(ABC):
    name: str
    @abstractmethod
    def answer(self, question: str) -> Timing: ...
```

- **`langchain_orchestrator.py`** — `RAG_PROMPT | llm` piped after the retriever.
- **`langgraph_orchestrator.py`** — a `StateGraph` with `retrieve` → `generate`
  nodes over a shared `State`.
- **`crewai_orchestrator.py`, `google_adk_orchestrator.py`** — stubs that raise
  `NotImplementedError` with instructions.

### Adding a new orchestrator (CrewAI / Google ADK / …)

1. `uv add crewai` (or `google-adk`).
2. Implement `answer()` in the stub, reusing the shared core:
   ```python
   from memory.vector_memory import VectorMemory
   from services.llm_service import get_llm
   # build your crew/agent, retrieve via VectorMemory().search(q), return a Timing
   ```
3. Register it in `scripts/benchmark.py` and `main.py`'s orchestrator map.

Because it reuses the same `memory/` and `services/`, it's instantly comparable.

## LangChain vs LangGraph (the working pair)

Both call the *same* retriever and model, so raw latency is nearly identical —
retrieval and generation dominate; orchestration overhead is sub-millisecond. The
benchmark shows it; the decision is architectural:

| Dimension | LangChain (LCEL chain) | LangGraph (StateGraph) |
|-----------|------------------------|------------------------|
| Mental model | A pipeline: `a \| b \| c` | A state machine: nodes + edges |
| Best for | Linear, fixed flows | Branching, loops, retries, human-in-the-loop |
| Control flow | Straight through | Conditional edges, cycles |
| State | Passed along the pipe | Explicit shared `State` (TypedDict) |
| Persistence/memory | Bring your own | Built-in checkpointers + `thread_id` |

## From RAG to Agentic RAG (where this grows)

The LangGraph orchestrator is the seed. Add a `grade_documents` node and a
conditional edge back to `retrieve`, and it becomes a self-correcting loop a
plain LCEL chain *cannot* express — this is where LangGraph (and later CrewAI /
Google ADK agents) earns the agentic structure:

```mermaid
flowchart LR
    START((START)) --> R[retrieve]
    R --> Gr[grade_documents]
    Gr -->|weak| RW[rewrite_query] --> R
    Gr -->|good| G[generate] --> E((END))
```

See [setup.md](setup.md) for installation and run commands.
