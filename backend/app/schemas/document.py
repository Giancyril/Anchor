from typing import Optional
from pydantic import BaseModel


class IngestionResponse(BaseModel):
    status: str
    document_id: str
    document_name: str
    chunks_created: int
    vectors_upserted: int


class DocumentMeta(BaseModel):
    source_id: str
    document_name: str
    chunks_count: int
    format: str
    category: Optional[str] = None
    url: Optional[str] = None
    last_updated: Optional[str] = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentMeta]
    total: int
