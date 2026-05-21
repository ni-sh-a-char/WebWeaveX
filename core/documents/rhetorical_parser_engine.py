from __future__ import annotations

from typing import Any, Dict

from core.documents.rhetorical_structure_engine import extract_rhetorical_structure
from core.documents.semantic_role_engine import assign_semantic_roles


def parse_rhetorical_structure(text: str) -> Dict[str, Any]:
    structure = extract_rhetorical_structure(text)
    roles = assign_semantic_roles(text)
    units = structure.get("units", [])
    role_map = {r["line"]: r["role"] for r in roles.get("roles", []) if "line" in r}
    enriched = []
    for u in units:
        enriched.append({**u, "role": role_map.get(u.get("line"), "nucleus" if u.get("type") == "heading" else "span")})
    return {
        "units": enriched,
        "unit_count": len(enriched),
        "roles": roles.get("roles", []),
        "rhetorical_roles": sorted(set(r.get("role", "") for r in enriched if r.get("role"))),
        "deterministic_inputs": structure.get("deterministic_inputs", []) + [f"roles={len(roles.get('roles', []))}"],
    }
