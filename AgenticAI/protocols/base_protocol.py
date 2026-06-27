"""Base communication protocol (extension point — not used by RAG yet).

Protocols define how agents talk to each other or to external systems, e.g. MCP
(Model Context Protocol) or A2A (agent-to-agent). Implement a subclass here when
you add multi-agent communication.
"""


from abc import ABC, abstractmethod


class BaseProtocol(ABC):
    @abstractmethod
    def send(self, message):
        """Send a message to another agent/system."""

    @abstractmethod
    def receive(self):
        """Receive an incoming message."""
