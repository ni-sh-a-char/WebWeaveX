from __future__ import annotations

from typing import Any, Dict

from core.memory.semantic_checkpoint_engine import create_semantic_checkpoint


def snapshot_semantic_state(state: Dict[str, Any]) -> Dict[str, Any]:
    cp = create_semantic_checkpoint(state)
    return {"snapshot": cp, "deterministic": True}
