from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_schema(filename: str) -> dict:
    base = Path(__file__).parent / "contracts"
    return json.loads((base / filename).read_text(encoding="utf-8"))


def _check_type(expected: str, value: Any) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _validate(schema: dict, data: Any) -> bool:
    schema_type = schema.get("type")
    if isinstance(schema_type, str) and not _check_type(schema_type, data):
        return False

    if not isinstance(data, (dict, list)):
        return True

    if isinstance(data, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in data:
                return False

        properties = schema.get("properties", {})
        for key, value in data.items():
            if key in properties:
                if not _validate(properties[key], value):
                    return False
            elif schema.get("additionalProperties") is False:
                return False

    if isinstance(data, list):
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for item in data:
                if not _validate(item_schema, item):
                    return False

    return True


def validate_contract(data: Any, contract: str) -> bool:
    schema = _load_schema(contract)
    return _validate(schema, data)
