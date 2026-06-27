"""Load the source corpus from data/documents/.

The "Data Sources -> Document Loader" stage. Each file becomes a Document (its
filename stem is the source tag). Real projects point langchain_community loaders
(PDF/CSV/web) at this directory; here we read plain .md/.txt files.
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "documents"


def load_documents() -> list[Document]:
    docs: list[Document] = []
    for path in sorted(DATA_DIR.glob("*.md")) + sorted(DATA_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            docs.append(Document(page_content=text, metadata={"source": path.stem}))
    return docs
