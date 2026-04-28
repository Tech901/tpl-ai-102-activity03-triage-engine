"""Endpoint normalization for azure.ai.inference.ChatCompletionsClient.

The azure-ai-inference SDK does NOT auto-append /openai/deployments/<name>
to a base Azure OpenAI endpoint the way openai.AzureOpenAI does. This helper
tolerates whichever form a student has configured and returns a fully
qualified endpoint URL suitable for ChatCompletionsClient.
"""
import os


def inference_endpoint() -> str:
    """Return a ChatCompletionsClient-ready endpoint URL.

    Accepts any of:
      - https://<res>.openai.azure.com/                             (base)
      - https://<res>.openai.azure.com/openai/deployments/<deploy>  (full)
      - https://<res>.services.ai.azure.com/models                  (Foundry)
      - https://<res>.cognitiveservices.azure.com/                  (multi-service)

    Raises:
        KeyError: if AZURE_OPENAI_ENDPOINT is unset.
    """
    base = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    if "/deployments/" in base or base.endswith("/models"):
        return base
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    return f"{base}/openai/deployments/{deployment}"
