# AI Customer Support Agent

A production-grade, AI-augmented Customer Support Agent that answers customer questions accurately using company documentation via Retrieval-Augmented Generation (RAG). Features deterministic chunk ID hashing, Pinecone serverless vector indexing, Perplexity-style inline citations (`[1]`, `[2]`), confidence similarity score gating (`< 0.75` cutoff), multi-format document ingestion (Markdown, PDF, HTML, TXT), and an automated hallucination evaluation test suite.

---

## Features

### Core Capabilities
- **Strictly Grounded RAG Answers**: Responses are synthesized directly from retrieved knowledge base chunks rather than open-ended model speculation.
- **Perplexity-Style Inline Citations**: Interactive citation markers (`[1]`, `[2]`) rendered adjacent to claims, with popover cards showing source documents, section headings, and excerpt previews.
- **Multi-Tier Confidence & Escalation Gate**: Cosine similarity cutoff (< 0.75) immediately intercepts unanswerable queries before LLM invocation, routing users to support escalation channels.
- **Deterministic Re-Ingestion & Anti-Orphan Cleanup**: Deterministic SHA-256 vector IDs `hash(doc_id + section + chunk_idx)` ensure document updates overwrite existing vectors, with pre-upsert deletion of old document chunks.
- **Multi-Format Ingestion**: Native support for Markdown (`.md`), PDF (`.pdf`), HTML (`.html`), and Plain Text (`.txt`).
- **Knowledge Base Management UI**: Admin dashboard with real-time vector statistics, document listing, and file upload modal.
- **Automated Hallucination Regression Eval Suite**: Dedicated test suite asserting grounded factual answers on known documents and strict "I don't know" behavior on deliberate out-of-domain queries.

---

## System Architecture

```
                                    +-----------------------------------------+
                                    |         User Ingestion Trigger          |
                                    |    (Markdown / PDF / HTML / Text)       |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |         LangChain Loaders & Chunker     |
                                    |        (600 chars / 120 overlap)        |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |      Deterministic SHA-256 Hasher       |
                                    |      hash(doc_id + section + idx)       |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |      OpenAI Embeddings (1536-dim)       |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |         Pinecone Vector Index           |
                                    |        (Serverless / Cosine)            |
                                    +--------------------+--------------------+
                                                         ^
                                                         | (Similarity Search)
+------------------------+          +--------------------+--------------------+          +------------------------+
|   Customer Chat UI     | <------> |     FastAPI RAG Orchestrator /chat      | <------> |  OpenAI GPT-4o-mini    |
| (Inline Citations [1]) |          |  (Hard Similarity Gate: Score >= 0.75)  |          | (Strict Numbered QA)   |
+------------------------+          +-----------------------------------------+          +------------------------+
```

---

## Project Structure

```
AI Customer Support Agent/
├── backend/
│   ├── app/
│   │   ├── chains/
│   │   │   ├── citation_parser.py    # Regex extractor mapping [n] to source metadata
│   │   │   └── rag_chain.py          # LangChain LCEL retrieval chain & grounded prompt
│   │   ├── ingestion/
│   │   │   ├── chunker.py            # RecursiveCharacterTextSplitter with metadata
│   │   │   ├── hasher.py             # Deterministic SHA-256 vector ID generation
│   │   │   └── loader.py             # Multi-format document loader dispatcher
│   │   ├── routers/
│   │   │   ├── chat.py               # POST /api/v1/chat
│   │   │   ├── documents.py          # GET /api/v1/documents
│   │   │   ├── health.py             # GET /api/v1/health
│   │   │   └── ingest.py             # POST /api/v1/ingest
│   │   ├── schemas/
│   │   │   ├── chat.py               # ChatRequest, ChatResponse, CitationSource
│   │   │   └── document.py           # IngestionResponse, DocumentMeta
│   │   ├── services/
│   │   │   ├── confidence_service.py # Tier 1 cosine similarity threshold gate
│   │   │   ├── embedding_service.py  # OpenAI text-embedding-3-small wrapper
│   │   │   └── pinecone_service.py   # Pinecone client, batch upsert & pre-deletion
│   │   ├── config.py                 # Pydantic BaseSettings environment validation
│   │   └── main.py                   # FastAPI app factory & CORS middleware
│   ├── sample_docs/                  # Company documentation (Billing, Security, etc.)
│   ├── tests/
│   │   ├── test_chunker.py           # Ingestion & splitting unit tests
│   │   ├── test_citation_parser.py   # Citation extraction unit tests
│   │   ├── test_confidence_gate.py   # Threshold similarity tests
│   │   ├── test_eval_suite.py        # Grounded QA & hallucination regression eval
│   │   └── test_hasher.py            # Deterministic hash collision tests
│   ├── pytest.ini
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── admin/page.tsx            # Admin Knowledge Base Ingestion view
│   │   ├── globals.css               # Design system tokens & animations
│   │   ├── layout.tsx                # Root layout with Inter typography
│   │   └── page.tsx                  # Customer Support Chat Interface
│   ├── components/
│   │   ├── admin/
│   │   │   ├── DocumentTable.tsx     # Ingested documents list
│   │   │   └── UploadModal.tsx       # Document upload modal with category picker
│   │   ├── chat/
│   │   │   ├── ChatMessage.tsx       # Message bubble with parsed [1] citation chips
│   │   │   ├── CitationChip.tsx      # Popover preview for inline citations
│   │   │   ├── EscalationBanner.tsx  # Fallback banner for low-confidence queries
│   │   │   └── TypingIndicator.tsx   # Staged search animation
│   │   └── Navbar.tsx                # Top navigation bar
│   ├── lib/
│   │   ├── api.ts                    # Typed API client for FastAPI backend
│   │   └── utils.ts                  # ClassName helper utilities
│   ├── package.json
│   └── tailwind.config.ts
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/chat` | Evaluates query against Pinecone, gates by similarity, and synthesizes cited response |
| `POST` | `/api/v1/ingest` | Uploads, chunks, embeds, and upserts a document to Pinecone |
| `GET` | `/api/v1/documents` | Lists all currently indexed documents and vector counts |
| `GET` | `/api/v1/health` | Service health status, model configurations, and index info |

---

## Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Configure your API keys
cp .env.example .env
# Edit .env and supply OPENAI_API_KEY and PINECONE_API_KEY

# Run FastAPI dev server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to access the chat interface, and `http://localhost:3000/admin` to manage documentation.

### 3. Running Automated Tests & Eval Suite
```bash
.\.venv\Scripts\pytest backend/tests/ -v
```