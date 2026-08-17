from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.escalation.ticket_dispatcher import ticket_dispatcher, SupportTicket
from app.escalation.live_queue import live_queue, LiveQueueItem
from app.escalation.canned_responses import canned_suggester
from app.escalation.webhook_notifier import webhook_notifier

router = APIRouter(prefix="/escalation", tags=["Human Escalation & HITL"])

class CreateTicketRequest(BaseModel):
    session_id: str
    customer_query: str
    intent: Optional[str] = "General Inquiry"
    sentiment: Optional[str] = "Neutral"
    customer_name: Optional[str] = "Anonymous User"

class ResolveTicketRequest(BaseModel):
    resolution_notes: str
    agent_name: Optional[str] = "Support Agent #1"

class DispatchWebhookRequest(BaseModel):
    webhook_url: str
    event_type: str = "ticket.escalated"
    data: Dict[str, Any]

@router.post("/tickets", response_model=SupportTicket)
async def create_ticket(payload: CreateTicketRequest):
    ticket = ticket_dispatcher.create_ticket(
        session_id=payload.session_id,
        customer_query=payload.customer_query,
        intent=payload.intent or "General Inquiry",
        sentiment=payload.sentiment or "Neutral",
    )
    # Also add to live triage queue
    live_queue.enqueue(
        session_id=payload.session_id,
        customer_name=payload.customer_name or "Anonymous User",
        intent=payload.intent or "General Inquiry",
        sentiment=payload.sentiment or "Neutral",
    )
    return ticket

@router.get("/tickets", response_model=List[SupportTicket])
async def list_tickets(status: Optional[str] = None):
    return ticket_dispatcher.list_tickets(status=status)

@router.post("/tickets/{ticket_id}/resolve", response_model=SupportTicket)
async def resolve_ticket(ticket_id: str, payload: ResolveTicketRequest):
    t = ticket_dispatcher.resolve_ticket(
        ticket_id=ticket_id,
        notes=payload.resolution_notes,
        agent=payload.agent_name or "Support Agent",
    )
    if not t:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return t

@router.get("/queue", response_model=List[LiveQueueItem])
async def get_live_queue():
    return live_queue.list_queue()

@router.post("/queue/{queue_id}/assign", response_model=LiveQueueItem)
async def assign_live_queue_agent(queue_id: str):
    item = live_queue.assign_agent(queue_id)
    if not item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    return item

@router.get("/canned")
async def get_canned_suggestions(intent: str, query: str = ""):
    suggestions = canned_suggester.suggest(intent, query)
    return {"intent": intent, "suggestions": suggestions}

@router.post("/webhooks/dispatch")
async def dispatch_custom_webhook(payload: DispatchWebhookRequest):
    success = await webhook_notifier.dispatch(
        webhook_url=payload.webhook_url,
        event_type=payload.event_type,
        data=payload.data,
    )
    return {"status": "success" if success else "failed"}