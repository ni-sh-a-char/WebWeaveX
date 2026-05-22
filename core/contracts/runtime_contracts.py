from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class RuntimePhase(str, Enum):
    INGESTION = "ingestion"
    EXECUTION = "execution"
    SEMANTIC = "semantic"
    CAUSALITY = "causality"
    SYNCHRONIZATION = "synchronization"
    MEMORY = "memory"
    RECONSTRUCTION = "reconstruction"
    GRAPH = "graph"


@dataclass(frozen=True)
class UniversalInput:
    """Canonical ingress descriptor for the runtime pipeline."""

    source: str
    source_type: str = "auto"
    url: str = ""
    path: str = ""
    session: Optional[Dict[str, Any]] = None
    options: Dict[str, Any] = field(default_factory=dict)
    tick: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "source_type": self.source_type,
            "url": self.url,
            "path": self.path,
            "session": self.session or {},
            "options": dict(sorted(self.options.items())),
            "tick": self.tick,
            "bounded": True,
        }
