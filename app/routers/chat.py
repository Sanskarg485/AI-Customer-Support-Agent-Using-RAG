import time

from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag import answer_question

router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    started = time.perf_counter()

    try:
        result = answer_question(
            question=request.question,
            history=[
                {
                    "role": item.role,
                    "content": item.content,
                }
                for item in request.history
            ],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        print(f"Internal chat error: {exc}")

        raise HTTPException(
            status_code=500,
            detail=(
                "The AI support agent could not process the request. "
                "Check the server terminal for details."
            ),
        ) from exc

    response_time = int(
        (time.perf_counter() - started) * 1000
    )

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        response_time_ms=response_time,
    )
