# GroqMind

AI assistant with streaming responses, conversation memory, and persona switching — powered by Groq.

## Features

- **Streaming Chat** — Real-time token-by-token responses via SSE
- **Conversation Memory** — Multi-turn context within sessions
- **Persona Switching** — General, Code Helper, Business Advisor, Bahasa Indonesia
- **Model Switcher** — Llama 3.1 8B (fast) or Llama 3.3 70B (powerful)
- **Markdown Rendering** — Syntax-highlighted code blocks with copy button
- **Token Usage** — Live token counter per session

## Tech Stack

- FastAPI + Groq SDK + SSE
- Vanilla JS + Tailwind CSS (CDN)
- uv for dependency management

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

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key ([console.groq.com](https://console.groq.com)) |

## Live Demo

[chat.zuhdi.id](https://chat.zuhdi.id)
