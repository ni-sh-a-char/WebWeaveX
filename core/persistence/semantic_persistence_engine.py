from __future__ import annotations

import hashlib
import json

from typing import Any, Dict


def persist_semantic_ir(
    ir: Dict[str, Any],
) -> Dict[str, Any]:

    encoded = json.dumps(
        ir,
        sort_keys=True,
        default=str,
    )

    fingerprint = hashlib.sha256(
        encoded.encode("utf-8")
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "bytes": len(encoded),
        "persisted": True,
    }
