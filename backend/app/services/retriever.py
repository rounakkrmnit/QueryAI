from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.services.embedding_service import get_embedding_model


VECTORSTORE_DIR = Path("vectorstore")


def load_vector_store() -> FAISS:
    """Load the saved FAISS vector store."""

    if not VECTORSTORE_DIR.exists():
        raise FileNotFoundError(
            "Vector store not found. Upload a document first."
        )

    embedding_model = get_embedding_model()

    vector_store = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embedding_model,
        index_name="documents",
        allow_dangerous_deserialization=True,
    )

    return vector_store


def search_documents(
    query: str,
    k: int = 3,
) -> list[dict]:
    """Find the most relevant document chunks for a query."""

    vector_store = load_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    matches = []

    for document, score in results:
        matches.append(
            {
                "text": document.page_content,
                "page_number": document.metadata.get("page_number"),
                "chunk_index": document.metadata.get("chunk_index"),
                "score": float(score),
            }
        )

    return matches