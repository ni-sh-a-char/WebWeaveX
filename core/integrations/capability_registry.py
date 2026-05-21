from __future__ import annotations

from typing import Dict, Set

CAPABILITIES = {
    "semantic_summarization",
    "semantic_embedding",
    "semantic_reasoning_augment",
}


class CapabilityRegistry:
    _providers: Dict[str, Set[str]] = {}
    _global: Set[str] = set()

    @classmethod
    def register(cls, provider_or_capability: str, capabilities: Set[str] | None = None) -> None:
        if capabilities is not None:
            cls._providers[provider_or_capability] = set(
                sorted(c for c in capabilities if c in CAPABILITIES)
            )
        elif provider_or_capability in CAPABILITIES:
            cls._global.add(provider_or_capability)

    @classmethod
    def supports(cls, capability: str) -> bool:
        return capability in cls._global

    @classmethod
    def supports_provider(cls, provider: str, capability: str) -> bool:
        return capability in cls._providers.get(provider, set())


REGISTRY = CapabilityRegistry()


def supports_capability(capability: str) -> bool:
    return CapabilityRegistry.supports(capability)


def supports_provider_capability(provider: str, capability: str) -> bool:
    return CapabilityRegistry.supports_provider(provider, capability)
