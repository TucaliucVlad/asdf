# tools/llm_client.py
from litellm import completion
import os

def llm_call(
    messages: list,
    model: str = "groq/grok-beta",  # or "openai/gpt-4o", "anthropic/claude-3-5-sonnet", etc.
    max_tokens: int = 2000,
    temperature: float = 0.7,
    **kwargs
):
    api_key = os.getenv("GROK_API_KEY") if "grok" in model.lower() else None
    # Add other key mappings if needed

    response = completion(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key,
        **kwargs
    )
    return response.choices[0].message.content