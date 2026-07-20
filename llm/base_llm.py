"""
Module: base_llm
Purpose: Defines the abstract base class for all Language Model (LLM) providers.
By using an abstract base class, we ensure that every specific LLM provider 
(like Gemini, Ollama, LMStudio) implements the required interface. This allows 
the rest of the application to interact with any LLM interchangeably without 
worrying about the underlying implementation details.
"""

from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """
    Abstract Base Class for LLM providers.
    Inheriting from ABC (Abstract Base Class) makes it impossible to instantiate 
    this class directly, and forces any child classes to implement methods 
    decorated with @abstractmethod.
    """
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM given a prompt.
        
        This method must be overridden by every subclass to handle the specific
        API calls (e.g., HTTP requests, SDK calls) required by the respective LLM.
        
        Args:
            prompt (str): The structured text prompt containing the code and instructions.
            
        Returns:
            str: The raw string response (expected to be in JSON format) returned by the LLM.
        """
        pass
