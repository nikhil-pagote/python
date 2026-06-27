"""Base memory interface — short-term, long-term, or vector (RAG) memory."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseMemory(ABC):
    @abstractmethod
    def add(self, documents) -> None:
        """Store documents in memory."""

    @abstractmethod
    def search(self, query: str, k: int | None = None):
        """Return the documents most relevant to a query."""
