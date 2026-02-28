import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

MODELS = {
    "llama-3.1-8b-instant": "Llama 3.1 8B (Fast)",
    "llama-3.3-70b-versatile": "Llama 3.3 70B (Powerful)",
}

DEFAULT_MODEL = "llama-3.1-8b-instant"
