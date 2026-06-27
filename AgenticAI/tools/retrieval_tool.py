"""Retrieval exposed as a tool — the bridge from RAG to agentic.

A fixed RAG pipeline calls retrieval directly; an *agent* calls it as a tool it
chooses to use. Wrapping VectorMemory here lets a future tool-calling agent or
orchestrator invoke retrieval as one option among many.
"""

from __future__ import annotations

from memory.vector_memory import VectorMemory
from tools.base_tool import BaseTool
from utils.helpers import format_docs


class RetrievalTool(BaseTool):
    name = "retrieve"
    description = "Search the knowledge base for documents relevant to a query."

    def __init__(self, memory: VectorMemory | None = None) -> None:
        self.memory = memory or VectorMemory()

    def run(self, query: str) -> str:
        return format_docs(self.memory.search(query))
