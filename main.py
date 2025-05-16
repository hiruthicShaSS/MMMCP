"""MMMCP Server - Main application"""

import logging
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from typing import Dict
from mmmcp.services import TextGenerationService

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Environment variables loaded")

mcp = FastMCP("MMMCP", "A MCP server that can run the prompt in multiple LLMs at a time.")
logger.info("MCP Server initialized")

service = TextGenerationService()

@mcp.tool()
async def generate_text(prompt: str) -> Dict[str, str]:
    """Generate text using configured AI models
    
    Args:
        prompt: Input prompt
        
    Returns:
        Dictionary mapping provider names to their responses
    """
    return await service.generate_text(prompt)

@mcp.tool()
async def summarize_responses(responses: Dict[str, str]) -> Dict[str, str]:
    """Summarize multiple model responses
    
    Args:
        responses: Dictionary of model responses to summarize
        
    Returns:
        Dictionary containing the summary if final model is configured
    """
    return await service.summarize_responses(responses)

if __name__ == "__main__":
    logger.info("Starting MCP server")
    mcp.run("streamable-http") 