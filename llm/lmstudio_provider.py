from openai import OpenAI
from .base_llm import BaseLLM
from config.settings import LMSTUDIO_URL, LOCAL_MODEL

class LMStudioProvider(BaseLLM):
    def __init__(self):
        # LM Studio uses an OpenAI-compatible API
        self.client = OpenAI(base_url=LMSTUDIO_URL, api_key="lm-studio")
        self.model = LOCAL_MODEL

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful programming tutor. Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                # LM Studio might not always support response_format="json_object" depending on the model, 
                # but we will try to enforce it through the prompt.
                # If supported, we could add: response_format={ "type": "json_object" }
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling LM Studio API: {e}")
            raise
