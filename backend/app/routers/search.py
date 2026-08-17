from fastapi import APIRouter, HTTPException
from app.schemas.search import HybridSearchRequest, HybridSearchResponse, SearchResultItem
from app.retrieval.bm25_indexer import bm25_indexer
from app.retrieval.hybrid_search import reciprocal_rank_fusion
from app.retrieval.cross_encoder_reranker import reranker
from app.retrieval.query_decomposer import query_decomposer
from app.services.embedding_service import embed_query
from app.services.pinecone_service import get_pinecone_index
from langchain_core.documents import Document
from app.config import settings

router = APIRouter(prefix="/search", tags=["Hybrid Search"])

@router.post("/hybrid", response_model=HybridSearchResponse)
async def hybrid_search(payload: HybridSearchRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty.")

    sub_queries = [payload.query]
    if payload.decompose:
        sub_queries = await query_decomposer.decompose(payload.query)

    # 1. Sparse BM25 Search
    sparse_matches = bm25_indexer.search(payload.query, top_k=payload.top_k * 2)

    # 2. Dense Vector Search
    dense_matches = []
    try:
        query_vector = embed_query(payload.query)
        index = get_pinecone_index()
        dense_res = index.query(
            vector=query_vector,
            top_k=payload.top_k * 2,
            include_metadata=True,
            namespace=settings.PINECONE_NAMESPACE,
        )
        for m in dense_res.matches:
            doc = Document(page_content=m.metadata.pop("text", ""), metadata=m.metadata)
            dense_matches.append((doc, m.score))
    except Exception:
        # If Pinecone is offline/mocked, fallback to BM25
        pass

    # 3. Reciprocal Rank Fusion
    fused = reciprocal_rank_fusion(
        dense_results=dense_matches,
        sparse_results=sparse_matches,
        alpha=payload.alpha,
        top_n=payload.top_k * 2,
    )

    candidate_docs = [doc for doc, _, _ in fused]
    
    # 4. Optional Two-Stage Cross-Encoder Reranking
    if payload.enable_rerank and candidate_docs:
        reranked = await reranker.rerank(payload.query, candidate_docs, top_k=payload.top_k)
        final_items = []
        for doc, score in reranked:
            meta = doc.metadata
            final_items.append(SearchResultItem(
                document_name=meta.get("document_name", "Unknown"),
                section=meta.get("section", "General"),
                url=meta.get("url"),
                content=doc.page_content[:350],
                final_score=round(score, 4),
                breakdown={"reranked_score": score},
            ))
    else:
        final_items = []
        for doc, score, breakdown in fused[:payload.top_k]:
            meta = doc.metadata
            final_items.append(SearchResultItem(
                document_name=meta.get("document_name", "Unknown"),
                section=meta.get("section", "General"),
                url=meta.get("url"),
                content=doc.page_content[:350],
                final_score=round(score, 4),
                breakdown=breakdown,
            ))

    return HybridSearchResponse(
        query=payload.query,
        sub_queries=sub_queries,
        alpha=payload.alpha,
        results_count=len(final_items),
        results=final_items,
    )