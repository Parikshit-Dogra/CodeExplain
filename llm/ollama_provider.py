import requests
import json
from .base_llm import BaseLLM
from config.settings import OLLAMA_URL, OLLAMA_MODEL

class OllamaProvider(BaseLLM):
    def __init__(self):
        self.url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        self.model = OLLAMA_MODEL

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        
        try:
            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            raise
