import google.generativeai as genai
import os
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .config import ModelConfig, ModelProvider

logger = logging.getLogger(__name__)

class GeminiModel:
    def __init__(self, api_key: str = None):
        if not api_key:
            raise ValueError("Google API key not found")
        
        self.model_name = ModelConfig.get_model_name(ModelProvider.GEMINI)
        if not self.model_name:
            raise ValueError("Invalid Gemini model specified in environment")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self._executor = ThreadPoolExecutor(max_workers=1)
        logger.debug(f"Gemini client initialized with model {self.model_name}")

    def _generate_sync(self, prompt: str) -> str:
        """Synchronous generation method"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"

    async def generate(self, prompt: str) -> str:
        """Generate text using Google's Gemini model asynchronously"""
        try:
            logger.debug(f"Calling Gemini API with model {self.model_name}")
            loop = asyncio.get_running_loop()
            text = await loop.run_in_executor(self._executor, self._generate_sync, prompt)
            logger.debug("Gemini response received")
            return text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"