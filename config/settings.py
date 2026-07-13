import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "").lower()
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "qwen3:4b")
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://localhost:1234/v1")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
