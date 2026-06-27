"""Common utilities: timing, logging, and small formatters."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


@dataclass
class Timing:
    """One question's measured cost, identical shape for every orchestrator.

    `trace` is optional — agentic orchestrators record the path of nodes they
    visited (retrieve -> grade -> rewrite -> ...); fixed ones leave it blank.
    """

    question: str
    answer: str
    retrieval_ms: float
    generation_ms: float
    total_ms: float
    output_tokens: int
    trace: str = ""


def get_logger(name: str) -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_DIR / "app.log")
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        )
        logger.addHandler(handler)
    return logger


def format_docs(docs) -> str:
    return "\n".join(d.page_content for d in docs)


def output_tokens(message) -> int:
    """Pull output token count off a Groq AIMessage (0 if not reported)."""
    usage = getattr(message, "usage_metadata", None) or {}
    return int(usage.get("output_tokens", 0))


def ms() -> float:
    return time.perf_counter() * 1000.0
