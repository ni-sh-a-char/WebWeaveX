from __future__ import annotations

from typing import Any, Dict, Protocol


class LLMAdapterProtocol(Protocol):
    def complete(self, prompt: str, **kwargs: Any) -> Dict[str, Any]: ...
