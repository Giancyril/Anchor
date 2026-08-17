from typing import List, Dict, Tuple, Any
from langchain_core.documents import Document

def reciprocal_rank_fusion(
    dense_results: List[Tuple[Document, float]],
    sparse_results: List[Tuple[Document, float]],
    k: int = 60,
    alpha: float = 0.5,
    top_n: int = 4,
) -> List[Tuple[Document, float, Dict[str, Any]]]:
    """
    Combines dense vector search results and sparse BM25 results using Reciprocal Rank Fusion (RRF).

    Args:
        dense_results: Ordered list of (Document, cosine_similarity) from Pinecone.
        sparse_results: Ordered list of (Document, bm25_score) from BM25.
        k: Smoothing constant to penalize low ranks (default 60).
        alpha: Weight for dense results (1.0 = 100% dense, 0.0 = 100% sparse).
        top_n: Final number of blended results to return.

    Returns:
        List of (Document, rrf_score, debug_breakdown_dict) sorted descending.
    """
    scores: Dict[str, float] = {}
    doc_map: Dict[str, Document] = {}
    dense_ranks: Dict[str, int] = {}
    sparse_ranks: Dict[str, int] = {}
    dense_raw_scores: Dict[str, float] = {}
    sparse_raw_scores: Dict[str, float] = {}

    def get_doc_key(doc: Document) -> str:
        meta = doc.metadata
        return f"{meta.get('source_id', '')}::{meta.get('section', '')}::{meta.get('chunk_index', 0)}"

    # Process Dense Results
    for rank, (doc, raw_score) in enumerate(dense_results, start=1):
        key = get_doc_key(doc)
        doc_map[key] = doc
        dense_ranks[key] = rank
        dense_raw_scores[key] = raw_score
        scores[key] = scores.get(key, 0.0) + (alpha * (1.0 / (k + rank)))

    # Process Sparse Results
    sparse_weight = 1.0 - alpha
    for rank, (doc, raw_score) in enumerate(sparse_results, start=1):
        key = get_doc_key(doc)
        doc_map[key] = doc
        sparse_ranks[key] = rank
        sparse_raw_scores[key] = raw_score
        scores[key] = scores.get(key, 0.0) + (sparse_weight * (1.0 / (k + rank)))

    # Sort documents by final combined RRF score
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    fused_results = []
    for key, combined_score in sorted_items[:top_n]:
        breakdown = {
            "dense_rank": dense_ranks.get(key),
            "dense_score": dense_raw_scores.get(key, 0.0),
            "sparse_rank": sparse_ranks.get(key),
            "sparse_score": sparse_raw_scores.get(key, 0.0),
            "rrf_score": combined_score,
        }
        fused_results.append((doc_map[key], combined_score, breakdown))

    return fused_results