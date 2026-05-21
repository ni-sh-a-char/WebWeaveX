from __future__ import annotations

from typing import Any, Dict

MAX_PAYLOAD_BYTES = 50_000_000
MAX_IR_COUNT = 10_000


def enforce_runtime_boundary(payload: Dict[str, Any]) -> Dict[str, Any]:
    import json

    size = len(json.dumps(payload, sort_keys=True, default=str))
    ir_count = len(payload.get("irs", []))
    return {
        "within_size": size <= MAX_PAYLOAD_BYTES,
        "within_ir_count": ir_count <= MAX_IR_COUNT,
        "size": size,
        "ir_count": ir_count,
        "bounded": True,
    }
