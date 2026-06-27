"""Vector store service — Pinecone index lifecycle and store construction."""

from __future__ import annotations

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from configs import config, secret
from services.embedding_service import get_embeddings


def _client() -> Pinecone:
    return Pinecone(api_key=secret("PINECONE_API_KEY"))


def _index_name() -> str:
    return config()["vectordb"]["index_name"]


def ensure_index() -> None:
    """Create the serverless index if it does not exist (idempotent)."""
    vdb = config()["vectordb"]
    pc = _client()
    if not pc.has_index(vdb["index_name"]):
        pc.create_index(
            name=vdb["index_name"],
            dimension=config()["embeddings"]["dimension"],
            metric=vdb["metric"],
            spec=ServerlessSpec(cloud=vdb["cloud"], region=vdb["region"]),
        )


def get_vector_store() -> PineconeVectorStore:
    return PineconeVectorStore(
        index=_client().Index(_index_name()),
        embedding=get_embeddings(),
    )
