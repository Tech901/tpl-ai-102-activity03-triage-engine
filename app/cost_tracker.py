"""
Activity 3 - 311 Triage Engine: Token Usage & Cost Tracker
AI-102: Optimize and operationalize (2.3) - monitoring, tracing

Your task: Track token usage from API responses and calculate the
dollar cost of running the classifier at scale.
"""
from app.utils import load_pricing


# ---------------------------------------------------------------------------
# TODO: Step 5 - Implement token counting from a single API response
# ---------------------------------------------------------------------------
def extract_token_usage(response) -> dict:
    """Extract token counts from an Azure AI Inference API response.

    The response object has a `.usage` attribute with:
        - response.usage.prompt_tokens (int)
        - response.usage.completion_tokens (int)

    Args:
        response: The ChatCompletions response object from azure-ai-inference.

    Returns:
        Dict with keys: prompt_tokens, completion_tokens, total_tokens.

    Example:
        >>> usage = extract_token_usage(response)
        >>> usage
        {'prompt_tokens': 127, 'completion_tokens': 42, 'total_tokens': 169}
    """
    # TODO: Implement this function.
    #   1. Read response.usage.prompt_tokens
    #   2. Read response.usage.completion_tokens
    #   3. Calculate total_tokens = prompt_tokens + completion_tokens
    #   4. Return the dict
    #
    # Hint: If response or response.usage is None, return zeros.
    raise NotImplementedError("Implement extract_token_usage() in Step 5")


# ---------------------------------------------------------------------------
# TODO: Step 5 - Implement cost calculation
# ---------------------------------------------------------------------------
def calculate_cost(
    prompt_tokens: int,
    completion_tokens: int,
    model: str = "gpt-4o",
    pricing: dict | None = None,
) -> float:
    """Calculate the dollar cost for a given number of tokens.

    Cost formula:
        cost = (prompt_tokens / 1000 * input_price_per_1k)
             + (completion_tokens / 1000 * output_price_per_1k)

    Args:
        prompt_tokens: Number of input/prompt tokens.
        completion_tokens: Number of output/completion tokens.
        model: Model name to look up in pricing data (default "gpt-4o").
        pricing: Optional pricing dict. If None, loads from data/pricing.json.

    Returns:
        Float representing the cost in US dollars.

    Raises:
        KeyError: If the model name is not found in pricing data.

    Example:
        >>> calculate_cost(1000, 500, model="gpt-4o")
        0.0075
    """
    # TODO: Implement this function.
    #   1. Load pricing data if not provided (use load_pricing())
    #   2. Look up the model's input and output prices
    #   3. Apply the cost formula
    #   4. Return the dollar amount as a float
    raise NotImplementedError("Implement calculate_cost() in Step 5")


# ---------------------------------------------------------------------------
# TODO: Step 5 - Implement cumulative cost tracking
# ---------------------------------------------------------------------------
class CostTracker:
    """Tracks cumulative token usage and cost across multiple API calls.

    Usage:
        tracker = CostTracker(model="gpt-4o")
        tracker.record(prompt_tokens=127, completion_tokens=42)
        tracker.record(prompt_tokens=130, completion_tokens=38)
        print(tracker.summary())
    """

    def __init__(self, model: str = "gpt-4o"):
        """Initialize the cost tracker.

        Args:
            model: The model name for pricing lookups.
        """
        self.model = model
        # TODO: Initialize tracking variables:
        #   self.total_prompt_tokens = 0
        #   self.total_completion_tokens = 0
        #   self.total_cost = 0.0
        #   self.call_count = 0
        #   self._pricing = load_pricing()
        raise NotImplementedError("Implement CostTracker.__init__() in Step 5")

    def record(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Record token usage from one API call and return its cost.

        Args:
            prompt_tokens: Number of input tokens for this call.
            completion_tokens: Number of output tokens for this call.

        Returns:
            Float cost in dollars for this single call.
        """
        # TODO: Implement this method.
        #   1. Calculate cost for this call using calculate_cost()
        #   2. Add tokens to running totals
        #   3. Add cost to running total
        #   4. Increment call_count
        #   5. Return the cost of this single call
        raise NotImplementedError("Implement CostTracker.record() in Step 5")

    def summary(self) -> dict:
        """Return a summary of all tracked costs.

        Returns:
            Dict with keys: model, call_count, total_prompt_tokens,
            total_completion_tokens, total_tokens, total_cost,
            avg_prompt_tokens, avg_completion_tokens, avg_cost_per_call.
        """
        # TODO: Implement this method.
        #   1. Calculate averages (handle zero call_count)
        #   2. Return the summary dict
        raise NotImplementedError("Implement CostTracker.summary() in Step 5")

    def estimate_monthly_cost(self, calls_per_day: int) -> float:
        """Estimate monthly cost based on average cost per call.

        Args:
            calls_per_day: Expected number of API calls per day.

        Returns:
            Estimated monthly cost in dollars (assumes 30 days/month).
        """
        # TODO: Implement this method.
        #   1. Calculate average cost per call from totals
        #   2. Multiply by calls_per_day * 30
        #   3. Return the estimate (0.0 if no calls recorded yet)
        raise NotImplementedError("Implement CostTracker.estimate_monthly_cost() in Step 5")
