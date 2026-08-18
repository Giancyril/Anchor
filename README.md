# Anchor (AI Customer Support Agent) — v2.0 Enterprise

A production-grade, AI-augmented Customer Support Agent that answers customer questions accurately using company documentation via Retrieval-Augmented Generation (RAG).

Features Hybrid BM25 + Pinecone Dense Search, Cross-Encoder Reranking, Multi-Turn Contextual Query Rewriting, Real-Time Intent & Sentiment Analytics, Automated Web Crawling & Semantic Diffs, Live Agent Triage & HMAC Webhook Dispatching, Perplexity-Style Inline Citations (`[1]`, `[2]`), and RAG Triad Observability Guardrails.

---

## Key Features

### 1. Hybrid Search & Reranking Engine
- **Dense + Sparse Fusion**: Blends Pinecone cosine similarity vectors with in-memory BM25 sparse keyword indices using Reciprocal Rank Fusion (RRF).
- **Two-Stage Cross-Encoder Reranker**: Computes fine-grained query-document relevance logits to eliminate false positives.
- **Query Decomposition**: Decomposes complex multi-part questions into atomic sub-queries.
- **Retrieval Inspector UI**: Interactive playground to tune $\alpha$ weighting and inspect rank breakdowns.

### 2. Contextual Multi-Turn Memory & Intent Analytics
- **Sliding Window History**: 10-turn sliding session memory managing multi-turn conversations.
- **LLM Query Reformulation**: Resolves pronouns and contextual follow-ups ("Can I upgrade that?") into standalone search queries.
- **Zero-Shot Intent Classifier**: Classifies queries into 7 support taxonomies (Billing, Tech Support, Security, Churn Risk, etc.).
- **Sentiment Dip Analyzer**: Detects customer frustration drop trends in real time.

### 3. Automated Knowledge Base Sync & Diff Engine
- **Web & Sitemap Crawler**: Recursively parses remote documentation pages, stripping boilerplate HTML.
- **Chunk-Level Semantic Differ**: Highlights exact added, modified, and removed sections between document revisions.
- **Immutable Version History**: Tracks SHA-256 checksums per revision.
- **Sync Scheduler**: Configurable cron-based background scrapers with execution logs.

### 4. Live Human Escalation & Priority Triage (HITL)
- **Automated Ticket Dispatcher**: Creates structured support tickets with full conversation transcripts.
- **HMAC-SHA256 Signed Webhooks**: Dispatches verified events to Zendesk, Slack, Discord, and CRMs.
- **Priority Triage Queue**: Composite formula weighting churn risk, frustration score, and conversation turns.
- **Smart Canned AI Replies**: Generates grounded response drafts for human support agents.

### 5. RAG Triad Observability & Guardrails
- **RAG Triad Evaluator**: Measures Context Relevance, Faithfulness (Groundedness), and Answer Relevance ($0.0-1.0$).
- **Multi-Model Cost Tracker**: Real-time token consumption and USD expense tracking.
- **PII Redaction Guardrails**: Automatically masks SSNs, credit cards, emails, and blocks jailbreak injections.
- **Telemetry Store**: p50/p95 latency metrics and resolution rate analytics.

---

## System Architecture

```
                                    +-----------------------------------------+
                                    |         User Ingestion Trigger          |
                                    |    (Markdown / PDF / HTML / Web URL)    |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |      Chunker & Deterministic Hasher     |
                                    |       hash(doc_id + sec + chunk_idx)    |
                                    +--------------------+--------------------+
                                                         |
                                     +-------------------+-------------------+
                                     |                                       |
                                     v                                       v
                        +-------------------------+             +-------------------------+
                        |  Pinecone Dense Index   |             |   BM25 Sparse Index     |
                        |   (text-embedding-3)    |             |   (Exact Error/SKU)     |
                        +------------+------------+             +------------+------------+
                                     |                                       |
                                     +-------------------+-------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |    Reciprocal Rank Fusion (RRF α=0.5)   |
                                    +--------------------+--------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |      Cross-Encoder Two-Stage Rerank     |
                                    +--------------------+--------------------+
                                                         |
                                                         v
+------------------------+          +--------------------+--------------------+          +------------------------+
|   Customer Chat UI     | <------> |  FastAPI RAG Orchestrator /api/v1/chat  | <------> |  OpenAI GPT-4o-mini    |
| (Inline Citations [1]) |          |  (Hard Similarity Gate: Score >= 0.75)  |          | (Strict Numbered QA)   |
+------------------------+          +--------------------+--------------------+          +------------------------+
                                                         |
                                                         v
                                    +-----------------------------------------+
                                    |  RAG Triad Telemetry & Guardrails Sanitizer|
                                    +-----------------------------------------+
```

---

## API Endpoints (v2.0)

| Module | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **Chat** | `POST` | `/api/v1/chat` | Main conversational RAG endpoint with memory, citations & confidence gate |
| **Ingestion** | `POST` | `/api/v1/ingest` | Uploads, chunks, embeds and indexes documents |
| **Documents** | `GET` | `/api/v1/documents` | Lists all indexed documents and vector counts |
| **Search** | `POST` | `/api/v1/search/hybrid` | Evaluates hybrid RRF search, BM25 scores, and cross-encoder reranking |
| **Sessions** | `GET` | `/api/v1/sessions` | Lists customer sessions with intent and sentiment history |
| **Sessions** | `GET` | `/api/v1/sessions/{id}/analytics` | Session turn count, intent category, and escalation risk |
| **Sync** | `POST` | `/api/v1/sync/crawl` | Crawls remote documentation page and extracts clean content |
| **Sync** | `POST` | `/api/v1/sync/diff` | Computes unified and semantic chunk diffs between versions |
| **Sync** | `GET` | `/api/v1/sync/jobs` | Lists active recurring sync crawl jobs |
| **Escalation**| `POST` | `/api/v1/escalation/tickets` | Creates human support escalation ticket with transcript |
| **Escalation**| `GET` | `/api/v1/escalation/queue` | Priority triage queue sorted by churn risk and urgency |
| **Escalation**| `GET` | `/api/v1/escalation/canned` | Generates smart grounded response suggestions for agents |
| **Telemetry** | `GET` | `/api/v1/telemetry/metrics` | Returns p50/p95 latency, resolution rate, and query volume |
| **Telemetry** | `GET` | `/api/v1/telemetry/costs` | Returns token usage and USD expenditures across models |
| **Telemetry** | `POST` | `/api/v1/telemetry/guardrails/sanitize` | Redacts sensitive PII and tests prompt injection safety |
| **Health** | `GET` | `/api/v1/health` | Service health status and active configuration |

---

## Automated Verification

### Running Test Suite
```bash
.\.venv\Scripts\pytest backend/tests/ -v
```

All 31 unit, integration, and hallucination regression tests pass cleanly across all 5 pillars:
- `test_chunker.py` (Ingestion & chunking)
- `test_hasher.py` (Deterministic SHA-256 vector IDs)
- `test_citation_parser.py` (Inline `[1]` citation extraction)
- `test_confidence_gate.py` (Similarity thresholding)
- `test_eval_suite.py` (Grounded QA & negative hallucination eval cases)
- `test_hybrid_search.py` (BM25, RRF fusion, Cross-Encoder reranking)
- `test_session_memory.py` (Session store, query rewriter, intent, sentiment)
- `test_sync_engine.py` (Crawler HTML cleaner, semantic diffs, version store)
- `test_escalation.py` (Tickets, HMAC webhook signatures, priority triage queue)
- `test_telemetry.py` (RAG Triad scoring, cost calculations, PII guardrails)

### Running Frontend Build
```bash
cd frontend
npm run build
```