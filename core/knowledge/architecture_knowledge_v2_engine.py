from __future__ import annotations

from typing import Any, Dict


def build_architecture_knowledge_v2(architecture: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(architecture, dict):
        return {"components": 0, "evidence": "empty"}
    keys = sorted(architecture.keys())
    return {"components": len(keys), "keys": keys[:50], "evidence": "architecture_payload"}
