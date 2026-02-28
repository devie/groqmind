import time
import uuid
from dataclasses import dataclass, field

MAX_SESSIONS = 1000
SESSION_TTL = 3600  # 1 hour


@dataclass
class ChatSession:
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    messages: list[dict] = field(default_factory=list)
    persona: str = "general"
    model: str = "llama-3.1-8b-instant"
    total_tokens: int = 0
    last_active: float = field(default_factory=time.time)


_sessions: dict[str, ChatSession] = {}


def _cleanup():
    """Remove expired sessions and enforce max cap."""
    now = time.time()
    expired = [sid for sid, s in _sessions.items() if now - s.last_active > SESSION_TTL]
    for sid in expired:
        del _sessions[sid]
    # If still over cap, remove oldest
    if len(_sessions) > MAX_SESSIONS:
        by_age = sorted(_sessions.items(), key=lambda x: x[1].last_active)
        for sid, _ in by_age[:len(_sessions) - MAX_SESSIONS]:
            del _sessions[sid]


def get_or_create_session(session_id: str | None = None) -> ChatSession:
    if session_id and session_id in _sessions:
        s = _sessions[session_id]
        s.last_active = time.time()
        return s
    _cleanup()
    session = ChatSession()
    _sessions[session.id] = session
    return session


def get_session(session_id: str) -> ChatSession | None:
    s = _sessions.get(session_id)
    if s:
        s.last_active = time.time()
    return s


def clear_session(session_id: str) -> bool:
    if session_id in _sessions:
        _sessions[session_id].messages.clear()
        _sessions[session_id].total_tokens = 0
        return True
    return False
