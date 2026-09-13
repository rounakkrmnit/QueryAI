from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.services.embedding_service import get_embedding_model


VECTORSTORE_DIR = Path("vectorstore")


def create_vector_store(chunks: list[dict]) -> FAISS:
    """Create and save a FAISS vector store from document chunks."""

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    embedding_model = get_embedding_model()

    vector_store = FAISS.from_texts(
        texts=texts,
        embedding=embedding_model,
        metadatas=metadatas,
    )

    VECTORSTORE_DIR.mkdir(exist_ok=True)

    vector_store.save_local(
        str(VECTORSTORE_DIR),
        index_name="documents",
    )

    return vector_store