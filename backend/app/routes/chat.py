from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.rag_service import answer_question


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class QuestionRequest(BaseModel):
    question: str
    k: int = 3


@router.post("")
def chat(request: QuestionRequest):
    """Answer a question using RAG."""

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        return answer_question(
            question=request.question,
            k=request.k,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )