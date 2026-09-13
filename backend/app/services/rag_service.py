from langchain_core.prompts import ChatPromptTemplate

from app.services.llm_service import get_llm
from app.services.retriever import search_documents


prompt = ChatPromptTemplate.from_template(
    """
You are QueryAI, an intelligent document assistant.

Answer the user's question using ONLY the provided document context.

If the answer cannot be found in the context, say:
"I couldn't find the answer in the uploaded document."

Do not make up information.

Document context:
{context}

User question:
{question}

Answer clearly and concisely.
"""
)


def answer_question(question: str, k: int = 3) -> dict:
    """Retrieve relevant chunks and generate an answer using Gemini."""

    results = search_documents(
        query=question,
        k=k,
    )

    if not results:
        return {
            "answer": "I couldn't find the answer in the uploaded document.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[Page {result['page_number']}]\n{result['text']}"
        for result in results
    )

    messages = prompt.format_messages(
        context=context,
        question=question,
    )

    response = get_llm().invoke(messages)

    if isinstance(response.content, str):
        answer = response.content
    elif isinstance(response.content, list):
        answer_parts = []

        for item in response.content:
            if isinstance(item, dict) and item.get("type") == "text":
                answer_parts.append(item.get("text", ""))

        answer = "\n".join(answer_parts).strip()
    else:
        answer = str(response.content)

    sources = [
        {
            "page_number": result["page_number"],
            "chunk_index": result["chunk_index"],
            "score": result["score"],
        }
        for result in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }