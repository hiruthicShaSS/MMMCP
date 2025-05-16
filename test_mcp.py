"""Test script for MMMCP server"""

import asyncio
from main import generate_text, summarize_responses

async def test_generation():
    """Test text generation and summarization"""
    try:
        # Generate text from all models
        results = await generate_text("Tell me a joke about programming")
        print("\nModel Responses:")
        for provider, response in results.items():
            print(f"\n{provider.upper()} Response:")
            print(response)
            
        # Try to get a summary
        summary_result = await summarize_responses(results)
        if "summary" in summary_result:
            print("\nSummarized Response:")
            print(summary_result["summary"])
        else:
            print("\nNo summary available (FINAL_MODEL not configured)")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_generation()) 