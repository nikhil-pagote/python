---
title: agents/
description: Agent definitions — the entities that decide and act.
category: package
---
# agents/
- `base_agent.py` — common agent interface (`run(query)`).
- `rag_agent.py` — wraps an orchestrator to answer a question.

**Extension point:** add planner / executor / critic agents here as you grow toward the 2026 agentic-RAG loop.
