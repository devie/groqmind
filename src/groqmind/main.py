import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from groqmind.routers import chat

STATIC_DIR = Path(__file__).parent / "static"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "https://chat.zuhdi.id").split(",")

app = FastAPI(title="GroqMind", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Optional bearer token auth for API endpoints
AUTH_TOKEN = os.getenv("GROQMIND_AUTH_TOKEN", "")

if AUTH_TOKEN:
    from fastapi.responses import JSONResponse

    @app.middleware("http")
    async def check_auth(request: Request, call_next):
        # Allow static files and index page without auth
        if request.url.path == "/" or request.url.path.startswith("/static"):
            return await call_next(request)
        # Check bearer token for API calls
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or auth[7:] != AUTH_TOKEN:
            return JSONResponse({"error": "Unauthorized"}, status_code=401)
        return await call_next(request)

app.include_router(chat.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


def start():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "6002"))
    reload = os.getenv("ENV", "development") == "development"
    uvicorn.run("groqmind.main:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    start()
