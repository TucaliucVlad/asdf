# tools/llm_client.py
# Version: 4.0 — Upgraded to grok-code-fast-1 (256k context) per xAI console

from litellm import completion
import os

def llm_call(
    messages: list,
    model: str = "xai/grok-code-fast-1",   # ← BEST for coding (your console list)
    max_tokens: int = 32000,               # ← was 4000 — now plenty
    temperature: float = 0.2,              # ← balanced (agents override some)
    **kwargs
):
    # Correct key for xAI
    if "xai" in model.lower():
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY is missing in .env file! (use your Grok/xAI key)")
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