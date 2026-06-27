"""Google ADK orchestrator (extension point — not implemented yet).

Implement BaseOrchestrator.answer() with the Google Agent Development Kit. Add
`google-adk` to requirements first, and reuse services.llm_service /
memory.vector_memory for parity with the other orchestrators.
"""


from orchestrators.base_orchestrator import BaseOrchestrator
from utils.helpers import Timing


class GoogleADKOrchestrator(BaseOrchestrator):
    name = "Google ADK"

    def answer(self, question: str) -> Timing:
        raise NotImplementedError(
            "Google ADK orchestrator not implemented yet — build the agent here "
            "and return a Timing, reusing the shared services and vector memory."
        )
