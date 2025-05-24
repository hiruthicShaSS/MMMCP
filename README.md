# Multi-Model MCP Server

This is an MCP server that generates text using both OpenAI's GPT-3.5 and Google's Gemini Pro models in parallel.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
   1. Set up your API keys:
      - Set OPENAI_API_KEY environment variable for OpenAI
      - Set GOOGLE_API_KEY environment variable for Google Gemini
   
   2. Set models:
      - ACTIVE_PROVIDERS=openai,gemini,nvidia
   
   3. Model Selection
      - OPENAI_MODEL=gpt-3.5-turbo
      - GEMINI_MODEL=gemini-2.0-flash
      - FINAL_MODEL=gemini-2.0-flash

## Running the Server

```bash
python server.py
```

## Usage

The server exposes a tool called `generate_text` that takes a prompt and returns responses from both models:

```python
response = await generate_text(prompt="Tell me a joke")
print("OpenAI response:", response["openai"])
print("Gemini response:", response["gemini"])
```
