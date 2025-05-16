from openai import OpenAI
import os
import logging
from .config import ModelConfig, ModelProvider

logger = logging.getLogger(__name__)

class OpenAIModel:
    def __init__(self, api_key: str = None):
        if not api_key:
            raise ValueError("OpenAI API key not found")
        
        self.model_name = ModelConfig.get_model_name(ModelProvider.OPENAI)
        if not self.model_name:
            raise ValueError("Invalid OpenAI model specified in environment")
            
        self.client = OpenAI(api_key=api_key)
        logger.debug(f"OpenAI client initialized with model {self.model_name}")

    async def generate(self, prompt: str) -> str:
        """Generate text using OpenAI's GPT model"""
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
            return f"Error: {str(e)}"