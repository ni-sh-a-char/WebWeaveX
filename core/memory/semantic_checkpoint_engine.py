from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


MAX_CHECKPOINT_BYTES = 2_000_000


def create_semantic_checkpoint(state: Dict[str, Any]) -> Dict[str, Any]:
    encoded = json.dumps(state, sort_keys=True).encode("utf-8")

    bounded = encoded[:MAX_CHECKPOINT_BYTES]

    fingerprint = hashlib.sha256(bounded).hexdigest()

    return {
        "fingerprint": fingerprint,
        "size": len(bounded),
        "state": state,
        "deterministic": True,
    }
