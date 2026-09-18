from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import (
    CHROMA_COLLECTION,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    validate_api_key,
)


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    validate_api_key()
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)


def get_vector_store() -> Chroma:
    if not Path(CHROMA_DIR).exists():
        raise RuntimeError(
            "ChromaDB has not been created yet. Run: python input.py"
        )

    return Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
    )
