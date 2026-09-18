from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import (
    CHROMA_COLLECTION,
    CHROMA_DIR,
    EMBEDDING_MODEL,
    KNOWLEDGE_BASE_DIR,
    validate_api_key,
)


_vector_store = None


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    validate_api_key()

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
    )


def load_documents() -> list[Document]:
    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.txt")):
        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name,
                },
            )
        )

    return documents


def create_vector_store() -> Chroma:
    documents = load_documents()

    if not documents:
        raise RuntimeError(
            "No .txt files found in knowledge_base/"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = splitter.split_documents(documents)

    Path(CHROMA_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )

    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
    )


def get_vector_store() -> Chroma:
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if Path(CHROMA_DIR).exists():
        try:
            _vector_store = Chroma(
                collection_name=CHROMA_COLLECTION,
                persist_directory=str(CHROMA_DIR),
                embedding_function=get_embeddings(),
            )

            if _vector_store._collection.count() > 0:
                return _vector_store

        except Exception:
            _vector_store = None

    _vector_store = create_vector_store()

    return _vector_store