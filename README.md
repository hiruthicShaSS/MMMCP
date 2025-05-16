# Multi-Model MCP Server

This is an MCP server that generates text using both OpenAI's GPT-3.5 and Google's Gemini Pro models in parallel.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your API keys:
   - Set OPENAI_API_KEY environment variable for OpenAI
   - Set GOOGLE_API_KEY environment variable for Google Gemini

3. Configure models (optional):
   - Set OPENAI_MODEL to specify OpenAI model (default: gpt-3.5-turbo)
   - Set GEMINI_MODEL to specify Gemini model (default: gemini-pro)
   - Set FINAL_MODEL to enable response summarization (e.g., gemini-2.0-flash)

## Running the Server

```bash
python server.py
```

## Usage

The server exposes two tools:

### 1. generate_text

Generates text using all configured models:

```python
responses = await generate_text(prompt="Tell me a joke")
print("OpenAI response:", responses["openai"])
print("Gemini response:", responses["gemini"])
```

### 2. summarize_responses

Summarizes multiple model responses into a single coherent response (requires FINAL_MODEL to be configured):

```python
# First get responses from models
responses = await generate_text(prompt="Tell me a joke")

# Then optionally summarize them
summary_result = await summarize_responses(responses)
if "summary" in summary_result:
    print("Summarized response:", summary_result["summary"])
```

### Response Summarization

The `summarize_responses` tool is available when FINAL_MODEL is configured in your environment (e.g., FINAL_MODEL=gemini-2.0-flash). It takes a dictionary of responses and returns a dictionary with a 'summary' key containing a synthesized response.

If FINAL_MODEL is not configured, `summarize_responses` will return an empty dictionary.
