from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class SemanticNode:
    id: str
    type: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class SemanticEdge:
    source: str
    target: str
    relation: str
    evidence: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ExecutionState:
    id: str
    state_type: str
    variables: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RuntimeTransition:
    from_state: str
    to_state: str
    transition_type: str
