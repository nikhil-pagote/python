---
title: Orchestrators — index
description: >-
  Per-library documentation for each orchestrator. All orchestrators share one
  RAG core and implement the same BaseOrchestrator.answer() contract; these docs
  cover the library used, the files it touches, and what the RAG app does through it.
category: reference
tags: [orchestrators, langchain, langgraph, crewai, google-adk]
last_updated: 2026-06-27
---

# Orchestrators

Every orchestrator drives the **same shared RAG core** and implements one contract:

```python
class BaseOrchestrator(ABC):
    name: str
    def answer(self, question: str) -> Timing: ...
```

So they are swappable (`main.py ask --orchestrator <name>`) and directly comparable
(`main.py benchmark`). Each doc below covers the library, the directory/files it
touches, and what the RAG application does through it.

| Orchestrator | Library | Status | Doc |
|---|---|---|---|
| LangChain (LCEL chain) | `langchain` / `langchain-core` | ✅ working | [langchain.md](langchain.md) |
| LangGraph (agentic) | `langgraph` | ✅ working — doc-grading + query-rewrite loop | [langgraph.md](langgraph.md) |
| CrewAI | `crewai` | 🧩 stub | [crewai.md](crewai.md) |
| Google ADK | `google-adk` | 🧩 stub | [google-adk.md](google-adk.md) |

## The shared core (used by all)

| Concern | Module |
|---|---|
| Documents → chunks | `ingestion/loader.py`, `ingestion/chunker.py` |
| Embeddings | `services/embedding_service.py` (Pinecone `llama-text-embed-v2`) |
| Vector DB / retrieval | `services/vector_store_service.py`, `memory/vector_memory.py` |
| LLM | `services/llm_service.py` (Groq `llama-3.1-8b-instant`) |
| Prompt(s) | `prompts/prompt_templates.py` |
| Config / secrets | `configs/config.yaml`, `.env` |

An orchestrator only adds the file(s) under `orchestrators/`; it reuses everything above.
