"""Agentic RAG orchestration with LangGraph.

A self-correcting graph: retrieve -> grade documents -> (relevant?) generate, or
rewrite the query and retrieve again, up to `agentic.max_retries`. The model
judges its own retrieval and loops to fix a weak result — which a fixed LCEL
chain fundamentally cannot do.

    START -> retrieve -> grade ── relevant ───────────────▶ generate -> END
                           └────── not relevant & retries ─▶ rewrite -> retrieve
"""

from __future__ import annotations

from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from configs import config
from memory.vector_memory import VectorMemory
from orchestrators.base_orchestrator import BaseOrchestrator
from prompts.prompt_templates import GRADER_PROMPT, RAG_PROMPT, REWRITE_PROMPT
from services.llm_service import get_llm
from utils.helpers import Timing, format_docs, ms, output_tokens


class GradeDocuments(BaseModel):
    """Binary relevance judgement for retrieved documents."""

    relevant: bool = Field(
        description="True if the documents are relevant to the question."
    )


class State(TypedDict):
    question: str  # the user's original question (used for grading + generation)
    query: str  # current search query (rewritten on a miss)
    documents: list
    relevant: bool
    answer: str
    retries: int
    retrieval_ms: float
    grading_ms: float
    rewrite_ms: float
    generation_ms: float
    output_tokens: int
    trace: list


class LangGraphOrchestrator(BaseOrchestrator):
    name = "LangGraph (agentic)"

    def __init__(self) -> None:
        self.max_retries = config().get("agentic", {}).get("max_retries", 2)
        retriever = VectorMemory().as_retriever()
        llm = get_llm()
        grader = GRADER_PROMPT | llm.with_structured_output(GradeDocuments)
        rewriter = REWRITE_PROMPT | llm | StrOutputParser()
        generator = RAG_PROMPT | llm

        def retrieve(state: State) -> dict:
            t0 = ms()
            docs = retriever.invoke(state["query"])
            return {
                "documents": docs,
                "retrieval_ms": state.get("retrieval_ms", 0.0) + round(ms() - t0, 1),
                "trace": state.get("trace", []) + ["retrieve"],
            }

        def grade(state: State) -> dict:
            t0 = ms()
            verdict = grader.invoke(
                {
                    "context": format_docs(state["documents"]),
                    "question": state["question"],
                }
            )
            return {
                "relevant": bool(verdict.relevant),
                "grading_ms": state.get("grading_ms", 0.0) + round(ms() - t0, 1),
                "trace": state["trace"]
                + [f"grade:{'relevant' if verdict.relevant else 'irrelevant'}"],
            }

        def rewrite(state: State) -> dict:
            t0 = ms()
            new_query = rewriter.invoke({"question": state["query"]})
            return {
                "query": new_query.strip(),
                "retries": state["retries"] + 1,
                "rewrite_ms": state.get("rewrite_ms", 0.0) + round(ms() - t0, 1),
                "trace": state["trace"] + ["rewrite"],
            }

        def generate(state: State) -> dict:
            t0 = ms()
            message = generator.invoke(
                {
                    "context": format_docs(state["documents"]),
                    "question": state["question"],
                }
            )
            return {
                "answer": message.content,
                "generation_ms": round(ms() - t0, 1),
                "output_tokens": output_tokens(message),
                "trace": state["trace"] + ["generate"],
            }

        def decide(state: State) -> str:
            if state["relevant"]:
                return "generate"
            if state["retries"] < self.max_retries:
                return "rewrite"
            return "generate"  # give up rewriting; answer with what we have

        builder = StateGraph(State)
        builder.add_node("retrieve", retrieve)
        builder.add_node("grade", grade)
        builder.add_node("rewrite", rewrite)
        builder.add_node("generate", generate)
        builder.add_edge(START, "retrieve")
        builder.add_edge("retrieve", "grade")
        builder.add_conditional_edges(
            "grade", decide, {"generate": "generate", "rewrite": "rewrite"}
        )
        builder.add_edge("rewrite", "retrieve")
        builder.add_edge("generate", END)
        self.graph = builder.compile()

    def answer(self, question: str) -> Timing:
        t0 = ms()
        final = self.graph.invoke(
            {"question": question, "query": question, "retries": 0, "trace": []}
        )
        total = round(ms() - t0, 1)
        return Timing(
            question=question,
            answer=final["answer"],
            retrieval_ms=round(final.get("retrieval_ms", 0.0), 1),
            generation_ms=round(final.get("generation_ms", 0.0), 1),
            total_ms=total,
            output_tokens=final.get("output_tokens", 0),
            trace=" -> ".join(final.get("trace", [])),
        )
