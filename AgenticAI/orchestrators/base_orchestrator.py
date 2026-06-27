"""Base orchestrator interface — coordinates retrieval + generation.

Every framework (LangChain, LangGraph, CrewAI, Google ADK) implements this same
contract, so orchestrators are swappable and directly comparable. This is the
extension point: add a new file here per framework.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from utils.helpers import Timing


class BaseOrchestrator(ABC):
    name: str = "orchestrator"

    @abstractmethod
    def answer(self, question: str) -> Timing:
        """Answer a question end to end, returning a timed result."""
