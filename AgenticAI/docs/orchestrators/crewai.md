---
title: CrewAI orchestrator (planned)
description: >-
  Extension point for a CrewAI-based orchestrator over the shared RAG core.
category: reference
framework: crewai
tags: [crewai, orchestrator, rag, extension-point]
last_updated: 2026-06-27
---

# CrewAI orchestrator (planned)

## Library

[CrewAI](https://docs.crewai.com/) — a framework for role-playing **multi-agent
crews**: agents with roles, goals, and tasks that collaborate. Package: `crewai`.

## Directory structure it touches

| File | Role |
|---|---|
| **`orchestrators/crewai_orchestrator.py`** | **owned** — currently a stub raising `NotImplementedError` |
| `memory/vector_memory.py` | retrieval (reuse for parity) |
| `services/llm_service.py` | LLM (reuse for parity) |
| `prompts/prompt_templates.py` | prompts (reuse) |

## What the RAG application would do through it

Model RAG as a small crew — e.g. a *Researcher* agent that retrieves and a
*Writer* agent that answers — to compare CrewAI's multi-agent style against the
LCEL chain and the LangGraph graph on the same task.

## How to implement

1. `uv add crewai` (then uncomment it in `requirements.txt`).
2. In `orchestrators/crewai_orchestrator.py`, implement `answer(question) -> Timing`:
   build a `Crew`, retrieve via `VectorMemory().search(question)`, run the crew,
   and return a `Timing` (reuse `utils.helpers`).
3. Register it in `main.py` (`_orchestrator`) and `scripts/benchmark.py`.

Docs: https://docs.crewai.com/
