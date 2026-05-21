from __future__ import annotations

from typing import Any, Dict, Protocol


class AugmentationProvider(Protocol):
  def augment(self, payload: Dict[str, Any]) -> Dict[str, Any]: ...


REQUIRED_METADATA_KEY = "llm"
