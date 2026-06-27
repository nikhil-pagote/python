"""Benchmark the orchestrators — same RAG task, each framework, timed.

Assumes the index is built (`uv run AgenticAI/main.py ingest`). Every orchestrator
shares one retrieval + generation core, so the timings isolate orchestration
overhead rather than different work.

    uv run AgenticAI/scripts/benchmark.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from configs import config  # noqa: E402
from orchestrators.langchain_orchestrator import LangChainOrchestrator  # noqa: E402
from orchestrators.langgraph_orchestrator import LangGraphOrchestrator  # noqa: E402


def _avg(timings, attr: str) -> float:
    return round(sum(getattr(t, attr) for t in timings) / len(timings), 1)


def run_benchmark() -> None:
    queries = config()["benchmark"]["queries"]
    orchestrators = [LangChainOrchestrator(), LangGraphOrchestrator()]
    print(f"Benchmarking {len(queries)} queries per orchestrator...\n")

    rows = {o.name: [o.answer(q) for q in queries] for o in orchestrators}

    header = (
        f"{'orchestrator':<24}{'retrieval':>12}{'generation':>13}"
        f"{'total':>10}{'tokens':>9}"
    )
    print(header)
    print("-" * len(header))
    for name, timings in rows.items():
        print(
            f"{name:<24}{_avg(timings, 'retrieval_ms'):>10}ms"
            f"{_avg(timings, 'generation_ms'):>11}ms"
            f"{_avg(timings, 'total_ms'):>8}ms{_avg(timings, 'output_tokens'):>9}"
        )

    print(
        "\nSame retrieval + generation core, so the gap between rows is "
        "orchestration overhead. The meaningful difference is architectural; "
        "see docs/architecture.md."
    )


if __name__ == "__main__":
    run_benchmark()
