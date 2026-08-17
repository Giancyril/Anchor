from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.sync.web_crawler import web_crawler
from app.sync.diff_engine import diff_engine
from app.sync.version_store import version_store, DocumentVersion
from app.sync.sync_scheduler import sync_scheduler, SyncJob

router = APIRouter(prefix="/sync", tags=["Knowledge Base Sync & Diffs"])

class CrawlRequest(BaseModel):
    url: str

class DiffRequest(BaseModel):
    old_content: str
    new_content: str

class CreateJobRequest(BaseModel):
    target_url: str
    schedule: str = "daily"

@router.post("/crawl")
async def crawl_web_doc(payload: CrawlRequest):
    doc = await web_crawler.crawl_url(payload.url)
    if not doc:
        raise HTTPException(status_code=400, detail=f"Could not crawl or parse content from {payload.url}")
    return {
        "url": payload.url,
        "title": doc.metadata.get("document_name"),
        "preview": doc.page_content[:400],
        "total_chars": len(doc.page_content),
    }

@router.post("/diff")
async def compute_content_diff(payload: DiffRequest):
    unified = diff_engine.generate_unified_diff(payload.old_content, payload.new_content)
    return {
        "unified_diff": unified,
        "chars_added": max(0, len(payload.new_content) - len(payload.old_content)),
        "chars_removed": max(0, len(payload.old_content) - len(payload.new_content)),
    }

@router.get("/jobs", response_model=List[SyncJob])
async def list_sync_jobs():
    return sync_scheduler.list_jobs()

@router.post("/jobs", response_model=SyncJob)
async def create_sync_job(payload: CreateJobRequest):
    return sync_scheduler.register_job(payload.target_url, payload.schedule)

@router.post("/jobs/{job_id}/run")
async def trigger_sync_job(job_id: str):
    job = sync_scheduler.trigger_job_run(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"status": "success", "job": job}

@router.get("/versions/{source_id}", response_model=List[DocumentVersion])
async def get_document_versions(source_id: str):
    return version_store.get_versions(source_id)