# Anchor v2.0 Enterprise Architecture Guide

This document details the internal design, algorithms, and engineering patterns behind **Anchor v2.0** — an enterprise AI Customer Support Agent with Hybrid RAG, Multi-Turn Contextual Memory, Automated Web Crawling & Diffs, Live Agent Triage (HITL), and RAG Triad Observability.

---

## 1. Five Advanced Architectural Pillars

### Pillar 1: Hybrid Search Engine & Reranking
1. **In-Memory BM25 Sparse Indexer (`app/retrieval/bm25_indexer.py`)**:
   - Implements BM25 Okapi with custom alphanumeric code symbol tokenization to ensure error codes (`ERR_AUTH_042`), product SKUs, and exact phrases score with high precision.
2. **Reciprocal Rank Fusion (`app/retrieval/hybrid_search.py`)**:
   - Blends dense vector search (Pinecone cosine scores) and sparse BM25 scores with configurable $\alpha$ balance parameter ($0.0 \le \alpha \le 1.0$):
     $$RRF\_Score(d) = \sum_{m \in M} \frac{w_m}{k + rank_m(d)}$$
3. **Cross-Encoder Reranking (`app/retrieval/cross_encoder_reranker.py`)**:
   - Two-stage retrieval reranker computing granular query-document relevance logits to eliminate false positives.
4. **Query Decomposition (`app/retrieval/query_decomposer.py`)**:
   - Breaks complex multi-part questions into atomic sub-queries.

---

### Pillar 2: Contextual Multi-Turn Memory & Intent Analytics
1. **Sliding Window Session Store (`app/memory/session_store.py`)**:
   - Manages conversational history windows and turn tracking per customer session.
2. **LLM Query Reformulation (`app/memory/query_rewriter.py`)**:
   - Transforms ambiguous follow-up questions ("Can I upgrade that?", "How much is the other one?") into self-contained standalone search queries.
3. **Zero-Shot Intent Classifier (`app/memory/intent_classifier.py`)**:
   - Categorizes turns into 7 standard taxonomies (Billing, Technical, Security, Pricing, Onboarding, Churn Risk, General).
4. **Sentiment & Frustration Tracker (`app/memory/sentiment_tracker.py`)**:
   - Real-time customer sentiment scoring and frustration dip detection.

---

### Pillar 3: Automated KB Sync & Chunk-Level Diff Engine
1. **Web & Sitemap Crawler (`app/sync/web_crawler.py`)**:
   - Recursive crawler with clean article text extraction (stripping nav, footer, ads, and scripts).
2. **Chunk-Level Diff Engine (`app/sync/diff_engine.py`)**:
   - Identifies added, modified, and removed sections between document revisions.
3. **Version & Checksum Store (`app/sync/version_store.py`)**:
   - Computes SHA-256 checksums per revision for immutable document change tracking and rollback support.
4. **Sync Scheduler (`app/sync/sync_scheduler.py`)**:
   - Background periodic sync worker managing hourly, daily, and weekly crawl schedules.

---

### Pillar 4: Live Human Escalation & Priority Triage (HITL)
1. **Support Ticket Dispatcher (`app/escalation/ticket_dispatcher.py`)**:
   - Automatically generates structured escalation tickets with chat transcripts, extracted intent, and confidence diagnostics.
2. **HMAC Webhook Dispatcher (`app/escalation/webhook_notifier.py`)**:
   - Cryptographically signs JSON payloads with `HMAC-SHA256` for Zendesk, Slack, Discord, and CRM webhooks.
3. **Live Triage Queue (`app/escalation/live_queue.py`)**:
   - Priority queue formula weighting churn risk ($+40$), user frustration ($+30$), and message duration.
4. **Canned AI Response Suggester (`app/escalation/canned_responses.py`)**:
   - Generates grounded, empathetic response drafts for human support agents.

---

### Pillar 5: RAG Triad Telemetry, Cost Tracker & Guardrails
1. **RAG Triad Evaluator (`app/telemetry/rag_triad.py`)**:
   - Computes Context Relevance, Faithfulness (Groundedness), and Answer Relevance ($0.0-1.0$).
2. **Multi-Model Cost Tracker (`app/telemetry/cost_tracker.py`)**:
   - Real-time token accounting for OpenAI embeddings and generation models.
3. **PII Sanitizer & Prompt Injection Guardrails (`app/telemetry/guardrails.py`)**:
   - Detects and redacts SSNs, credit cards, emails, and blocks jailbreak attempts.
4. **Telemetry Store (`app/telemetry/metrics_store.py`)**:
   - Aggregated metrics time-series store tracking p50/p95 latency and resolution rates.