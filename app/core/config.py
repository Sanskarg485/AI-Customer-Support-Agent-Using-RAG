import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemini-2.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

CHROMA_DIR_VALUE = os.getenv("CHROMA_DIR", "./chroma_db")
CHROMA_DIR = Path(CHROMA_DIR_VALUE)
if not CHROMA_DIR.is_absolute():
    CHROMA_DIR = BASE_DIR / CHROMA_DIR

CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION",
    "customer_support_knowledge",
)
TOP_K = int(os.getenv("TOP_K", "4"))

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
STATIC_DIR = BASE_DIR / "static"


def validate_api_key() -> None:
    if not GOOGLE_API_KEY:
        raise RuntimeError(
            "GOOGLE_API_KEY is empty. Open .env and add your Gemini API key."
        )
