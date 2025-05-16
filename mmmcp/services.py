"""Service layer for text generation and summarization"""

import logging
from typing import Dict, Optional
from .config import ModelConfig, ModelProvider
from .models.base import BaseModel
from .models.openai_model import OpenAIModel
from .models.gemini_model import GeminiModel

logger = logging.getLogger(__name__)

class TextGenerationService:
    """Service for handling text generation and summarization"""
    
    def __init__(self):
        """Initialize the service"""
        self.config = ModelConfig()
        self.models: Dict[str, BaseModel] = {}
        self.final_model: Optional[BaseModel] = None
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize all configured models"""
        active_providers = self.config.get_active_providers()
        logger.info(f"Active providers: {[p.value for p in active_providers]}")
        
        # Initialize main models
        for provider in active_providers:
            model_name = self.config.get_model_name(provider)
            api_key = self.config.get_api_key(provider)
            
            if not model_name or not api_key:
                continue
                
            try:
                model = self._create_model_instance(provider, model_name, api_key)
                if model:
                    self.models[provider.value] = model
            except Exception as e:
                logger.error(f"Failed to initialize {provider.value} model: {str(e)}")
                
        # Initialize final model if configured
        final_model_name = self.config.get_final_model()
        if final_model_name:
            try:
                if final_model_name in self.config.OPENAI_MODELS:
                    api_key = self.config.get_api_key(ModelProvider.OPENAI)
                    self.final_model = OpenAIModel(final_model_name, api_key)
                elif final_model_name in self.config.GEMINI_MODELS:
                    api_key = self.config.get_api_key(ModelProvider.GEMINI)
                    self.final_model = GeminiModel(final_model_name, api_key)
                logger.info(f"Final model initialized: {final_model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize final model: {str(e)}")
                
    def _create_model_instance(self, provider: ModelProvider, model_name: str, api_key: str) -> Optional[BaseModel]:
        """Create a model instance based on provider"""
        if provider == ModelProvider.OPENAI:
            return OpenAIModel(model_name, api_key)
        elif provider == ModelProvider.GEMINI:
            return GeminiModel(model_name, api_key)
        elif provider == ModelProvider.NVIDIA:
            return GeminiModel(model_name, api_key)
        return None
        
    async def generate_text(self, prompt: str) -> Dict[str, str]:
        """Generate text using all configured models
        
        Args:
            prompt: Input prompt
            
        Returns:
            Dictionary mapping provider names to their responses
        """
        logger.info(f"Generating text for prompt: {prompt}")

        hasError = False
        results = {}
        for provider, model in self.models.items():
            try:
                results[provider] = await model.generate(prompt)
            except Exception as e:
                logger.error(f"Error generating text: {str(e)}", exc_info=True)
                results[provider] = f"Error: {str(e)}"
                hasError = True
            
        if hasError:
            logger.info("Error while generating text from active models")
        else:
            logger.info("Successfully generated text from active models")
            
        return results
            
            
    async def summarize_responses(self, responses: Dict[str, str]) -> Dict[str, str]:
        """Summarize multiple model responses
        
        Args:
            responses: Dictionary of model responses to summarize
            
        Returns:
            Dictionary containing the summary if final model is configured
        """
        if not self.final_model:
            logger.warning("No final model configured for summarization")
            return {}
            
        try:
            summary_prompt = "Please provide a concise summary of the following model responses:\n\n"
            for provider, response in responses.items():
                summary_prompt += f"{provider.upper()} MODEL RESPONSE:\n{response}\n\n"
            summary_prompt += "Please synthesize these responses into a single, coherent response that captures the key information from all models."
            
            summary = await self.final_model.generate(summary_prompt)
            return {"summary": summary}
            
        except Exception as e:
            logger.error(f"Error summarizing responses: {str(e)}", exc_info=True)
            raise 