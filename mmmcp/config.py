"""Configuration management for MMMCP"""

from enum import Enum
from typing import Optional, Dict
import os
from pydantic_settings import BaseSettings
from pydantic import Field

class ModelProvider(Enum):
    """Supported model providers"""
    OPENAI = "openai"
    GEMINI = "gemini"
    NVIDIA = "nvidia"

class Settings(BaseSettings):
    """Application settings"""
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    GOOGLE_API_KEY: str = Field(..., description="Google API key")
    NVIDIA_API_KEY: Optional[str] = Field(None, description="NVIDIA API key")
    OPENAI_MODEL: str = Field("gpt-3.5-turbo", description="OpenAI model name")
    GEMINI_MODEL: str = Field("gemini-2.0-flash", description="Gemini model name")
    FINAL_MODEL: Optional[str] = Field(None, description="Model to use for summarization")
    ACTIVE_PROVIDERS: str = Field("openai,gemini", description="Comma-separated list of active providers")

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields in the environment

class ModelConfig:
    """Model configuration and validation"""
    
    OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4"]
    GEMINI_MODELS = ["gemini-2.0-flash"]
    
    def __init__(self):
        self.settings = Settings()
        
    def get_active_providers(self) -> list[ModelProvider]:
        """Get list of active model providers from environment"""
        providers = []
        for provider in self.settings.ACTIVE_PROVIDERS.split(","):
            try:
                providers.append(ModelProvider(provider.strip().lower()))
            except ValueError:
                continue
        return providers

    def get_model_name(self, provider: ModelProvider) -> Optional[str]:
        """Get model name for a specific provider"""
        if provider == ModelProvider.OPENAI:
            model = self.settings.OPENAI_MODEL
            if model in self.OPENAI_MODELS:
                return model
        elif provider == ModelProvider.GEMINI:
            model = self.settings.GEMINI_MODEL
            if model in self.GEMINI_MODELS:
                return model
        return None

    def get_final_model(self) -> Optional[str]:
        """Get the final model name if provided"""
        model = self.settings.FINAL_MODEL
        if model:
            if model in self.OPENAI_MODELS or model in self.GEMINI_MODELS:
                return model
        return None
    
    def get_api_key(self, provider: ModelProvider) -> Optional[str]:
        """Get API key for a provider"""
        if provider == ModelProvider.OPENAI:
            return self.settings.OPENAI_API_KEY
        elif provider == ModelProvider.GEMINI:
            return self.settings.GOOGLE_API_KEY
        elif provider == ModelProvider.NVIDIA:
            return self.settings.NVIDIA_API_KEY
        return None 