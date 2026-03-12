# tools/llm_client.py
# Version: 3.0 - Switched to xAI Grok (your $50 credits)

from litellm import completion
import os

def llm_call(
    messages: list,
    model: str = "xai/grok-3-mini-beta",  # ← official xAI model via LiteLLM (fast + cheap)
    max_tokens: int = 4000,
    temperature: float = 0.7,
    **kwargs
):
    # Correct key for xAI
    if "xai" in model.lower():
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("❌ XAI_API_KEY is missing in .env file! (use your Grok/xAI key)")
    else:
        api_key = None

    response = completion(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key,
        **kwargs
    )
    return response.choices[0].message.content