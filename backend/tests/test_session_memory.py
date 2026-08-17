import pytest
from app.memory.session_store import SessionStore
from app.memory.intent_classifier import IntentClassifier
from app.memory.sentiment_tracker import SentimentTracker
from app.memory.query_rewriter import QueryRewriter

def test_session_store_sliding_window():
    store = SessionStore(max_history_turns=2)
    sid = "sess_test_1"

    # Add 6 turns (12 messages)
    for i in range(6):
        store.add_message(sid, "user", f"User question {i}")
        store.add_message(sid, "assistant", f"Assistant answer {i}")

    sess = store._sessions[sid]
    # Max turns is 2 (4 messages)
    assert len(sess.messages) <= 4
    assert sess.messages[-1].content == "Assistant answer 5"


@pytest.mark.asyncio
async def test_intent_classifier_rules():
    classifier = IntentClassifier()

    assert await classifier.classify("I want a refund for my subscription") == "Billing & Invoicing"
    assert await classifier.classify("How do I setup MFA authentication?") == "Security & Privacy"
    assert await classifier.classify("My Slack integration is broken and not syncing") == "Technical & Troubleshooting"
    assert await classifier.classify("How much does the Pro tier plan cost?") == "Pricing & Plans"
    assert await classifier.classify("Please cancel and close my account immediately") == "Churn & Cancellation Risk"


def test_sentiment_tracker_scoring():
    tracker = SentimentTracker()

    frustrated = tracker.analyze("This is terrible, completely broken and unacceptable!")
    assert frustrated["sentiment"] == "Urgent / Frustrated"
    assert frustrated["requires_human_attention"] is True

    positive = tracker.analyze("Thank you so much, this was very helpful!")
    assert positive["sentiment"] == "Satisfied"
    assert positive["requires_human_attention"] is False

    neutral = tracker.analyze("Where can I find the API docs?")
    assert neutral["sentiment"] == "Neutral"