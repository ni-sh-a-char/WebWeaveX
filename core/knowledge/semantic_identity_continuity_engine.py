from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.semantic_identity_resolver import resolve_semantic_identities


def track_identity_continuity(entities_before: List[str], entities_after: List[str]) -> Dict[str, Any]:
    b = resolve_semantic_identities(entities_before)
    a = resolve_semantic_identities(entities_after)
    b_ids = {e["id"] for e in b.get("entities", [])}
    a_ids = {e["id"] for e in a.get("entities", [])}
    return {"continuous": sorted(b_ids & a_ids), "added": sorted(a_ids - b_ids), "removed": sorted(b_ids - a_ids)}
