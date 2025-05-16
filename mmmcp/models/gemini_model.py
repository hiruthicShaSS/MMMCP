"""Google Gemini model implementation"""

import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai
from typing import Optional
from .base import BaseModel

logger = logging.getLogger(__name__)

class GeminiModel(BaseModel):
    """Google Gemini language model implementation"""
    
    def __init__(self, model_name: str, api_key: Optional[str] = None):
        """Initialize the Gemini model
        
        Args:
            model_name: Name of the Gemini model to use
            api_key: Google API key
        """
        super().__init__(model_name, api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self._executor = ThreadPoolExecutor(max_workers=1)
        logger.debug(f"Gemini client initialized with model {model_name}")

    def _generate_sync(self, prompt: str) -> str:
        """Synchronous generation method
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text response
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise

    async def generate(self, prompt: str) -> str:
        """Generate text using Gemini model asynchronously
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Calling Gemini API with model {self.model_name}")
            loop = asyncio.get_running_loop()
            text = await loop.run_in_executor(self._executor, self._generate_sync, prompt)
            logger.debug("Gemini response received")
            return text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            raise 