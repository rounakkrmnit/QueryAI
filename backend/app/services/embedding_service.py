from functools import lru_cache

from langchain_google_genai import GoogleGenerativeAIEmbeddings


@lru_cache(maxsize=1)
def get_embedding_model():
    """Return the Gemini embedding model."""

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        output_dimensionality=768,
    )