from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import CHAT_MODEL, validate_api_key


def get_chat_model() -> ChatGoogleGenerativeAI:
    validate_api_key()

    return ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        temperature=0.2,
        max_retries=2,
    )
