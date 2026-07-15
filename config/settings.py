import os
from dotenv import load_dotenv

load_dotenv()

def get_env_or_secret(key, default=""):
    # First try environment variables
    val = os.getenv(key)
    if val:
        return val
        
    # Then try Streamlit secrets if available
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
        
    return default

GEMINI_API_KEY = get_env_or_secret("GEMINI_API_KEY", "")
GEMINI_MODEL = get_env_or_secret("GEMINI_MODEL", "gemini-2.5-flash")
MODEL_PROVIDER = get_env_or_secret("MODEL_PROVIDER", "").lower()
OLLAMA_MODEL = get_env_or_secret("OLLAMA_MODEL", "llama3")
LMSTUDIO_MODEL = get_env_or_secret("LMSTUDIO_MODEL", "gemma4-e4b")
LMSTUDIO_URL = get_env_or_secret("LMSTUDIO_URL", "http://localhost:1234/v1")
OLLAMA_URL = get_env_or_secret("OLLAMA_URL", "http://localhost:11434")
