from __future__ import annotations

import hashlib
from typing import Any, Dict


def identity_hash(name: str, namespace: str = "") -> Dict[str, Any]:
    raw = f"{namespace}:{name}".encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()[:16]
    return {
        "name": name,
        "namespace": namespace,
        "id": digest,
        "deterministic_inputs": [f"name={name}", f"namespace={namespace}"],
    }
