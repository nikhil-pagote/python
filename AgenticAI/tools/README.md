---
title: tools/
description: Tools an agent can choose to call.
category: package
---
# tools/
- `base_tool.py` — common tool interface.
- `retrieval_tool.py` — retrieval-as-a-tool (the RAG→agent bridge).

**Extension point:** add web search, SQL, or API tools here for an agent to select among.
