from __future__ import annotations

from typing import Any, List, Protocol


class EmbeddingAdapterProtocol(Protocol):
    def embed(self, texts: List[str]) -> List[List[float]]: ...
