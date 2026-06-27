---
title: protocols/
description: Agent communication protocols (extension point).
category: package
---
# protocols/
- `base_protocol.py` — interface for agent-to-agent / tool messaging.

**Extension point (not used by single-orchestrator RAG yet):** implement MCP or A2A subclasses here when agents need to talk to each other or external systems.
