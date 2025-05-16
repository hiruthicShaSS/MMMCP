# Multi-Model MCP Server

This is an MCP server that generates text using both OpenAI's GPT-3.5 and Google's Gemini Pro models in parallel.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
NVIDIA_API_KEY=your_nvidia_api_key  # Optional

# Model Configuration
OPENAI_MODEL=gpt-3.5-turbo  # Options: gpt-3.5-turbo, gpt-4
GEMINI_MODEL=gemini-2.0-flash  # Options: gemini-2.0-flash
FINAL_MODEL=gemini-2.0-flash  # Optional: Model to use for summarization

# Provider Configuration
ACTIVE_PROVIDERS=openai,gemini  # Comma-separated list of active providers
```

### Environment Variables

| Variable | Required | Default | Description | Options |
|----------|----------|---------|-------------|----------|
| OPENAI_API_KEY | Yes | - | OpenAI API key | - |
| GOOGLE_API_KEY | Yes | - | Google API key | - |
| NVIDIA_API_KEY | No | None | NVIDIA API key | - |
| OPENAI_MODEL | No | gpt-3.5-turbo | OpenAI model to use | gpt-3.5-turbo, gpt-4 |
| GEMINI_MODEL | No | gemini-2.0-flash | Gemini model to use | gemini-2.0-flash |
| FINAL_MODEL | No | None | Model to use for summarization | Any model from OpenAI or Gemini |
| ACTIVE_PROVIDERS | No | openai,gemini | Active model providers | openai, gemini, nvidia |

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
