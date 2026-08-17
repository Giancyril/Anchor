import re
from typing import List, Dict, Tuple
from langchain_core.documents import Document
from app.schemas.chat import CitationSource


def parse_citations(
    answer_text: str,
    retrieved_chunks: List[Document],
) -> Tuple[str, List[CitationSource]]:
    """
    Extract inline citation markers [1], [2] etc. from LLM answer text,
    map them back to source document metadata, and return structured sources.

    Args:
        answer_text: Raw LLM output containing [n] citation markers.
        retrieved_chunks: Ordered list of retrieved Document objects (index 0 = [1]).

    Returns:
        (cleaned_answer, sources) where sources is a list of CitationSource objects.
    """
    # Find all citation numbers referenced in the answer
    cited_indices = sorted(set(int(m) for m in re.findall(r"\[(\d+)\]", answer_text)))

    sources: List[CitationSource] = []
    for n in cited_indices:
        # n is 1-indexed; chunks list is 0-indexed
        chunk_idx = n - 1
        if 0 <= chunk_idx < len(retrieved_chunks):
            chunk = retrieved_chunks[chunk_idx]
            meta = chunk.metadata
            snippet = chunk.page_content[:200].strip().replace("\n", " ")
            sources.append(CitationSource(
                citation_index=n,
                document_name=meta.get("document_name", "Unknown Document"),
                section=meta.get("section", "General"),
                url=meta.get("url") or None,
                snippet=snippet,
            ))

    return answer_text, sources
