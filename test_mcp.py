import asyncio
from main import generate_text

async def test_generation():
    try:
        result = await generate_text("Tell me a joke about programming")
        print("\nOpenAI Response:")
        print(result["openai"])
        print("\nGemini Response:")
        print(result["gemini"])
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_generation()) 