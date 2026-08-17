import time
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SupportTicket(BaseModel):
    ticket_id: str
    session_id: str
    title: str
    customer_query: str
    intent: str
    sentiment: str
    priority: str  # "Low" | "Medium" | "High" | "Urgent"
    status: str    # "open" | "assigned" | "resolved"
    created_at: float
    transcript: List[Dict[str, str]]
    assigned_agent: Optional[str] = None
    resolution_notes: Optional[str] = None

class TicketDispatcher:
    """
    Creates and stores human support escalation tickets from failed RAG queries or user requests.
    """
    def __init__(self):
        self._tickets: Dict[str, SupportTicket] = {}

    def create_ticket(
        self,
        session_id: str,
        customer_query: str,
        intent: str = "General Inquiry",
        sentiment: str = "Neutral",
        transcript: Optional[List[Dict[str, str]]] = None,
    ) -> SupportTicket:
        tid = f"TICK-{uuid.uuid4().hex[:6].upper()}"
        
        # Determine priority dynamically based on sentiment and intent
        if "Frustrated" in sentiment or "Urgent" in sentiment or "Churn" in intent:
            priority = "Urgent"
        elif "Billing" in intent or "Security" in intent:
            priority = "High"
        elif "Technical" in intent:
            priority = "Medium"
        else:
            priority = "Low"

        ticket = SupportTicket(
            ticket_id=tid,
            session_id=session_id,
            title=f"[{priority}] {intent}: {customer_query[:50]}...",
            customer_query=customer_query,
            intent=intent,
            sentiment=sentiment,
            priority=priority,
            status="open",
            created_at=time.time(),
            transcript=transcript or [],
        )
        self._tickets[tid] = ticket
        return ticket

    def list_tickets(self, status: Optional[str] = None) -> List[SupportTicket]:
        all_t = list(self._tickets.values())
        if status:
            return [t for t in all_t if t.status == status]
        return sorted(all_t, key=lambda t: t.created_at, reverse=True)

    def resolve_ticket(self, ticket_id: str, notes: str = "", agent: str = "Agent #1") -> Optional[SupportTicket]:
        t = self._tickets.get(ticket_id)
        if t:
            t.status = "resolved"
            t.resolution_notes = notes
            t.assigned_agent = agent
        return t

ticket_dispatcher = TicketDispatcher()