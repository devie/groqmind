# GroqMind

AI chat assistant with streaming responses, conversation memory, and persona switching — powered by Groq.

**Live Demo:** [chat.zuhdi.id](https://chat.zuhdi.id)

## Features

- **Streaming Chat** — Real-time token-by-token responses via Server-Sent Events (SSE)
- **Conversation Memory** — Multi-turn context within sessions
- **Persona Switching** — General, Code Helper, Business Advisor, Bahasa Indonesia
- **Model Switcher** — Llama 3.1 8B (fast) or Llama 3.3 70B (powerful)
- **Markdown Rendering** — Syntax-highlighted code blocks with copy button
- **Token Usage** — Live token counter per session
- **Security** — CORS protection, XSS prevention, session limits, input validation

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.12, FastAPI |
| AI | Groq SDK (Llama 3.x) |
| Streaming | SSE (sse-starlette) |
| Frontend | Vanilla JS, Tailwind CSS |
| Deploy | uv, Cloudflare Tunnel |

## Quick Start

```bash
# Set your Groq API key
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# Install and run
uv sync
uv run groqmind
```

Server starts at `http://localhost:6002`

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key ([console.groq.com](https://console.groq.com)) | Yes |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Chat UI |
| POST | `/chat` | Send message (SSE streaming response) |
| GET | `/health` | Health check |

## How It Works

1. User selects a persona and model from the sidebar
2. Messages are sent via POST to `/chat` with session context
3. Groq API streams tokens back via SSE
4. Frontend renders markdown in real-time with syntax highlighting
5. Conversation history is maintained per session for multi-turn context

## License

MIT
