from fastapi import APIRouter
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": "openai",
        "embedding_model": settings.EMBEDDING_MODEL,
        "pinecone_index": settings.PINECONE_INDEX_NAME,
    }
