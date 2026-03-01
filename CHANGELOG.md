# Changelog

All notable changes to GroqMind are documented here.

---

## [Unreleased] — 2026-03-01

### Fixed
- **Session ID validation** — fixed null session_id rejection on first message when no session exists yet

### Security
- CORS protection with configurable origins
- XSS prevention on user input rendering
- Session limits (max sessions per IP, max message length)
- Input validation on all endpoints

---

## [7bd2a31] — 2026-02-28

### Added
- Security hardening: CORS, XSS prevention, session limits, input validation

---

## [e32e741] — 2026-02-28

### Added
- Initial release
- Streaming chat via Server-Sent Events (SSE)
- Conversation memory (multi-turn context within sessions)
- Persona switching: General, Code Helper, Business Advisor, Bahasa Indonesia
- Model switcher: Llama 3.1 8B (fast), Llama 3.3 70B (powerful)
- Markdown rendering with syntax-highlighted code blocks and copy button
- Live token usage counter per session
- Responsive UI with Tailwind CSS
