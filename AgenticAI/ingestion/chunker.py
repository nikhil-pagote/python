"""Split documents into retrievable chunks (chunk size/overlap from config)."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from configs import config


def chunk(docs: list[Document]) -> list[Document]:
    settings = config()["chunking"]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings["chunk_size"],
        chunk_overlap=settings["chunk_overlap"],
    )
    return splitter.split_documents(docs)
