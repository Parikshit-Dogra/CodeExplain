from .base_llm import BaseLLM
from .gemini_provider import GeminiProvider
from .ollama_provider import OllamaProvider
from .lmstudio_provider import LMStudioProvider
from config.settings import MODEL_PROVIDER

def get_llm_provider(provider_name: str = None) -> BaseLLM:
    """
    Factory function to get the appropriate LLM provider.
    
    Args:
        provider_name (str, optional): The name of the provider. 
                                       Defaults to MODEL_PROVIDER from settings.
    
    Returns:
        BaseLLM: An instance of the requested LLM provider.
    """
    provider = provider_name or MODEL_PROVIDER
    provider = provider.lower()
    
    if provider == "gemini":
        return GeminiProvider()
    elif provider == "ollama":
        return OllamaProvider()
    elif provider in ["lmstudio", "lm_studio", "lm-studio"]:
        return LMStudioProvider()
    else:
        raise ValueError(f"Unsupported model provider: {provider}")
