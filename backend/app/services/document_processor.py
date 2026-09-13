from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader


def extract_pages_from_pdf(file_path: str) -> list[dict]:
    """Extract text from each PDF page while preserving page numbers."""

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": text.strip(),
                }
            )

    return pages


def chunk_document(pages: list[dict]) -> list[dict]:
    """Split document pages into smaller chunks while preserving metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk_index, chunk_text in enumerate(page_chunks):
            chunks.append(
                {
                    "text": chunk_text,
                    "page_number": page["page_number"],
                    "chunk_index": chunk_index,
                }
            )

    return chunks