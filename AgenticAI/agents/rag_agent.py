"""A RAG agent — answers questions via a chosen orchestrator.

Today it delegates to a fixed retrieve->generate orchestrator. As you add agentic
behavior (tool-calling, planning, doc-grading loops), the agent loop lives here
while the orchestrator stays the coordination layer underneath.
"""

from __future__ import annotations

from agents.base_agent import BaseAgent
from orchestrators.base_orchestrator import BaseOrchestrator
from utils.helpers import Timing


class RAGAgent(BaseAgent):
    name = "rag-agent"

    def __init__(self, orchestrator: BaseOrchestrator) -> None:
        self.orchestrator = orchestrator

    def run(self, query: str) -> Timing:
        return self.orchestrator.answer(query)
