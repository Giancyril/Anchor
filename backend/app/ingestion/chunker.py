import re
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings


def extract_section_heading(text: str) -> str:
    """
    Extract the first Markdown heading from a text block as the section name.
    Falls back to 'General' if none found.
    """
    match = re.search(r"^#{1,3}\s+(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else "General"


def chunk_documents(
    documents: List[Document],
    document_id: str,
    document_name: str,
    url: str = "",
    category: str = "",
) -> List[Document]:
    """
    Split documents into chunks and attach rich metadata to each chunk.
    Chunk size and overlap are driven by app settings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    chunks = splitter.split_documents(documents)

    enriched = []
    for idx, chunk in enumerate(chunks):
        section = extract_section_heading(chunk.page_content)
        chunk.metadata.update({
            "source_id": document_id,
            "document_name": document_name,
            "section": section,
            "url": url,
            "category": category,
            "chunk_index": idx,
            "total_chunks": len(chunks),
        })
        enriched.append(chunk)

    return enriched
