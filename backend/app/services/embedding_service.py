from typing import List
from langchain_openai import OpenAIEmbeddings
from app.config import settings


def get_embeddings() -> OpenAIEmbeddings:
    """Return the configured OpenAI embedding model."""
    return OpenAIEmbeddings(
        model=settings.EMBEDDING_MODEL,
        openai_api_key=settings.OPENAI_API_KEY,
    )


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a list of strings in batches and return float vectors."""
    embeddings_model = get_embeddings()
    return embeddings_model.embed_documents(texts)


def embed_query(query: str) -> List[float]:
    """Embed a single query string for similarity search."""
    embeddings_model = get_embeddings()
    return embeddings_model.embed_query(query)
