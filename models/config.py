from enum import Enum
import os
from typing import Optional

class ModelProvider(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"

class ModelConfig:
    OPENAI_MODELS = ["gpt-3.5-turbo", "gpt-4"]
    GEMINI_MODELS = ["gemini-pro", "gemini-2.0-flash"]

    @staticmethod
    def get_active_providers() -> list[ModelProvider]:
        """Get list of active model providers from environment"""
        active_providers_str = os.getenv("ACTIVE_PROVIDERS", "openai,gemini")
        providers = []
        for provider in active_providers_str.split(","):
            try:
                providers.append(ModelProvider(provider.strip().lower()))
            except ValueError:
                continue
        return providers

    @staticmethod
    def get_model_name(provider: ModelProvider) -> Optional[str]:
        """Get model name for a specific provider from environment"""
        if provider == ModelProvider.OPENAI:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            if model in ModelConfig.OPENAI_MODELS:
                return model
        elif provider == ModelProvider.GEMINI:
            model = os.getenv("GEMINI_MODEL", "gemini-pro")
            if model in ModelConfig.GEMINI_MODELS:
                return model
        return None 