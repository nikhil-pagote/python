"""CrewAI orchestrator (extension point — not implemented yet).

Implement BaseOrchestrator.answer() with a CrewAI crew. Add `crewai` to
requirements first, and reuse services.llm_service / memory.vector_memory so the
comparison against the LangChain and LangGraph orchestrators stays fair.
"""


from orchestrators.base_orchestrator import BaseOrchestrator
from utils.helpers import Timing


class CrewAIOrchestrator(BaseOrchestrator):
    name = "CrewAI"

    def answer(self, question: str) -> Timing:
        raise NotImplementedError(
            "CrewAI orchestrator not implemented yet — build a crew here and "
            "return a Timing, reusing the shared services and vector memory."
        )
