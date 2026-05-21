from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


def build_runtime_action(
    action_type: str,
    runtime: str,
    payload: Optional[Dict[str, Any]] = None,
    tick: int = 0,
) -> Dict[str, Any]:
    payload = dict(payload or {})
    canonical = json.dumps(
        {"runtime": runtime, "action_type": action_type, "payload": payload, "tick": tick},
        sort_keys=True,
    )
    action_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]

    return {
        "id": action_id,
        "runtime": runtime,
        "action_type": action_type,
        "payload": payload,
        "timestamp": tick,
        "bounded": True,
    }
