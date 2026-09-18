from typing import Any

from app.core.config import TOP_K
from app.services.llm import get_chat_model
from app.services.vector_store import get_vector_store


def content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            else:
                parts.append(str(item))

        return "\n".join(part for part in parts if part).strip()

    return str(content)


def answer_question(
    question: str,
    history: list[dict[str, str]] | None = None,
) -> dict:
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        question,
        k=TOP_K,
    )

    if not documents:
        return {
            "answer": (
                "I could not find relevant information in the knowledge base. "
                "Please contact a human support agent."
            ),
            "sources": [],
        }

    context_parts = []
    sources = []

    for document in documents:
        source = document.metadata.get(
            "source",
            "knowledge_base",
        )

        context_parts.append(
            f"[Source: {source}]\n{document.page_content}"
        )

        if source not in sources:
            sources.append(source)

    context = "\n\n---\n\n".join(context_parts)

    history_text = "(none)"

    if history:
        recent_history = history[-6:]
        history_text = "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}"
            for item in recent_history
            if item.get("content")
        )

    prompt = f"""You are an AI Customer Support Agent.

STRICT RULES:
1. Answer using only the supplied knowledge-base context.
2. Never invent company policies, prices, deadlines, refunds, order status,
   account details, or other facts.
3. If the knowledge base does not contain enough information, say:
   "I don't have enough information in the knowledge base to answer that."
   Then recommend contacting human support.
4. Never ask for or expose a password, full card number, CVV, OTP,
   authentication secret, or other sensitive credential.
5. Be polite, concise, and practical.
6. You may use recent conversation context to understand the user's question,
   but factual answers must be grounded in the knowledge-base context.
7. If the request is unrelated to customer support, politely explain that
   you are designed for customer-support questions.

KNOWLEDGE BASE:
{context}

RECENT CONVERSATION:
{history_text}

USER QUESTION:
{question}
"""

    response = get_chat_model().invoke(prompt)
    answer = content_to_text(response.content)

    return {
        "answer": answer,
        "sources": sources,
    }
