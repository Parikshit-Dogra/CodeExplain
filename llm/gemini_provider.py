import os
from google import genai
from .base_llm import BaseLLM
from config.settings import GEMINI_API_KEY, GEMINI_MODEL

class GeminiProvider(BaseLLM):
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = GEMINI_MODEL

    def generate(self, prompt: str) -> str:
        try:
            # We enforce JSON response format
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            raise
