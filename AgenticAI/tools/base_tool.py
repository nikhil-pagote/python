"""Base tool interface — anything an agent can choose to call."""


from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str = "tool"
    description: str = ""

    @abstractmethod
    def run(self, **kwargs):
        """Execute the tool and return a result."""
