from __future__ import annotations

from typing import Any, Dict, List

from core.knowledge.semantic_identity_calculus import identity_hash


def resolve_semantic_identities(entities: List[str], namespace: str = "") -> Dict[str, Any]:
    resolved = [identity_hash(e, namespace) for e in entities or [] if e]
    by_id = {r["id"]: r["name"] for r in resolved}
    return {"entities": resolved, "index": by_id, "count": len(resolved)}
