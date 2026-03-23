"""AI providers configuration for WebWeaveX."""

from typing import Dict, Any, Optional, Callable
import os

from .utils import get_spec


class ProviderRegistry:
    """Registry for AI providers."""

    def __init__(self):
        """Initialize the registry."""
        self._providers: Dict[str, Dict[str, Any]] = {}
        self._defaults = {}

    def register(self, name: str, config: Dict[str, Any]) -> None:
        """Register an AI provider."""
        self._providers[name] = config

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get provider configuration."""
        return self._providers.get(name)

    def get_default(self) -> Optional[Dict[str, Any]]:
        """Get the default provider."""
        if not self._defaults:
            spec = get_spec()
            ai_config = spec.get("ai", {})
            providers = ai_config.get("providers", {})
            
            for name, config in providers.items():
                api_key = self._get_api_key(name, config)
                if api_key:
                    self._defaults[name] = config.copy()
                    self._defaults[name]["api_key"] = api_key
                    break
        
        return self._defaults.get(next(iter(self._defaults), None))

    def _get_api_key(self, name: str, config: Dict[str, Any]) -> Optional[str]:
        """Get API key from environment."""
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
            "groq": "GROQ_API_KEY",
            "ollama": None,
        }
        
        env_var = env_vars.get(name)
        if env_var:
            return os.environ.get(env_var)
        
        return None

    def list_providers(self) -> list:
        """List available providers."""
        return list(self._providers.keys())


class ProviderConfig:
    """AI provider configuration manager."""

    def __init__(self):
        """Initialize the config."""
        self.registry = ProviderRegistry()
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default provider configurations."""
        spec = get_spec()
        ai_config = spec.get("ai", {})
        providers = ai_config.get("providers", {})
        
        for name, config in providers.items():
            self.registry.register(name, config)

    def register_provider(self, name: str, config: Dict[str, Any]) -> None:
        """Register a custom provider."""
        self.registry.register(name, config)

    def get_provider(self, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get provider configuration by name."""
        if name:
            return self.registry.get(name)
        return self.registry.get_default()
