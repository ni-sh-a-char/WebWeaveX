from __future__ import annotations

from typing import Any, Dict, Protocol


class ReasoningAdapterProtocol(Protocol):
    def augment(self, bundle: Dict[str, Any]) -> Dict[str, Any]: ...
