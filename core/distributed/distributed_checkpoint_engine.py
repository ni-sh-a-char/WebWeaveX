from __future__ import annotations

import hashlib
import json

from typing import Any, Dict


def create_distributed_checkpoint(
    state: Dict[str, Any],
) -> Dict[str, Any]:

    serialized = json.dumps(
        state,
        sort_keys=True,
        default=str,
    )

    fingerprint = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "state": state,
    }
