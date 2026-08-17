import time
import uuid
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class SessionMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str
    timestamp: float
    confidence: Optional[str] = "high"
    intent: Optional[str] = "General Inquiry"
    sentiment: Optional[str] = "Neutral"

class SessionData(BaseModel):
    session_id: str
    created_at: float
    updated_at: float
    messages: List[SessionMessage] = []
    primary_intent: str = "General Inquiry"
    sentiment_history: List[str] = []

class SessionStore:
    """
    In-memory / Redis-compatible sliding window conversation history store.
    """
    def __init__(self, max_history_turns: int = 10):
        self.max_history_turns = max_history_turns
        self._sessions: Dict[str, SessionData] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> SessionData:
        sid = session_id or str(uuid.uuid4())
        if sid not in self._sessions:
            now = time.time()
            self._sessions[sid] = SessionData(
                session_id=sid,
                created_at=now,
                updated_at=now,
                messages=[],
            )
        return self._sessions[sid]

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        confidence: str = "high",
        intent: str = "General Inquiry",
        sentiment: str = "Neutral",
    ):
        sess = self.get_or_create(session_id)
        msg = SessionMessage(
            role=role,
            content=content,
            timestamp=time.time(),
            confidence=confidence,
            intent=intent,
            sentiment=sentiment,
        )
        sess.messages.append(msg)
        sess.updated_at = time.time()
        sess.primary_intent = intent
        sess.sentiment_history.append(sentiment)

        # Enforce sliding window
        if len(sess.messages) > self.max_history_turns * 2:
            sess.messages = sess.messages[-self.max_history_turns * 2:]

    def get_conversation_context(self, session_id: str, last_n: int = 4) -> str:
        """Returns formatted recent chat history for query rewriting."""
        sess = self._sessions.get(session_id)
        if not sess or not sess.messages:
            return ""

        recent = sess.messages[-last_n:]
        lines = []
        for m in recent:
            prefix = "Customer" if m.role == "user" else "Assistant"
            lines.append(f"{prefix}: {m.content}")
        return "\n".join(lines)

    def list_all_sessions(self) -> List[SessionData]:
        return sorted(self._sessions.values(), key=lambda s: s.updated_at, reverse=True)

session_store = SessionStore()