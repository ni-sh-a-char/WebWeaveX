"""WebWeaveX AI - Production-ready AI engine with retry."""

import json
import time
from typing import Dict, Any, Optional

from .config import DEFAULT_CONFIG, get_config


class AIEngine:
    """Production-ready AI engine with retry and fallback."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = get_config(config)
        self.ai_config = self.config.get("ai", DEFAULT_CONFIG["ai"])
        self.timeout = self.ai_config.get("timeout", 30)
        self.retries = self.ai_config.get("retries", 2)

    def call_model(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Call AI model with retry logic."""
        provider_config = self._get_provider_config(provider)
        
        if not provider_config:
            return self._mock_response(prompt)

        endpoint = provider_config.get("endpoint", "")
        api_key = provider_config.get("api_key")
        model = model or provider_config.get("model", "gpt-3.5-turbo")
        temperature = temperature if temperature is not None else provider_config.get("temperature", 0.0)
        max_tokens = max_tokens or provider_config.get("max_tokens", 1000)

        if not api_key:
            return self._mock_response(prompt)

        last_error = None
        for attempt in range(self.retries + 1):
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
            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    time.sleep(2 ** attempt)

        return self._mock_response(prompt)

    def _get_provider_config(self, provider: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get provider configuration."""
        providers = self.ai_config.get("providers", {})

        if provider and provider in providers:
            config = providers[provider].copy()
            config["api_key"] = self._get_api_key(provider)
            return config

        for name, config in providers.items():
            api_key = self._get_api_key(name)
            if api_key:
                result = config.copy()
                result["api_key"] = api_key
                result["name"] = name
                return result

        return None

    def _get_api_key(self, provider: str) -> Optional[str]:
        """Get API key from environment."""
        import os
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "groq": "GROQ_API_KEY",
            "ollama": None,
        }
        env_var = env_vars.get(provider)
        return os.environ.get(env_var) if env_var else None

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
        """Execute API call."""
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

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if provider == "ollama":
                return data.get("message", {}).get("content", "")
            
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")

    def _mock_response(self, prompt: str) -> str:
        """Return mock response when no API is configured."""
        truncated = prompt[:100] + "..." if len(prompt) > 100 else prompt
        return json.dumps({
            "status": "no_api",
            "message": "AI API not configured. Set API key for OpenAI, OpenRouter, Groq, or Ollama.",
            "prompt_received": truncated,
        }, sort_keys=True)
