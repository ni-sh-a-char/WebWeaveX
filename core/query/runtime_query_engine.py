from __future__ import annotations

from typing import Any, Dict, List


def query_runtime_ir(runtime_ir: Dict[str, Any], field: str) -> Dict[str, Any]:
    value = runtime_ir.get(field)
    return {"field": field, "value": value, "found": value is not None, "deterministic": True}
