"""
Module: llm_factory
Purpose: Implements the Factory design pattern for creating LLM providers.
This module is responsible for instantiating the correct LLM provider class based
on the application configuration (or a requested provider name). This abstracts
the instantiation logic away from the rest of the application.
"""

from .base_llm import BaseLLM
from .gemini_provider import GeminiProvider
from .ollama_provider import OllamaProvider
from .lmstudio_provider import LMStudioProvider
from config.settings import MODEL_PROVIDER

def get_llm_provider(provider_name: str = None) -> BaseLLM:
    """
    Factory function to instantiate and return the appropriate LLM provider.
    
    By centralizing provider creation here, the main application code doesn't need
    to know which specific provider class (e.g., GeminiProvider, OllamaProvider) 
    is being used, promoting loose coupling.
    
    Args:
        provider_name (str, optional): The name of the provider to instantiate. 
                                       If not provided, it defaults to the MODEL_PROVIDER 
                                       defined in the global settings.
    
    Returns:
        BaseLLM: An initialized instance of the requested LLM provider.
        
    Raises:
        ValueError: If the requested provider name is not supported.
    """
    # Use the passed provider_name if available, otherwise fall back to settings
    provider = provider_name or MODEL_PROVIDER
    provider = provider.lower()
    
    # Return the corresponding provider instance based on the string name
    if provider == "gemini":
        return GeminiProvider()
    elif provider == "ollama":
        return OllamaProvider()
    elif provider in ["lmstudio", "lm_studio", "lm-studio", "lm studio"]:
        # We check multiple string variations to handle different potential config inputs
        return LMStudioProvider()
    else:
        # If an unknown provider is specified, raise an error to fail fast
        raise ValueError(f"Unsupported model provider: {provider}")
