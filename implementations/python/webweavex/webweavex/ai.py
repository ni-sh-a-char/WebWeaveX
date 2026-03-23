"""AI engine for WebWeaveX."""

from typing import Dict, Any, Optional
import json

from .providers import ProviderConfig
from .utils import get_spec


class AIEngine:
    """AI engine for model calls with multiple provider support."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the AI engine."""
        self.spec = config or get_spec()
        self.provider_config = ProviderConfig()
        self._client = None

    def register_provider(self, name: str, provider_config: Dict[str, Any]) -> None:
        """Register a new AI provider."""
        self.provider_config.register_provider(name, provider_config)

    def call_model(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Call AI model with prompt."""
        provider_config = self.provider_config.get_provider(provider)
        
        if not provider_config:
            return self._mock_response(prompt)

        endpoint = provider_config.get("endpoint")
        api_key = provider_config.get("api_key")
        model = model or provider_config.get("model", "gpt-3.5-turbo")
        temperature = temperature if temperature is not None else provider_config.get("temperature", 0.0)
        max_tokens = max_tokens or provider_config.get("max_tokens", 1000)

        if not api_key:
            return self._mock_response(prompt)

        try:
            return self._call_api(
                endpoint=endpoint,
                api_key=api_key,
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                provider=provider,
                **kwargs
            )
        except Exception:
            return self._mock_response(prompt)

    def _call_api(
        self,
        endpoint: str,
        api_key: str,
        model: str,
        prompt: str,
        temperature: float,
        max_tokens: int,
        provider: Optional[str] = None,
        **kwargs
    ) -> str:
        """Call the AI API."""
        import httpx

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        messages = [{"role": "user", "content": prompt}]

        if provider == "ollama":
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
            }
        else:
            payload = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if provider == "ollama":
                return data.get("message", {}).get("content", "")
            
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def _mock_response(self, prompt: str) -> str:
        """Return a mock response when no API is available."""
        return json.dumps({
            "status": "no_api",
            "message": "AI API not configured. Set API key for OpenAI, OpenRouter, Groq, or Ollama.",
            "prompt_received": prompt[:100] + "..." if len(prompt) > 100 else prompt,
        }, sort_keys=True)

    async def call_model_async(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Call AI model asynchronously."""
        return self.call_model(prompt, provider, model, temperature, max_tokens, **kwargs)
