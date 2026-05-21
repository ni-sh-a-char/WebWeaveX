from __future__ import annotations

from core.llm.base_adapter import disabled_result


def complete(prompt: str, **kwargs):
    return disabled_result('transformers', "optional_adapter_not_configured")
