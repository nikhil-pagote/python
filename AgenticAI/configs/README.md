---
title: configs/
description: Configuration loading — config separate from code and secrets.
category: package
---
# configs/
- `config.yaml` — tunables (models, index, chunking, retrieval k, agentic.max_retries, benchmark queries).
- `__init__.py` — `config()` and `secret()` loaders (`.env` holds secrets).
