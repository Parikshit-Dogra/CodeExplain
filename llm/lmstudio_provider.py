"""
Module: lmstudio_provider
Purpose: Implements integration with a local LM Studio instance.
LM Studio provides an OpenAI-compatible REST API. Therefore, this provider
utilizes the official `openai` Python package, but points the base URL to 
the local LM Studio server instead of OpenAI's cloud servers.
"""

from openai import OpenAI
from .base_llm import BaseLLM
from config.settings import LMSTUDIO_URL, LMSTUDIO_MODEL

class LMStudioProvider(BaseLLM):
    """
    Provider class for interacting with models hosted locally via LM Studio.
    Inherits from BaseLLM, ensuring it implements the `generate` method.
    """
    
    def __init__(self):
        """
        Initializes the OpenAI client configured for LM Studio.
        It uses the base URL specified in settings (e.g., http://localhost:1234/v1).
        """
        # We override the base_url to point to our local LM Studio instance.
        # The api_key is typically ignored by LM Studio, but "lm-studio" is used as a placeholder.
        self.client = OpenAI(base_url=LMSTUDIO_URL, api_key="lm-studio")
        self.model = LMSTUDIO_MODEL

    def generate(self, prompt: str) -> str:
        """
        Sends the prompt to LM Studio via the OpenAI-compatible API.
        
        Args:
            prompt (str): The structured prompt to send to the model.
            
        Returns:
            str: The generated response string (expected to be JSON).
        """
        try:
            # Create a chat completion request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    # System prompt instructs the model on its role and expected output format
                    {"role": "system", "content": "You are a helpful programming tutor. Return ONLY valid JSON."},
                    # User prompt contains the actual code and instructions
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Controls randomness (0.7 is a good balance for creativity and coherence)
                
                # Note: LM Studio models may or may not support strict JSON mode 
                # (response_format={"type": "json_object"}), so we rely primarily on the system prompt.
            )
            # Extract and return the content of the first message choice
            return response.choices[0].message.content
        except Exception as e:
            # Log and re-raise any exceptions that occur during the API call
            print(f"Error calling LM Studio API: {e}")
            raise
