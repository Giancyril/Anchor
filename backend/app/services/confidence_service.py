from typing import List, Tuple
from app.config import settings


def check_confidence(scored_results: List[Tuple[any, float]]) -> Tuple[bool, float]:
    """
    Tier 1 hard similarity gate.

    Args:
        scored_results: List of (Document, score) tuples from Pinecone similarity search.

    Returns:
        (should_answer, top_score)
        - should_answer=False means bypass LLM and return escalation response.
        - should_answer=True means proceed to RAG chain.
    """
    if not scored_results:
        return False, 0.0

    top_score = scored_results[0][1]
    return top_score >= settings.SIMILARITY_THRESHOLD, top_score
