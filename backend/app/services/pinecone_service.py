import uuid
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from app.config import settings
from app.ingestion.hasher import generate_vector_id


def get_pinecone_index():
    """Initialize and return a Pinecone index client."""
    from pinecone import Pinecone, ServerlessSpec
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    existing = [idx.name for idx in pc.list_indexes()]
    if settings.PINECONE_INDEX_NAME not in existing:
        pc.create_index(
            name=settings.PINECONE_INDEX_NAME,
            dimension=settings.EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=settings.PINECONE_ENVIRONMENT),
        )

    return pc.Index(settings.PINECONE_INDEX_NAME)


def delete_vectors_by_source(index, source_id: str, namespace: str):
    """
    Delete all existing vectors for a document before re-ingesting.
    Prevents orphaned stale chunks when a document shrinks or restructures.
    """
    try:
        # Pinecone supports delete by metadata filter on non-serverless;
        # for serverless we query + delete by IDs in batches.
        results = index.query(
            vector=[0.0] * settings.EMBEDDING_DIMENSION,
            top_k=10000,
            filter={"source_id": {"": source_id}},
            include_metadata=False,
            namespace=namespace,
        )
        ids = [m.id for m in results.matches]
        if ids:
            index.delete(ids=ids, namespace=namespace)
        return len(ids)
    except Exception:
        return 0


def upsert_chunks(
    index,
    chunks: List[Document],
    embeddings: List[List[float]],
    namespace: str,
) -> int:
    """
    Batch upsert chunks with deterministic vector IDs derived from metadata.
    Returns the number of vectors upserted.
    """
    vectors = []
    for chunk, embedding in zip(chunks, embeddings):
        meta = chunk.metadata
        vector_id = generate_vector_id(
            document_id=meta["source_id"],
            section=meta["section"],
            chunk_index=meta["chunk_index"],
        )
        vectors.append({
            "id": vector_id,
            "values": embedding,
            "metadata": {
                **meta,
                "text": chunk.page_content,
            },
        })

    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i : i + batch_size], namespace=namespace)

    return len(vectors)
