import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from groqmind.routers import chat

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="GroqMind", version="1.0.0")

app.include_router(chat.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


def start():
    uvicorn.run("groqmind.main:app", host="0.0.0.0", port=6002, reload=True)


if __name__ == "__main__":
    start()
