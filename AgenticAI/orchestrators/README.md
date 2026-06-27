---
title: orchestrators/
description: Coordination layer — the framework swap point.
category: package
---
# orchestrators/
One file per framework; all implement `base_orchestrator.BaseOrchestrator.answer()`.
- `langchain_orchestrator.py` — LCEL chain (fixed). ✅
- `langgraph_orchestrator.py` — agentic StateGraph (grade + rewrite loop). ✅
- `crewai_orchestrator.py`, `google_adk_orchestrator.py` — stubs (extension points).

Per-library docs: [`../docs/orchestrators/`](../docs/orchestrators/README.md).
