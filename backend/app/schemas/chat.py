from typing import List, Optional
from pydantic import BaseModel


class ChatFilters(BaseModel):
    category: Optional[str] = None
    product_line: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    filters: Optional[ChatFilters] = None


class CitationSource(BaseModel):
    citation_index: int
    document_name: str
    section: str
    url: Optional[str] = None
    snippet: str


class ChatResponse(BaseModel):
    answer: str
    confidence: str  # "high" | "low"
    escalated: bool
    sources: List[CitationSource]
    session_id: Optional[str] = None
