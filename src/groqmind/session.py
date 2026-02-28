import uuid
from dataclasses import dataclass, field


@dataclass
class ChatSession:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    messages: list[dict] = field(default_factory=list)
    persona: str = "general"
    model: str = "llama-3.1-8b-instant"
    total_tokens: int = 0


_sessions: dict[str, ChatSession] = {}


def get_or_create_session(session_id: str | None = None) -> ChatSession:
    if session_id and session_id in _sessions:
        return _sessions[session_id]
    session = ChatSession()
    _sessions[session.id] = session
    return session


def get_session(session_id: str) -> ChatSession | None:
    return _sessions.get(session_id)


def clear_session(session_id: str) -> bool:
    if session_id in _sessions:
        _sessions[session_id].messages.clear()
        _sessions[session_id].total_tokens = 0
        return True
    return False
