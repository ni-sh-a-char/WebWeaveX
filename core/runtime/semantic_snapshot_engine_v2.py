from __future__ import annotations

import hashlib
import json

from typing import Any
from typing import Dict


def create_runtime_snapshot(
    state: Dict[str, Any],
) -> Dict[str, Any]:

    payload = json.dumps(
        state,
        sort_keys=True,
        default=str,
    )

    fingerprint = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "state": state,
    }
