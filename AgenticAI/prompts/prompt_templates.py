"""Prompt templates — kept separate from code so they can be tuned in one place."""

from langchain_core.prompts import ChatPromptTemplate

# Generation: answer grounded only in retrieved context.
RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a concise assistant. Answer the question using only the "
            "provided context. If the context does not contain the answer, say "
            "you don't know.",
        ),
        ("human", "Context:\n{context}\n\nQuestion: {question}"),
    ]
)

# Agentic RAG: grade whether retrieved documents are relevant to the question.
GRADER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a grader assessing whether the retrieved documents are "
            "relevant to the user's question. Give a binary relevance judgement.",
        ),
        ("human", "Retrieved documents:\n{context}\n\nQuestion: {question}"),
    ]
)

# Agentic RAG: rewrite the query to retrieve better documents on a miss.
REWRITE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite the user's question into a better search query that will "
            "retrieve more relevant documents. Return only the rewritten query.",
        ),
        ("human", "Question: {question}"),
    ]
)
