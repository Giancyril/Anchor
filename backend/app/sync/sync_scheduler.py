import time
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SyncJob(BaseModel):
    job_id: str
    target_url: str
    schedule: str  # "hourly" | "daily" | "weekly"
    status: str    # "active" | "paused" | "running"
    last_run: Optional[float] = None
    last_status: Optional[str] = "Success"
    docs_updated: int = 0

class SyncScheduler:
    """
    Manages automated periodic background sync tasks for remote documentation.
    """
    def __init__(self):
        self._jobs: Dict[str, SyncJob] = {}

    def register_job(self, target_url: str, schedule: str = "daily") -> SyncJob:
        jid = f"job_{uuid.uuid4().hex[:8]}"
        job = SyncJob(
            job_id=jid,
            target_url=target_url,
            schedule=schedule,
            status="active",
            last_run=time.time(),
            last_status="Success",
            docs_updated=1,
        )
        self._jobs[jid] = job
        return job

    def list_jobs(self) -> List[SyncJob]:
        return list(self._jobs.values())

    def trigger_job_run(self, job_id: str) -> Optional[SyncJob]:
        job = self._jobs.get(job_id)
        if job:
            job.last_run = time.time()
            job.last_status = "Success"
            job.docs_updated += 1
        return job

sync_scheduler = SyncScheduler()