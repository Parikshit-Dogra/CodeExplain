from abc import ABC, abstractmethod

class BaseLLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the LLM given a prompt.
        
        Args:
            prompt (str): The structured prompt.
            
        Returns:
            str: The raw JSON string returned by the LLM.
        """
        pass
