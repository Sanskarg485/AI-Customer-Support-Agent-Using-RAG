# AI Customer Support Agent

Complete FastAPI + LangChain + Gemini + ChromaDB RAG application.

## Project structure

```text
AI-Customer-Support-Agent/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── input.py
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   └── health.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── chat.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── llm.py
│       ├── rag.py
│       └── vector_store.py
│
├── knowledge_base/
│   └── faq.txt
│
├── chroma_db/
│   └── .gitkeep
│
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## 1. Add your API key

Open `.env`.

You will see:

```env
GOOGLE_API_KEY=
```

Paste your Gemini API key after `=`.

Example:

```env
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

Do not add quotes unless your key actually requires them.

## 2. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Build ChromaDB

Before starting the server:

```bash
python input.py
```

This reads all `.txt` files from:

```text
knowledge_base/
```

It chunks them, creates embeddings, and stores them in:

```text
chroma_db/
```

If you change the knowledge base later, run `python input.py` again.

## 5. Start the backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The frontend is:

```text
http://127.0.0.1:8000/
```

## API routes

### Health

```text
GET /api/health
```

### Chat

```text
POST /api/chat
```

Example request:

```json
{
    "question": "How long does standard shipping take?",
    "history": []
}
```

### Swagger

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

## Architecture

```text
                         FRONTEND
                  index.html / CSS / JS
                            |
                            v
                       FastAPI
                            |
                  +---------+---------+
                  |                   |
             /api/health          /api/chat
                                      |
                                      v
                                RAG SERVICE
                                      |
                       +--------------+--------------+
                       |                             |
                       v                             v
                Gemini Embeddings               ChromaDB
                       |                       Vector Search
                       +--------------+--------------+
                                      |
                              Relevant Context
                                      |
                                      v
                               Gemini LLM
                                      |
                                      v
                               Final Answer
                                      |
                                      v
                                  Frontend
```

## Important

The included knowledge base is sample/demo content.

For an actual company customer-support system, replace:

```text
knowledge_base/faq.txt
```

with the company's real FAQs, product documentation, return policy, refund policy, shipping information, account rules, escalation procedures, etc.

The RAG prompt intentionally prevents the model from inventing unsupported policies.


## Quick Windows PowerShell run

```powershell
.\start.ps1
```

Then open `http://127.0.0.1:8000/`.

If your Gemini project exposes a different model, change `CHAT_MODEL` in `.env` to a model available to your API key.
