import pytest
from langchain_core.documents import Document
from app.retrieval.bm25_indexer import BM25Indexer
from app.retrieval.hybrid_search import reciprocal_rank_fusion
from app.retrieval.cross_encoder_reranker import CrossEncoderReranker


def test_bm25_indexer_keyword_matching():
    indexer = BM25Indexer()
    docs = [
        Document(page_content="Error ERR_AUTH_042 occurred during SAML SSO login handshake.", metadata={"source_id": "d1"}),
        Document(page_content="Annual plans have a 14-day refund window policy.", metadata={"source_id": "d2"}),
        Document(page_content="Stripe credit card payments are supported for Pro tier.", metadata={"source_id": "d3"}),
    ]
    indexer.fit(docs)

    # Exact error code search
    results = indexer.search("ERR_AUTH_042", top_k=2)
    assert len(results) >= 1
    assert results[0][0].metadata["source_id"] == "d1"
    assert results[0][1] > 0.0


def test_reciprocal_rank_fusion_blending():
    doc1 = Document(page_content="Doc 1", metadata={"source_id": "d1", "section": "s1", "chunk_index": 0})
    doc2 = Document(page_content="Doc 2", metadata={"source_id": "d2", "section": "s2", "chunk_index": 0})

    dense = [(doc1, 0.95), (doc2, 0.80)]
    sparse = [(doc2, 4.5), (doc1, 1.2)]

    # Alpha 0.5 balanced fusion
    fused = reciprocal_rank_fusion(dense, sparse, k=60, alpha=0.5, top_n=2)
    assert len(fused) == 2
    assert fused[0][1] > 0.0
    assert "dense_rank" in fused[0][2]
    assert "sparse_rank" in fused[0][2]


@pytest.mark.asyncio
async def test_cross_encoder_reranker_fallback():
    reranker = CrossEncoderReranker()
    doc1 = Document(page_content="Billing refund policies and payment cycles.", metadata={})
    doc2 = Document(page_content="Unrelated database replication architecture.", metadata={})

    reranked = await reranker.rerank("What is the refund policy?", [doc2, doc1], top_k=2)
    assert len(reranked) == 2
    assert reranked[0][0].page_content == doc1.page_content