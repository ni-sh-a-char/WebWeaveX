"""WebWeaveX Providers - AI provider configuration."""

from typing import Dict, Any, Optional

from .config import DEFAULT_CONFIG, get_config


class ProviderRegistry:
    """Registry for AI providers."""

    def __init__(self):
        self._providers: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, config: Dict[str, Any]) -> None:
        self._providers[name] = config

    def get(self, name: str) -> Optional[Dict[str, Any]]:
        return self._providers.get(name)

    def list_providers(self) -> list:
        return list(self._providers.keys())


class ProviderConfig:
    """AI provider configuration manager."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = get_config(config)
        self.registry = ProviderRegistry()
        self._load_defaults()

    def _load_defaults(self) -> None:
        ai_config = self.config.get("ai", DEFAULT_CONFIG["ai"])
        providers = ai_config.get("providers", {})
        for name, cfg in providers.items():
            self.registry.register(name, cfg)

    def register_provider(self, name: str, provider_config: Dict[str, Any]) -> None:
        self.registry.register(name, provider_config)

    def get_provider(self, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if name:
            return self.registry.get(name)
        return None
