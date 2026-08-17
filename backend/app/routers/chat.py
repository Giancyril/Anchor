import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.chains.rag_chain import run_rag_chain

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    # Build optional metadata filters for scoped retrieval
    metadata_filter = {}
    if payload.filters:
        if payload.filters.category:
            metadata_filter["category"] = {"": payload.filters.category}
        if payload.filters.product_line:
            metadata_filter["product_line"] = {"": payload.filters.product_line}

    response = await run_rag_chain(
        question=payload.question,
        namespace="default",
        metadata_filter=metadata_filter if metadata_filter else None,
    )

    # Attach session_id passthrough
    response.session_id = payload.session_id or str(uuid.uuid4())
    return response
