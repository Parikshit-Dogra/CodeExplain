"""
This module centralizes all configuration variables and secrets required by the application.
It loads variables from a standard `.env` file or from Streamlit's internal secrets manager.
This ensures API keys and URLs are not hardcoded into the source code.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

def get_env_or_secret(key, default=""):
    """
    Helper function to securely retrieve configuration values.
    
    It checks for the value in the following order:
    1. System environment variables (e.g., set via export or .env).
    2. Streamlit's secrets manager (useful when deployed on Streamlit Community Cloud).
    3. The provided default value fallback.
    
    Args:
        key (str): The configuration key to look up.
        default (str): The fallback value if the key is not found anywhere.
        
    Returns:
        str: The resolved configuration value.
    """
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
        # If Streamlit is not available or secrets aren't set, silently ignore
        pass
        
    return default

# Configuration Variables
# These variables control which LLM models and APIs the application connects to.

GEMINI_API_KEY = get_env_or_secret("GEMINI_API_KEY", "")
GEMINI_MODEL = get_env_or_secret("GEMINI_MODEL", "gemini-2.5-flash")
MODEL_PROVIDER = get_env_or_secret("MODEL_PROVIDER", "").lower()

# Local model configurations
OLLAMA_MODEL = get_env_or_secret("OLLAMA_MODEL", "llama3")
OLLAMA_URL = get_env_or_secret("OLLAMA_URL", "http://localhost:11434")

LMSTUDIO_MODEL = get_env_or_secret("LMSTUDIO_MODEL", "gemma4-e4b")
LMSTUDIO_URL = get_env_or_secret("LMSTUDIO_URL", "http://localhost:1234/v1")
