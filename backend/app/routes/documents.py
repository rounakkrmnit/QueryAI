from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.document_processor import (
    extract_pages_from_pdf,
    chunk_document,
)

from app.services.vector_store import create_vector_store


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract its text, and create document chunks."""

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    file_path = UPLOAD_DIR / file.filename

    contents = await file.read()
    file_path.write_bytes(contents)

    pages = extract_pages_from_pdf(str(file_path))
    chunks = chunk_document(pages)
    create_vector_store(chunks)

    return {
        "filename": file.filename,
        "message": "Document processed and indexed successfully.",
        "pages": len(pages),
        "chunks": len(chunks),
    }