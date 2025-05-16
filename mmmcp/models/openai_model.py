"""OpenAI model implementation"""

import logging
from openai import OpenAI
from typing import Optional
from .base import BaseModel

logger = logging.getLogger(__name__)

class OpenAIModel(BaseModel):
    """OpenAI language model implementation"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the OpenAI model
        
        Args:
            model_name: Name of the OpenAI model to use
            api_key: OpenAI API key
        """
        super().__init__(model_name, api_key)
        self.client = OpenAI(api_key=api_key)
        logger.debug(f"OpenAI client initialized with model {model_name}")

    async def generate(self, prompt: str) -> str:
        """Generate text using OpenAI's model
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Calling OpenAI API with model {self.model_name}")
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content
            logger.debug("OpenAI response received")
            return text
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}", exc_info=True)
            raise 