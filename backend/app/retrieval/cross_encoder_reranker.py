from typing import List, Tuple, Dict, Any
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from app.config import settings

class CrossEncoderReranker:
    """
    Two-stage retrieval reranker computing explicit query-document relevance scores (0-10)
    to re-order candidates and discard low-relevance false positives.
    """
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name

    async def rerank(
        self,
        query: str,
        candidates: List[Document],
        top_k: int = 4,
    ) -> List[Tuple[Document, float]]:
        if not candidates:
            return []

        # If LLM API key is not configured or in unit test mode, use deterministic heuristic
        if not settings.OPENAI_API_KEY:
            # Fallback heuristic: exact term overlap ratio
            q_words = set(query.lower().split())
            scored = []
            for doc in candidates:
                d_words = set(doc.page_content.lower().split())
                overlap = len(q_words.intersection(d_words)) / max(1, len(q_words))
                scored.append((doc, float(overlap)))
            scored.sort(key=lambda x: x[1], reverse=True)
            return scored[:top_k]

        llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.0,
            openai_api_key=settings.OPENAI_API_KEY,
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert search reranker. Given a customer support question and a candidate document excerpt, rate how relevant and useful the excerpt is for answering the question on a scale from 0.0 (completely irrelevant) to 10.0 (directly answers the question). Output ONLY a single floating-point number."),
            ("human", "Question: {query}\n\nDocument Excerpt:\n{content}\n\nRelevance Score (0.0 to 10.0):"),
        ])

        chain = prompt | llm | StrOutputParser()

        scored_results: List[Tuple[Document, float]] = []
        for doc in candidates:
            try:
                raw_score = await chain.ainvoke({"query": query, "content": doc.page_content[:600]})
                score = float(raw_score.strip().split()[0])
            except Exception:
                score = 5.0
            scored_results.append((doc, score))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]

reranker = CrossEncoderReranker()