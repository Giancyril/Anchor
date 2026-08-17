import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.chains.rag_chain import run_rag_chain
from app.memory.session_store import session_store
from app.memory.query_rewriter import query_rewriter
from app.memory.intent_classifier import intent_classifier
from app.memory.sentiment_tracker import sentiment_tracker

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    session_id = payload.session_id or str(uuid.uuid4())

    # 1. Analyze sentiment & intent
    sent_res = sentiment_tracker.analyze(payload.question)
    user_intent = await intent_classifier.classify(payload.question)

    # 2. Extract conversation context & rewrite query if contextual follow-up
    conv_context = session_store.get_conversation_context(session_id, last_n=4)
    search_query = payload.question
    if conv_context:
        search_query = await query_rewriter.rewrite(payload.question, conv_context)

    # 3. Add user message to session store
    session_store.add_message(
        session_id=session_id,
        role="user",
        content=payload.question,
        intent=user_intent,
        sentiment=sent_res["sentiment"],
    )

    # 4. Build metadata filters
    metadata_filter = {}
    if payload.filters:
        if payload.filters.category:
            metadata_filter["category"] = {"$eq": payload.filters.category}
        if payload.filters.product_line:
            metadata_filter["product_line"] = {"$eq": payload.filters.product_line}

    # 5. Run RAG chain with rewritten query
    response = await run_rag_chain(
        question=search_query,
        namespace="default",
        metadata_filter=metadata_filter if metadata_filter else None,
    )

    # 6. Add assistant response to session store
    session_store.add_message(
        session_id=session_id,
        role="assistant",
        content=response.answer,
        confidence=response.confidence,
        intent=user_intent,
    )

    response.session_id = session_id
    return response