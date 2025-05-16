from mcp.server.fastmcp import FastMCP
from typing import Dict
import os
from dotenv import load_dotenv
import logging
from models import OpenAIModel, GeminiModel
from models.config import ModelConfig, ModelProvider

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()
logger.debug("Environment variables loaded")

mcp = FastMCP("MMMCP")
logger.info("MCP Server initialized")

# Initialize active AI models based on configuration
models = {}
active_providers = ModelConfig.get_active_providers()
logger.info(f"Active providers: {[p.value for p in active_providers]}")

if ModelProvider.OPENAI in active_providers:
    models['openai'] = OpenAIModel(os.environ.get("OPENAI_API_KEY"))
if ModelProvider.GEMINI in active_providers:
    models['gemini'] = GeminiModel(os.environ.get("GOOGLE_API_KEY"))

logger.debug(f"Initialized models: {list(models.keys())}")

@mcp.tool()
async def generate_text(prompt: str) -> Dict[str, str]:
    """Generate text using configured AI models"""
    logger.info(f"Generating text for prompt: {prompt}")
    
    try:
        results = {}
        for provider, model in models.items():
            results[provider] = await model.generate(prompt)

        logger.info("Successfully generated text from active models")
        return results

    except Exception as e:
        logger.error(f"Error generating text: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting MCP server")
    mcp.run("streamable-http") 