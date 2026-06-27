"""LLM service — Groq chat model (external service wrapper)."""

from __future__ import annotations

from langchain_groq import ChatGroq

from configs import config, secret


def get_llm() -> ChatGroq:
    settings = config()["llm"]
    return ChatGroq(
        model=settings["model"],
        temperature=settings["temperature"],
        api_key=secret("GROQ_API_KEY"),
    )
