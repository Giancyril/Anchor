from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class HybridSearchRequest(BaseModel):
    query: str
    alpha: float = 0.5  # 1.0 = 100% dense, 0.0 = 100% sparse
    top_k: int = 4
    enable_rerank: bool = True
    decompose: bool = False

class SearchResultItem(BaseModel):
    document_name: str
    section: str
    url: Optional[str] = None
    content: str
    final_score: float
    breakdown: Dict[str, Any]

class HybridSearchResponse(BaseModel):
    query: str
    sub_queries: List[str]
    alpha: float
    results_count: int
    results: List[SearchResultItem]