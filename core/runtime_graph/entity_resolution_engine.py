from __future__ import annotations

import hashlib
from typing import Any, Dict


def resolve_canonical_entity(
    entity: Dict[str, Any],
) -> Dict[str, Any]:
    name = str(entity.get("name", "")).strip().lower()
    entity_type = str(entity.get("type", "")).strip().lower()

    canonical = f"{entity_type}:{name}"

    fingerprint = hashlib.sha256(
        canonical.encode("utf-8")
    ).hexdigest()

    return {
        "canonical_id": fingerprint,
        "canonical_key": canonical,
        "entity": entity,
        "bounded": True,
    }
