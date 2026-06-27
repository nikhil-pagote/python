"""Entry point — ingest, ask, or benchmark.

uv run AgenticAI/main.py ingest
uv run AgenticAI/main.py ask "What is Pinecone used for?" --orchestrator langgraph
uv run AgenticAI/main.py benchmark
"""

from __future__ import annotations

import argparse

from agents.rag_agent import RAGAgent
from ingestion.chunker import chunk
from ingestion.loader import load_documents
from memory.vector_memory import VectorMemory
from services.vector_store_service import ensure_index
from utils.helpers import get_logger

log = get_logger("rag")


def ingest() -> None:
    ensure_index()
    chunks = chunk(load_documents())
    VectorMemory().add(chunks)
    log.info("ingested %d chunks", len(chunks))
    print(f"Ingested {len(chunks)} chunks into vector memory.")


def _orchestrator(name: str):
    if name == "langchain":
        from orchestrators.langchain_orchestrator import LangChainOrchestrator

        return LangChainOrchestrator()
    from orchestrators.langgraph_orchestrator import LangGraphOrchestrator

    return LangGraphOrchestrator()


def ask(question: str, orchestrator: str) -> None:
    agent = RAGAgent(_orchestrator(orchestrator))
    t = agent.run(question)
    print(f"Q: {t.question}")
    print(f"A: {t.answer}")
    print(
        f"   retrieval={t.retrieval_ms}ms generation={t.generation_ms}ms "
        f"total={t.total_ms}ms tokens={t.output_tokens}"
    )
    if t.trace:
        print(f"   trace: {t.trace}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic RAG — multi-orchestrator")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ingest", help="build vector memory from data/documents/")
    ask_p = sub.add_parser("ask", help="answer one question")
    ask_p.add_argument("question")
    ask_p.add_argument(
        "--orchestrator", choices=["langchain", "langgraph"], default="langgraph"
    )
    sub.add_parser("benchmark", help="time all orchestrators side by side")

    args = parser.parse_args()
    if args.cmd == "ingest":
        ingest()
    elif args.cmd == "ask":
        ask(args.question, args.orchestrator)
    elif args.cmd == "benchmark":
        from scripts.benchmark import run_benchmark

        run_benchmark()


if __name__ == "__main__":
    main()
