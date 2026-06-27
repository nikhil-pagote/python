"""RAG orchestration with LangChain (LCEL).

A composition of Runnables wired with the pipe operator. Implements the shared
BaseOrchestrator contract so it is swappable with the LangGraph / CrewAI / ADK
orchestrators. Retrieval and generation are timed separately for the benchmark.
"""

from __future__ import annotations

from memory.vector_memory import VectorMemory
from orchestrators.base_orchestrator import BaseOrchestrator
from prompts.prompt_templates import RAG_PROMPT
from services.llm_service import get_llm
from utils.helpers import Timing, format_docs, ms, output_tokens


class LangChainOrchestrator(BaseOrchestrator):
    name = "LangChain (LCEL chain)"

    def __init__(self) -> None:
        self.retriever = VectorMemory().as_retriever()
        self.generate = RAG_PROMPT | get_llm()  # ends at the model -> AIMessage

    def answer(self, question: str) -> Timing:
        t0 = ms()
        docs = self.retriever.invoke(question)
        t1 = ms()
        message = self.generate.invoke(
            {"context": format_docs(docs), "question": question}
        )
        t2 = ms()
        return Timing(
            question=question,
            answer=message.content,
            retrieval_ms=round(t1 - t0, 1),
            generation_ms=round(t2 - t1, 1),
            total_ms=round(t2 - t0, 1),
            output_tokens=output_tokens(message),
        )
