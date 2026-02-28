import json

from fastapi import APIRouter, HTTPException, Request
from groq import Groq
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from groqmind.config import GROQ_API_KEY, MODELS
from groqmind.prompts import PERSONAS
from groqmind.session import clear_session, get_or_create_session, get_session

router = APIRouter(prefix="/api", tags=["Chat"])

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    persona: str = "general"
    model: str = "llama-3.1-8b-instant"


class SessionUpdate(BaseModel):
    persona: str | None = None
    model: str | None = None


@router.post("/chat")
async def chat(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    if req.persona not in PERSONAS:
        raise HTTPException(status_code=400, detail=f"Unknown persona: {req.persona}")
    if req.model not in MODELS:
        raise HTTPException(status_code=400, detail=f"Unknown model: {req.model}")

    session = get_or_create_session(req.session_id)
    session.persona = req.persona
    session.model = req.model
    session.messages.append({"role": "user", "content": req.message})

    # Keep conversation manageable (last 20 messages)
    if len(session.messages) > 20:
        session.messages = session.messages[-20:]

    system_prompt = PERSONAS[req.persona]["system"]
    messages = [{"role": "system", "content": system_prompt}] + session.messages

    async def generate():
        assistant_content = ""
        try:
            stream = client.chat.completions.create(
                model=req.model,
                messages=messages,
                stream=True,
                max_tokens=2048,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    assistant_content += delta.content
                    yield {"data": json.dumps({"token": delta.content})}

                if chunk.x_groq and hasattr(chunk.x_groq, "usage") and chunk.x_groq.usage:
                    session.total_tokens += chunk.x_groq.usage.total_tokens

            session.messages.append({"role": "assistant", "content": assistant_content})
            yield {"data": json.dumps({
                "done": True,
                "session_id": session.id,
                "tokens": session.total_tokens,
            })}
        except Exception as e:
            yield {"data": json.dumps({"error": str(e)})}

    return EventSourceResponse(generate())


@router.get("/session/{session_id}")
def get_session_info(session_id: str):
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {
        "id": session.id,
        "persona": session.persona,
        "model": session.model,
        "message_count": len(session.messages),
        "total_tokens": session.total_tokens,
    }


@router.post("/session/{session_id}/clear")
def clear(session_id: str):
    if not clear_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "cleared"}


@router.get("/models")
def list_models():
    return {"models": MODELS}


@router.get("/personas")
def list_personas():
    return {"personas": {k: v["name"] for k, v in PERSONAS.items()}}
