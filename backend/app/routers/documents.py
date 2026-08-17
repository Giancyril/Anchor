from fastapi import APIRouter
from app.schemas.document import DocumentListResponse

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.get("", response_model=DocumentListResponse)
async def list_documents():
    from app.routers.ingest import _document_registry
    docs = list(_document_registry.values())
    return DocumentListResponse(documents=docs, total=len(docs))
