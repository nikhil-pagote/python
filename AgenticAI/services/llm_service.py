"""LLM service — Groq chat model (external service wrapper)."""

from __future__ import annotations

from functools import lru_cache

import httpx
from langchain_groq import ChatGroq

from configs import config, secret


@lru_cache
def _http_client() -> httpx.Client:
    """IPv4-only HTTP client, forwarded to Groq via ChatGroq's `http_client`.

    On this environment httpx's IPv6 "happy eyeballs" stalls ~24s per Groq call
    before falling back to IPv4 (curl was always fast — only the SDK stalled).
    Binding the socket to an IPv4 local address skips IPv6 entirely. ChatGroq
    forwards `http_client` to the underlying `groq.Groq` sync client.
    """
    return httpx.Client(
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
        timeout=60.0,
    )


def get_llm() -> ChatGroq:
    settings = config()["llm"]
    return ChatGroq(
        model=settings["model"],
        temperature=settings["temperature"],
        api_key=secret("GROQ_API_KEY"),
        http_client=_http_client(),
    )
