from __future__ import annotations

from typing import Any, Dict, List


def synchronize_adaptive_runtime(
    adaptive_states: List[Dict[str, Any]],
) -> Dict[str, Any]:
    healed: Dict[str, str] = {}
    pagination: List[str] = []
    modals: List[Dict[str, Any]] = []
    schemas: List[List[str]] = []

    for state in adaptive_states:
        memory = state.get("memory", state.get("adaptive_runtime", {}))
        healed.update(memory.get("healed_selectors", {}))
        pagination.extend(memory.get("pagination_patterns", []))
        modals.extend(memory.get("modal_solutions", []))
        schema = state.get("schema", {})
        schemas.append(list(schema.get("fields", [])))

    stable_fields = sorted(set(
        field
        for fields in schemas
        for field in fields
    ))

    return {
        "healed_selectors": dict(sorted(healed.items())),
        "pagination_patterns": sorted(set(pagination)),
        "modal_solutions": modals[:1000],
        "stable_schema_fields": stable_fields,
        "bounded": True,
    }
