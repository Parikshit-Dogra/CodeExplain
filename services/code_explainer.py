"""
This module contains the CodeExplainerService, which acts as the core business logic layer 
for the application. It orchestrates the communication between the user's input (code, settings) 
and the chosen LLM provider to generate explanations and quizzes.

By keeping this logic in a dedicated 'service' class, we separate the prompt construction 
and JSON parsing from the UI layer (Streamlit app) and the low-level LLM API calls.
"""

import json
from typing import Optional
from models.response_schema import ResponseSchema, QuizSchema
from llm.llm_factory import get_llm_provider
from config.prompts import CODE_EXPLANATION_PROMPT, QUIZ_GENERATION_PROMPT

class CodeExplainerService:
    """
    Service class responsible for handling requests to explain code and generate quizzes.
    It encapsulates the selected LLM provider and formats prompts before sending them.
    """
    def __init__(self, provider_name: str = None):
        """
        Initializes the service with a specific LLM provider.
        
        Args:
            provider_name (str, optional): The name of the LLM provider to use (e.g., 'gemini', 'lmstudio').
                                           If None, the factory will likely choose a default.
        """
        # Obtain the appropriate LLM implementation from the factory based on the requested provider name
        self.llm = get_llm_provider(provider_name)
        
    def _clean_json_string(self, raw_string: str) -> str:
        """
        Helper method to sanitize the output returned by the LLM.
        
        Sometimes LLMs wrap their JSON responses inside markdown code blocks (e.g., ```json ... ```).
        This function strips away those markdown formatting tags to ensure the resulting string 
        is valid JSON that can be parsed by `json.loads()`.
        
        Args:
            raw_string (str): The raw text response from the LLM.
            
        Returns:
            str: The cleaned JSON string without markdown formatting.
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
        Generates a detailed, structured explanation for the provided code snippet.
        
        This method formats the explanation prompt with user parameters, sends it to the LLM,
        cleans the response, and validates it against the ResponseSchema.
        
        Args:
            code (str): The source code snippet to explain.
            language (str): The target language for the explanation text (e.g., 'English', 'Hindi').
            difficulty (str): The target audience difficulty level (e.g., 'Beginner', 'Expert').
            code_language (str): The programming language of the code (or 'Auto-detect').
            
        Returns:
            Optional[ResponseSchema]: A validated Pydantic model containing the structured explanation,
                                      or raises an exception if parsing fails.
        """
        # Determine the language instruction for the prompt
        target_language_prompt = code_language
        if code_language == "Auto-detect":
            target_language_prompt = "Auto-detect (You must identify the programming language)"

        # Inject the arguments into the predefined prompt template
        prompt = CODE_EXPLANATION_PROMPT.format(
            language=language,
            difficulty=difficulty,
            code_language=target_language_prompt,
            code=code
        )
        
        try:
            # 1. Send the prompt to the LLM
            raw_response = self.llm.generate(prompt)
            # 2. Clean any markdown artifacts from the response
            cleaned_json = self._clean_json_string(raw_response)
            
            # 3. Parse the cleaned string into a Python dictionary
            data_dict = json.loads(cleaned_json)
            # 4. Validate the dictionary against our strict Pydantic schema
            validated_response = ResponseSchema(**data_dict)
            
            return validated_response
            
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from LLM response: {e}")
            # If the LLM didn't return valid JSON, raise a clear error to the UI
            raise ValueError("The LLM did not return valid JSON.")
        except Exception as e:
            print(f"Error during code explanation: {e}")
            raise

    def generate_quiz(self, code: str, difficulty: str) -> Optional[QuizSchema]:
        """
        Generates an interactive multiple-choice quiz based on the provided code.
        
        Args:
            code (str): The source code snippet to generate questions for.
            difficulty (str): The difficulty level of the quiz questions.
            
        Returns:
            Optional[QuizSchema]: A validated Pydantic model containing the quiz questions and options.
        """
        # Inject arguments into the quiz prompt template
        prompt = QUIZ_GENERATION_PROMPT.format(
            difficulty=difficulty,
            code=code
        )
        
        try:
            # 1. Ask the LLM to generate the quiz
            raw_response = self.llm.generate(prompt)
            # 2. Clean markdown from the output
            cleaned_json = self._clean_json_string(raw_response)
            
            # 3. Parse and validate the response against QuizSchema
            data_dict = json.loads(cleaned_json)
            validated_response = QuizSchema(**data_dict)
            
            return validated_response
            
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON from LLM response for quiz: {e}")
            raise ValueError("The LLM did not return valid JSON for the quiz.")
        except Exception as e:
            print(f"Error during quiz generation: {e}")
            raise
