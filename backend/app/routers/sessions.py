from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from app.memory.session_store import session_store, SessionData

router = APIRouter(prefix="/sessions", tags=["Sessions & Analytics"])

@router.get("", response_model=List[SessionData])
async def list_sessions():
    return session_store.list_all_sessions()

@router.get("/{session_id}", response_model=SessionData)
async def get_session(session_id: str):
    sess = session_store._sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")
    return sess

@router.get("/{session_id}/analytics")
async def get_session_analytics(session_id: str):
    sess = session_store._sessions.get(session_id)
    if not sess:
        raise HTTPException(status_code=404, detail="Session not found")

    total_turns = len(sess.messages) // 2
    sentiment_counts = {}
    for s in sess.sentiment_history:
        sentiment_counts[s] = sentiment_counts.get(s, 0) + 1

    return {
        "session_id": session_id,
        "total_turns": total_turns,
        "primary_intent": sess.primary_intent,
        "sentiment_breakdown": sentiment_counts,
        "escalation_risk": "High" if any("Frustrated" in s for s in sess.sentiment_history) else "Low",
    }