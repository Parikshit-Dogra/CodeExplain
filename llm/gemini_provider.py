"""
Module: gemini_provider
Purpose: Implements the Google Gemini API integration.
This provider uses the official google-genai SDK to send prompts to the Gemini model
and retrieve responses, specifically enforcing a JSON response format.
"""

import os
from google import genai
from .base_llm import BaseLLM
from config.settings import GEMINI_API_KEY, GEMINI_MODEL

class GeminiProvider(BaseLLM):
    """
    Provider class for Google's Gemini models.
    Inherits from BaseLLM, ensuring it implements the `generate` method.
    """
    
    def __init__(self):
        """
        Initializes the Gemini client. 
        It reads the API key and model identifier from the application settings.
        """
        # Ensure the API key is present before attempting to create the client
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        
        # Instantiate the GenAI client with the provided API key
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model_id = GEMINI_MODEL

    def generate(self, prompt: str) -> str:
        """
        Sends the prompt to the Gemini API and returns the generated text.
        
        Args:
            prompt (str): The structured prompt.
            
        Returns:
            str: The raw JSON string returned by Gemini.
        """
        try:
            # Make the API call to generate content
            # We enforce a JSON response format via GenerateContentConfig
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )
            # Return the text portion of the response which contains the JSON string
            return response.text
        except Exception as e:
            # Catch and log any exceptions (e.g., network issues, invalid keys) before re-raising
            print(f"Error calling Gemini API: {e}")
            raise
