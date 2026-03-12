# tools/token_counter.py
# Version: 1.0 - Phase 2

from litellm import token_counter
from typing import List, Dict

def count_tokens(messages: List[Dict[str, str]], model: str = "groq/grok-beta") -> int:
    try:
        return token_counter(model=model, messages=messages)
    except Exception:
        # Rough fallback
        total = sum(len(msg.get("content", "")) // 4 + 10 for msg in messages)
        return total + 50  # overhead


def estimate_cost(
    input_tokens: int,
    output_estimate: int = 0,
    model: str = "groq/grok-beta"
) -> float:
    if "grok" in model.lower():
        return round((input_tokens / 1e6 * 0.20) + (output_estimate / 1e6 * 0.50), 6)
    # Add more providers later
    return round((input_tokens + output_estimate) / 1e6 * 1.0, 6)