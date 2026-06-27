---
title: ingestion/
description: Load and chunk source documents (offline indexing).
category: package
---
# ingestion/
- `loader.py` — load files from `data/documents/` (PDF/CSV/web loaders go here).
- `chunker.py` — split documents into chunks (size/overlap from `config.yaml`).
