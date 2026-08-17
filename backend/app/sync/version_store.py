import time
import hashlib
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class DocumentVersion(BaseModel):
    version_id: int
    source_id: str
    document_name: str
    checksum: str
    timestamp: float
    chunk_count: int
    change_summary: str
    raw_content: str

class DocumentVersionStore:
    """
    Tracks revision histories and checksum snapshots for ingested documents.
    """
    def __init__(self):
        # source_id -> list of DocumentVersion
        self._history: Dict[str, List[DocumentVersion]] = {}

    @staticmethod
    def compute_checksum(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

    def record_version(
        self,
        source_id: str,
        document_name: str,
        raw_content: str,
        chunk_count: int,
        change_summary: str = "Initial Ingestion",
    ) -> DocumentVersion:
        checksum = self.compute_checksum(raw_content)
        if source_id not in self._history:
            self._history[source_id] = []

        v_num = len(self._history[source_id]) + 1
        ver = DocumentVersion(
            version_id=v_num,
            source_id=source_id,
            document_name=document_name,
            checksum=checksum,
            timestamp=time.time(),
            chunk_count=chunk_count,
            change_summary=change_summary,
            raw_content=raw_content,
        )
        self._history[source_id].append(ver)
        return ver

    def get_versions(self, source_id: str) -> List[DocumentVersion]:
        return self._history.get(source_id, [])

    def get_latest(self, source_id: str) -> Optional[DocumentVersion]:
        vers = self._history.get(source_id)
        return vers[-1] if vers else None

version_store = DocumentVersionStore()