from app.escalation.ticket_dispatcher import TicketDispatcher
from app.escalation.webhook_notifier import WebhookNotifier
from app.escalation.live_queue import LiveTriageQueue
from app.escalation.canned_responses import CannedResponseSuggester

def test_ticket_dispatcher_priority_assignment():
    dispatcher = TicketDispatcher()

    # Frustrated billing query -> Urgent priority
    t1 = dispatcher.create_ticket("sess_1", "I demand a refund immediately!", "Billing & Invoicing", "Frustrated")
    assert t1.priority == "Urgent"
    assert t1.status == "open"

    # General inquiry -> Low priority
    t2 = dispatcher.create_ticket("sess_2", "Where is the office located?", "General Inquiry", "Neutral")
    assert t2.priority == "Low"

    # Resolve ticket
    res = dispatcher.resolve_ticket(t1.ticket_id, notes="Processed refund in Stripe", agent="Support Lead")
    assert res.status == "resolved"
    assert res.assigned_agent == "Support Lead"


def test_webhook_hmac_signature_generation():
    notifier = WebhookNotifier(secret="test_secret_123")
    payload = {"ticket_id": "TICK-123", "status": "escalated"}
    ts = 1723968000

    sig1 = notifier.sign_payload(payload, ts)
    sig2 = notifier.sign_payload(payload, ts)
    assert sig1 == sig2
    assert len(sig1) == 64  # SHA-256 hex string


def test_live_queue_priority_ordering():
    queue = LiveTriageQueue()

    # Low priority
    q_low = queue.enqueue("sess_low", "User Low", "General Inquiry", "Neutral", num_turns=1)
    # Urgent churn risk
    q_urgent = queue.enqueue("sess_urg", "User VIP", "Churn & Cancellation Risk", "Urgent", num_turns=5)

    ranked = queue.list_queue()
    assert len(ranked) == 2
    # Urgent must be first
    assert ranked[0].queue_id == q_urgent.queue_id
    assert ranked[0].priority_score > ranked[1].priority_score


def test_canned_responses_suggestions():
    suggester = CannedResponseSuggester()
    suggestions = suggester.suggest("Billing & Invoicing", "How do I get a refund?")
    assert len(suggestions) >= 3
    assert any("refund" in s.lower() for s in suggestions)