"""Embedding service — Pinecone hosted inference (external service wrapper)."""

from __future__ import annotations

from langchain_pinecone import PineconeEmbeddings

from configs import config, secret


def get_embeddings() -> PineconeEmbeddings:
    secret("PINECONE_API_KEY")  # fail fast; the client reads it from env
    return PineconeEmbeddings(model=config()["embeddings"]["model"])
