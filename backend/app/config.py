from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "AI Customer Support Agent"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # LLM & Embeddings
    OPENAI_API_KEY: str = ""
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    EMBEDDING_DIMENSION: int = 1536
    LLM_MODEL: str = "gpt-4o-mini"

    # Pinecone
    PINECONE_API_KEY: str = ""
    PINECONE_INDEX_NAME: str = "customer-support-kb"
    PINECONE_NAMESPACE: str = "default"
    PINECONE_ENVIRONMENT: str = "us-east-1"

    # RAG
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 120
    TOP_K: int = 4
    SIMILARITY_THRESHOLD: float = 0.75

    # Escalation
    ESCALATION_EMAIL: str = "support@company.com"


settings = Settings()
