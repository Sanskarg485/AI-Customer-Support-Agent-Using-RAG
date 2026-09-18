from pathlib import Path
import shutil

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


def main():
    validate_api_key()

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

    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
    )

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=CHROMA_COLLECTION,
        persist_directory=str(CHROMA_DIR),
    )

    print("=" * 60)
    print("ChromaDB knowledge base created successfully.")
    print(f"Documents : {len(documents)}")
    print(f"Chunks    : {len(chunks)}")
    print(f"Database  : {CHROMA_DIR}")
    print(f"Collection: {CHROMA_COLLECTION}")
    print("=" * 60)


if __name__ == "__main__":
    main()
