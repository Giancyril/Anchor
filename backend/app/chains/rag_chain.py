from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.config import settings
from app.chains.citation_parser import parse_citations
from app.schemas.chat import ChatResponse, CitationSource
from app.services.confidence_service import check_confidence
from app.services.embedding_service import embed_query
from app.services.pinecone_service import get_pinecone_index


SYSTEM_PROMPT = """You are a helpful AI Customer Support Assistant. Your role is to answer customer questions accurately using ONLY the numbered knowledge base excerpts provided below.

Rules you must follow:
1. For every factual claim or piece of information you state, append the citation number inline immediately after it, e.g.: "Refunds are processed within 3 business days [1]."
2. You may cite multiple sources in one sentence, e.g.: "Annual plans are refundable [1] and upgrades take effect immediately [2]."
3. Do NOT make any statements that cannot be directly supported by the provided excerpts.
4. If the excerpts do not contain enough information to answer the question, respond ONLY with: "I'm unable to find this information in our documentation. Please contact our support team for further assistance."
5. Be concise, professional, and empathetic in tone.

Knowledge Base Excerpts:
{context}"""

HUMAN_PROMPT = "Customer Question: {question}"


def build_context_string(chunks: List[Document]) -> str:
    """Format retrieved chunks as numbered context for the LLM prompt."""
    parts = []
    for idx, chunk in enumerate(chunks, start=1):
        meta = chunk.metadata
        header = f"[{idx}] (Source: {meta.get('document_name', 'Unknown')} > {meta.get('section', 'General')})"
        parts.append(f"{header}\n{chunk.page_content.strip()}")
    return "\n\n".join(parts)


async def run_rag_chain(
    question: str,
    namespace: str = "default",
    metadata_filter: Optional[Dict[str, Any]] = None,
) -> ChatResponse:
    """
    Full RAG pipeline:
    1. Embed the query
    2. Retrieve top-k chunks from Pinecone
    3. Apply similarity confidence gate (Tier 1)
    4. If confident: build numbered context, run LLM, parse citations
    5. If not confident: return escalation response
    """
    # Step 1: Embed query
    query_vector = embed_query(question)

    # Step 2: Retrieve from Pinecone
    index = get_pinecone_index()
    filter_dict = metadata_filter or {}
    results = index.query(
        vector=query_vector,
        top_k=settings.TOP_K,
        include_metadata=True,
        namespace=namespace,
        filter=filter_dict if filter_dict else None,
    )

    # Convert Pinecone matches to (Document, score) pairs
    scored_chunks = []
    for match in results.matches:
        doc = Document(
            page_content=match.metadata.pop("text", ""),
            metadata=match.metadata,
        )
        scored_chunks.append((doc, match.score))

    # Step 3: Confidence gate (Tier 1)
    should_answer, top_score = check_confidence(scored_chunks)

    if not should_answer:
        return ChatResponse(
            answer=(
                "I'm unable to find specific information about this in our documentation. "
                "Would you like me to connect you with our support team for further assistance?"
            ),
            confidence="low",
            escalated=True,
            sources=[],
        )

    # Step 4: Build context and run LLM
    chunks = [doc for doc, _ in scored_chunks]
    context = build_context_string(chunks)

    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0.0,
        openai_api_key=settings.OPENAI_API_KEY,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])

    chain = prompt | llm | StrOutputParser()
    raw_answer = await chain.ainvoke({"context": context, "question": question})

    # Step 5: Parse citations and resolve to source metadata
    answer_text, sources = parse_citations(raw_answer, chunks)

    # Detect LLM-signaled uncertainty (Tier 2)
    idk_signals = [
        "unable to find",
        "not covered",
        "cannot find",
        "don't have information",
        "no information",
    ]
    llm_uncertain = any(sig in answer_text.lower() for sig in idk_signals)

    return ChatResponse(
        answer=answer_text,
        confidence="low" if llm_uncertain else "high",
        escalated=llm_uncertain,
        sources=sources,
    )
