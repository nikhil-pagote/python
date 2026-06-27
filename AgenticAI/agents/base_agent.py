"""Base agent interface — the common contract every agent implements."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    name: str = "agent"

    @abstractmethod
    def run(self, query: str):
        """Handle a user query and return a result."""
