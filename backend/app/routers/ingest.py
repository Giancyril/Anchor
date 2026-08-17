import os
import shutil
import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.document import IngestionResponse, DocumentMeta, DocumentListResponse
from app.ingestion.loader import load_document, SUPPORTED_FORMATS
from app.ingestion.chunker import chunk_documents
from app.services.embedding_service import embed_texts
from app.services.pinecone_service import get_pinecone_index, delete_vectors_by_source, upsert_chunks
from app.config import settings

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

# In-memory document registry (v1 — no DB dependency)
_document_registry: dict[str, DocumentMeta] = {}
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("", response_model=IngestionResponse)
async def ingest_document(
    file: UploadFile = File(...),
    document_name: Optional[str] = Form(None),
    url: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
):
    # Validate file extension
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: {', '.join(SUPPORTED_FORMATS)}"
        )

    # Save uploaded file to disk
    doc_name = document_name or file.filename or f"document_{uuid.uuid4().hex[:8]}"
    source_id = f"doc_{uuid.uuid4().hex[:12]}"
    save_path = os.path.join(UPLOAD_DIR, f"{source_id}{ext}")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Load ? Chunk ? Embed ? Upsert
    try:
        raw_docs = load_document(save_path)
        chunks = chunk_documents(
            documents=raw_docs,
            document_id=source_id,
            document_name=doc_name,
            url=url or "",
            category=category or "",
        )

        texts = [c.page_content for c in chunks]
        embeddings = embed_texts(texts)

        index = get_pinecone_index()
        delete_vectors_by_source(index, source_id, settings.PINECONE_NAMESPACE)
        upserted = upsert_chunks(index, chunks, embeddings, settings.PINECONE_NAMESPACE)

        # Register document for admin view
        _document_registry[source_id] = DocumentMeta(
            source_id=source_id,
            document_name=doc_name,
            chunks_count=upserted,
            format=ext.lstrip("."),
            category=category,
            url=url,
        )

        return IngestionResponse(
            status="success",
            document_id=source_id,
            document_name=doc_name,
            chunks_created=len(chunks),
            vectors_upserted=upserted,
        )

    except Exception as e:
        os.remove(save_path)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.get("/registry", response_model=DocumentListResponse)
async def get_registry():
    docs = list(_document_registry.values())
    return DocumentListResponse(documents=docs, total=len(docs))
