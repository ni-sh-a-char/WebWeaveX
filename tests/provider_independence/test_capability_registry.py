from core.integrations.capability_registry import (
    CapabilityRegistry,
    supports_capability,
    supports_provider_capability,
)


def test_provider_registers_capabilities():
    CapabilityRegistry.register("cap_provider", {"semantic_summarization"})
    assert supports_provider_capability("cap_provider", "semantic_summarization") is True
    assert supports_capability("semantic_summarization") is False


def test_provider_capability_isolated():
    CapabilityRegistry.register("p1", {"semantic_embedding"})
    assert supports_provider_capability("p1", "semantic_embedding") is True
    assert supports_provider_capability("p1", "semantic_summarization") is False
