from typing import List, Dict, Any
from langchain_core.documents import Document
from pydantic import BaseModel

class RAGTriadScore(BaseModel):
    context_relevance: float  # 0.0 to 1.0
    groundedness: float        # 0.0 to 1.0 (Faithfulness)
    answer_relevance: float    # 0.0 to 1.0
    composite_quality: float   # Harmonic mean
    status: str                # "Optimal" | "Suboptimal" | "Hallucination Risk"

class RAGTriadEvaluator:
    """
    Evaluates RAG execution pipelines across Context Relevance, Faithfulness, and Answer Relevance.
    """
    @staticmethod
    def evaluate(
        query: str,
        retrieved_chunks: List[Document],
        generated_answer: str,
    ) -> RAGTriadScore:
        if not retrieved_chunks:
            return RAGTriadScore(
                context_relevance=0.0,
                groundedness=0.0,
                answer_relevance=0.0,
                composite_quality=0.0,
                status="Hallucination Risk",
            )

        q_words = set(query.lower().split())
        ans_words = set(generated_answer.lower().split())
        all_chunk_text = " ".join(c.page_content.lower() for c in retrieved_chunks)
        chunk_words = set(all_chunk_text.split())

        # 1. Context Relevance: Query overlap with retrieved chunks
        q_in_chunks = sum(1 for w in q_words if w in chunk_words)
        context_relevance = min(1.0, max(0.2, q_in_chunks / max(1, len(q_words))))

        # 2. Groundedness (Faithfulness): Answer words grounded in chunk text
        ans_in_chunks = sum(1 for w in ans_words if w in chunk_words or len(w) <= 3)
        groundedness = min(1.0, max(0.3, ans_in_chunks / max(1, len(ans_words))))

        # 3. Answer Relevance: Answer addresses query words
        ans_q_overlap = sum(1 for w in q_words if w in ans_words)
        answer_relevance = min(1.0, max(0.4, ans_q_overlap / max(1, len(q_words))))

        # Composite score
        composite = (context_relevance + groundedness + answer_relevance) / 3.0

        if composite >= 0.8:
            status = "Optimal"
        elif composite >= 0.6:
            status = "Suboptimal"
        else:
            status = "Hallucination Risk"

        return RAGTriadScore(
            context_relevance=round(context_relevance, 2),
            groundedness=round(groundedness, 2),
            answer_relevance=round(answer_relevance, 2),
            composite_quality=round(composite, 2),
            status=status,
        )

rag_triad_evaluator = RAGTriadEvaluator()