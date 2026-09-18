from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import STATIC_DIR
from app.routers import chat, health

app = FastAPI(
    title="AI Customer Support Agent",
    description=(
        "AI customer-support RAG application using "
        "FastAPI, LangChain, Gemini and ChromaDB."
    ),
    version="1.0.0",
)

# API routes
app.include_router(health.router)
app.include_router(chat.router)

# Frontend static files
app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/docs-info", include_in_schema=False)
def docs_info():
    return {
        "message": "API documentation is available at /docs",
        "routes": {
            "frontend": "/",
            "health": "/api/health",
            "chat": "POST /api/chat",
            "swagger": "/docs",
            "redoc": "/redoc",
        },
    }
