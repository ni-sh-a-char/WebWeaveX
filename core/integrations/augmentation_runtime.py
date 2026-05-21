from __future__ import annotations

from typing import Any, Dict

from core.integrations.capability_registry import supports_capability, supports_provider_capability


def augment_metadata(
    bundle: Dict[str, Any],
    capability: str,
    provider_result: Dict[str, Any] | None = None,
    provider: str | None = None,
) -> Dict[str, Any]:
    """LLM/provider output isolated under metadata['llm'] only."""
    meta = dict(bundle.get("metadata", {}) or {})
    llm = dict(meta.get("llm", {}) or {})
    enabled = (
        supports_provider_capability(provider, capability)
        if provider
        else supports_capability(capability)
    )
    if enabled and provider_result:
        llm[capability] = provider_result
    meta["llm"] = llm
    return {**bundle, "metadata": meta}
