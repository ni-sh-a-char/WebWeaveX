from __future__ import annotations

from typing import Any, Dict, Optional

from core.integrations.capability_registry import supports_capability, supports_provider_capability
from core.integrations.provider_registry import ProviderRegistry


def route_augmentation(
    capability: str,
    provider: str | None = None,
) -> Optional[Any]:
    if provider:
        if not supports_provider_capability(provider, capability):
            return None
        return ProviderRegistry.get(provider)
    if supports_capability(capability):
        providers = ProviderRegistry.list_providers()
        return ProviderRegistry.get(providers[0]) if providers else None
    return None
