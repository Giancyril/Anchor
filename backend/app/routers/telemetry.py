from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.telemetry.rag_triad import rag_triad_evaluator, RAGTriadScore
from app.telemetry.cost_tracker import cost_tracker
from app.telemetry.guardrails import safety_guardrails
from app.telemetry.metrics_store import metrics_store
from langchain_core.documents import Document

router = APIRouter(prefix="/telemetry", tags=["Telemetry & Observability"])

class EvaluateTriadRequest(BaseModel):
    query: str
    generated_answer: str
    chunk_contents: List[str]

class SanitizeRequest(BaseModel):
    text: str

@router.get("/metrics")
async def get_performance_metrics():
    return metrics_store.get_summary()

@router.get("/costs")
async def get_cost_summary():
    return cost_tracker.get_summary()

@router.post("/rag-triad", response_model=RAGTriadScore)
async def evaluate_rag_triad(payload: EvaluateTriadRequest):
    docs = [Document(page_content=c, metadata={}) for c in payload.chunk_contents]
    return rag_triad_evaluator.evaluate(
        query=payload.query,
        retrieved_chunks=docs,
        generated_answer=payload.generated_answer,
    )

@router.post("/guardrails/sanitize")
async def sanitize_message(payload: SanitizeRequest):
    sanitized, redacted = safety_guardrails.sanitize_text(payload.text)
    inj_check = safety_guardrails.check_prompt_injection(payload.text)
    return {
        "original": payload.text,
        "sanitized": sanitized,
        "redacted_types": redacted,
        "injection_check": inj_check,
    }