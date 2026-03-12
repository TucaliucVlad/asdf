# tools/cost_preview.py
def estimate_cost(tokens_in: int = 2000, tokens_out: int = 1000, model: str = "grok-4.1-fast") -> float:
    # Real prices March 2026: Grok 4.1 Fast ~ $0.20/M input, $0.50/M output
    if "grok" in model.lower():
        cost = (tokens_in / 1_000_000 * 0.20) + (tokens_out / 1_000_000 * 0.50)
    else:
        cost = 0.01  # placeholder
    return round(cost, 4)