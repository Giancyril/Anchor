from typing import Dict, Any, List
from pydantic import BaseModel

class ModelPricing(BaseModel):
    model: str
    provider: str
    input_cost_per_1m: float
    output_cost_per_1m: float

class CostTracker:
    """
    Tracks token consumption and USD costs across embedding and LLM synthesis calls.
    """
    PRICING_CATALOG: Dict[str, ModelPricing] = {
        "text-embedding-3-small": ModelPricing(
            model="text-embedding-3-small",
            provider="OpenAI",
            input_cost_per_1m=0.02,
            output_cost_per_1m=0.0,
        ),
        "text-embedding-3-large": ModelPricing(
            model="text-embedding-3-large",
            provider="OpenAI",
            input_cost_per_1m=0.13,
            output_cost_per_1m=0.0,
        ),
        "gpt-4o-mini": ModelPricing(
            model="gpt-4o-mini",
            provider="OpenAI",
            input_cost_per_1m=0.15,
            output_cost_per_1m=0.60,
        ),
        "gpt-4o": ModelPricing(
            model="gpt-4o",
            provider="OpenAI",
            input_cost_per_1m=2.50,
            output_cost_per_1m=10.00,
        ),
        "claude-3-5-sonnet": ModelPricing(
            model="claude-3-5-sonnet",
            provider="Anthropic",
            input_cost_per_1m=3.00,
            output_cost_per_1m=15.00,
        ),
    }

    def __init__(self):
        self.total_input_tokens: int = 0
        self.total_output_tokens: int = 0
        self.total_cost_usd: float = 0.0
        self.total_calls: int = 0

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int = 0) -> float:
        pricing = self.PRICING_CATALOG.get(model, self.PRICING_CATALOG["gpt-4o-mini"])
        in_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_1m
        out_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_1m
        return in_cost + out_cost

    def record_call(self, model: str, input_tokens: int, output_tokens: int = 0) -> float:
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd += cost
        self.total_calls += 1
        return cost

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_calls": self.total_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6),
            "pricing_catalog": [p.dict() for p in self.PRICING_CATALOG.values()],
        }

cost_tracker = CostTracker()