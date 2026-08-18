from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, chat, documents, ingest, search, sessions, sync, escalation, telemetry


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="AI Customer Support Agent powered by RAG (LangChain + Pinecone + OpenAI)",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers under /api/v1
    prefix = settings.API_V1_PREFIX
    app.include_router(health.router, prefix=prefix)
    app.include_router(chat.router, prefix=prefix)
    app.include_router(documents.router, prefix=prefix)
    app.include_router(ingest.router, prefix=prefix)
    app.include_router(search.router, prefix=prefix)
    app.include_router(sessions.router, prefix=prefix)
    app.include_router(sync.router, prefix=prefix)
    app.include_router(escalation.router, prefix=prefix)
    app.include_router(telemetry.router, prefix=prefix)

    return app


app = create_app()