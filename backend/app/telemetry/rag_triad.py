import re
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
    def _tokenize(text: str) -> set[str]:
        words = re.findall(r"\b[a-zA-Z0-9_-]+\b", text.lower())
        stopwords = {"what", "is", "the", "for", "a", "an", "in", "of", "and", "or", "to", "how", "do", "i"}
        filtered = {w for w in words if w not in stopwords and len(w) > 1}
        return filtered if filtered else set(words)

    def evaluate(
        self,
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

        q_words = self._tokenize(query)
        ans_words = self._tokenize(generated_answer)
        all_chunk_text = " ".join(c.page_content for c in retrieved_chunks)
        chunk_words = self._tokenize(all_chunk_text)

        # 1. Context Relevance: Content words from query present in retrieved chunks
        q_in_chunks = sum(1 for w in q_words if w in chunk_words)
        context_relevance = q_in_chunks / max(1, len(q_words))

        # 2. Groundedness (Faithfulness): Answer tokens supported by chunk text
        ans_in_chunks = sum(1 for w in ans_words if w in chunk_words)
        groundedness = ans_in_chunks / max(1, len(ans_words))

        # 3. Answer Relevance: Answer addresses core query entities
        ans_q_overlap = sum(1 for w in q_words if w in ans_words)
        answer_relevance = ans_q_overlap / max(1, len(q_words))

        # Composite score
        composite = (context_relevance + groundedness + answer_relevance) / 3.0

        if composite >= 0.7:
            status = "Optimal"
        elif composite >= 0.4:
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