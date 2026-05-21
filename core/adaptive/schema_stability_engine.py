from __future__ import annotations

from typing import Any, Dict, List


def stabilize_extraction_schema(
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    stabilized: Dict[str, Any] = {}

    for key in sorted(payload.keys()):
        value = payload[key]

        if isinstance(value, dict):
            stabilized[key] = stabilize_extraction_schema(value)
        elif isinstance(value, list):
            stabilized[key] = [
                stabilize_extraction_schema(item)
                if isinstance(item, dict)
                else item
                for item in value
            ]
        else:
            stabilized[key] = value

    return {
        "schema": stabilized,
        "fields": sorted(_collect_fields(stabilized)),
        "bounded": True,
    }


def _collect_fields(payload: Any, prefix: str = "") -> List[str]:
    fields: List[str] = []

    if isinstance(payload, dict):
        for key in sorted(payload.keys()):
            path = f"{prefix}.{key}" if prefix else str(key)
            fields.append(path)
            fields.extend(_collect_fields(payload[key], path))

    return fields
