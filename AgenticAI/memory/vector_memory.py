"""Vector memory — long-term semantic memory backed by Pinecone.

In an agentic system this is the RAG component (the agentic templates label it
"vector_memory.py # RAG embeddings"): store documents as embeddings and retrieve
the most relevant on demand. Orchestrators, tools, and agents all read from it.
"""

from __future__ import annotations

from configs import config
from memory.base_memory import BaseMemory
from services.vector_store_service import get_vector_store


class VectorMemory(BaseMemory):
    def __init__(self) -> None:
        self.store = get_vector_store()

    def add(self, documents) -> None:
        self.store.add_documents(
            documents, ids=[f"doc-{i}" for i in range(len(documents))]
        )

    def search(self, query: str, k: int | None = None):
        return self.store.similarity_search(query, k=k or config()["retrieval"]["k"])

    def as_retriever(self):
        return self.store.as_retriever(search_kwargs={"k": config()["retrieval"]["k"]})
