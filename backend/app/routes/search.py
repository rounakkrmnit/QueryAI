from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.retriever import search_documents


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


class SearchRequest(BaseModel):
    query: str
    k: int = 3


@router.post("")
def search(request: SearchRequest):
    """Search the uploaded document using semantic similarity."""

    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    try:
        results = search_documents(
            query=request.query,
            k=request.k,
        )

        return {
            "query": request.query,
            "results": results,
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )