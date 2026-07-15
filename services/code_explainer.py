import json
import re
from typing import Optional
from models.response_schema import ResponseSchema, QuizSchema
from llm.llm_factory import get_llm_provider
from config.prompts import CODE_EXPLANATION_PROMPT, QUIZ_GENERATION_PROMPT

class CodeExplainerService:
    def __init__(self, provider_name: str = None):
        self.llm = get_llm_provider(provider_name)
        
    def _clean_json_string(self, raw_string: str) -> str:
        """
        Sometimes LLMs wrap JSON in markdown block like ```json ... ```
        This helper removes that if present.
        """
        cleaned = raw_string.strip()
        # Remove markdown code block if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
            
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
            
        return cleaned.strip()

    def explain_code(self, code: str, language: str, difficulty: str, code_language: str) -> Optional[ResponseSchema]:
        """
        Generates an explanation for the given code.
        """
        target_language_prompt = code_language
        if code_language == "Auto-detect":
            target_language_prompt = "Auto-detect (You must identify the programming language)"

        prompt = CODE_EXPLANATION_PROMPT.format(
            language=language,
            difficulty=difficulty,
            code_language=target_language_prompt,
            code=code
        )
        
        try:
            raw_response = self.llm.generate(prompt)
            cleaned_json = self._clean_json_string(raw_response)
            
            # Parse to dict first to validate structure via Pydantic
            data_dict = json.loads(cleaned_json)
            validated_response = ResponseSchema(**data_dict)
            return validated_response
            
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from LLM response: {e}")
            # Try to return something or bubble up the error
            raise ValueError("The LLM did not return valid JSON.")
        except Exception as e:
            print(f"Error during code explanation: {e}")
            raise

    def generate_quiz(self, code: str, difficulty: str) -> Optional[QuizSchema]:
        """
        Generates an interactive quiz for the given code.
        """
        prompt = QUIZ_GENERATION_PROMPT.format(
            difficulty=difficulty,
            code=code
        )
        
        try:
            raw_response = self.llm.generate(prompt)
            cleaned_json = self._clean_json_string(raw_response)
            
            data_dict = json.loads(cleaned_json)
            validated_response = QuizSchema(**data_dict)
            return validated_response
            
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from LLM response for quiz: {e}")
            raise ValueError("The LLM did not return valid JSON for the quiz.")
        except Exception as e:
            print(f"Error during quiz generation: {e}")
            raise
