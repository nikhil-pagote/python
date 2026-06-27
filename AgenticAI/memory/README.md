---
title: memory/
description: Memory — what the system knows and remembers.
category: package
---
# memory/
- `base_memory.py` — common memory interface.
- `vector_memory.py` — Pinecone-backed long-term/semantic memory (the RAG core).

**Extension point:** add session / conversation memory (e.g. Supabase) here for multi-turn chat.
