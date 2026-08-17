import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class LiveQueueItem(BaseModel):
    queue_id: str
    session_id: str
    customer_name: str
    priority_score: float
    reason: str
    wait_time_seconds: float
    status: str  # "waiting" | "in_progress" | "resolved"

class LiveTriageQueue:
    """
    Priority triage queue ranking waiting support requests by urgency, churn risk, and sentiment.
    """
    def __init__(self):
        self._items: Dict[str, LiveQueueItem] = {}

    def enqueue(
        self,
        session_id: str,
        customer_name: str,
        intent: str,
        sentiment: str,
        num_turns: int = 1,
    ) -> LiveQueueItem:
        qid = f"Q-{session_id[:6].upper()}"
        
        # Priority formula (Higher = more urgent)
        score = 10.0
        if "Churn" in intent:
            score += 40.0
        if "Frustrated" in sentiment or "Urgent" in sentiment:
            score += 30.0
        if "Billing" in intent or "Security" in intent:
            score += 20.0
        score += min(20.0, num_turns * 2.0)

        reason = f"Intent: {intent} | Sentiment: {sentiment}"
        item = LiveQueueItem(
            queue_id=qid,
            session_id=session_id,
            customer_name=customer_name,
            priority_score=score,
            reason=reason,
            wait_time_seconds=0.0,
            status="waiting",
        )
        self._items[qid] = item
        return item

    def list_queue(self) -> List[LiveQueueItem]:
        # Return sorted by priority_score descending
        return sorted(self._items.values(), key=lambda i: i.priority_score, reverse=True)

    def assign_agent(self, queue_id: str) -> Optional[LiveQueueItem]:
        item = self._items.get(queue_id)
        if item:
            item.status = "in_progress"
        return item

live_queue = LiveTriageQueue()