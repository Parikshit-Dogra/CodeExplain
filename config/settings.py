import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "").lower()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "gemma4-e4b")
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
