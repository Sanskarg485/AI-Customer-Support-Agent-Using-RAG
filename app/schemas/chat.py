from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: str = Field(..., min_length=1, max_length=30)
    content: str = Field(..., min_length=1, max_length=5000)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    history: list[HistoryMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    response_time_ms: int
