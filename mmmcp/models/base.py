"""Base model interface"""

from abc import ABC, abstractmethod
from typing import Optional

class BaseModel(ABC):
    """Base class for all language models"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the model
        
        Args:
            model_name: Name of the model to use
            api_key: API key for the service
        """
        if not api_key:
            raise ValueError("API key not provided")
        self.model_name = model_name
        self.api_key = api_key
        
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate text from a prompt
        
        Args:
            prompt: The input prompt
            
        Returns:
            Generated text response
        """
        pass 