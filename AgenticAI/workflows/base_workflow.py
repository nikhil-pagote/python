"""Base workflow (extension point — not used by single-orchestrator RAG yet).

Workflows sequence tasks/agents — sequential, parallel, or hybrid. Add subclasses
here when you coordinate multiple agents.
"""


from abc import ABC, abstractmethod


class BaseWorkflow(ABC):
    @abstractmethod
    def run(self, inputs: dict) -> dict:
        """Run the workflow and return its outputs."""
