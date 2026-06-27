---
title: services/
description: External service wrappers (one place per provider).
category: package
---
# services/
- `llm_service.py` — Groq chat model (forces IPv4 `http_client`; see file).
- `embedding_service.py` — Pinecone hosted embeddings.
- `vector_store_service.py` — Pinecone index lifecycle + store.
