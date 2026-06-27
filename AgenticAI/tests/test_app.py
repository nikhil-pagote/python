"""Light structure/config tests — no network, no API keys required.

uv run pytest AgenticAI/tests
"""

from configs import config
from ingestion.loader import load_documents
from prompts.prompt_templates import RAG_PROMPT


def test_config_has_expected_sections():
    cfg = config()
    for key in ("llm", "embeddings", "vectordb", "retrieval", "chunking", "benchmark"):
        assert key in cfg


def test_embedding_dimension_matches_pinecone_model():
    cfg = config()
    assert cfg["embeddings"]["model"] == "llama-text-embed-v2"
    assert cfg["embeddings"]["dimension"] == 1024


def test_corpus_loads():
    docs = load_documents()
    assert len(docs) >= 5
    assert all(d.page_content and d.metadata.get("source") for d in docs)


def test_prompt_exposes_context_and_question():
    assert set(RAG_PROMPT.input_variables) == {"context", "question"}
