from __future__ import annotations

from typing import Any, Dict, Optional


class ProviderRegistry:
    _providers: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, adapter: Any) -> None:
        cls._providers[name] = adapter

    @classmethod
    def get(cls, name: str) -> Optional[Any]:
        return cls._providers.get(name)

    @classmethod
    def list_providers(cls) -> list:
        return sorted(cls._providers.keys())
