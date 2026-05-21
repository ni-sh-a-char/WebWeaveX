from __future__ import annotations

from typing import Any, Dict, List


def resolve_semantic_references(refs: List[Dict[str, Any]]) -> Dict[str, Any]:
    resolved = []
    for ref in sorted(refs, key=lambda r: str(r.get("target", ""))):
        resolved.append(
            {
                "source": ref.get("source"),
                "target": ref.get("target"),
                "resolved": bool(ref.get("target")),
            }
        )
    return {"references": resolved, "count": len(resolved), "deterministic": True}
