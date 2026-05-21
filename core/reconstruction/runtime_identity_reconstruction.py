from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


def _identity_hash(payload: Dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]


def reconstruct_runtime_identity(
    browser_identity: Optional[Dict[str, Any]] = None,
    session: Optional[Dict[str, Any]] = None,
    runtime_id: str = "",
    execution_id: str = "",
    worker_id: str = "",
) -> Dict[str, Any]:
    browser = dict(browser_identity or {})
    session_body = dict(session or {})

    browser_hash = _identity_hash({"browser": browser})
    session_hash = _identity_hash({"session": session_body})
    runtime_hash = _identity_hash({"runtime_id": runtime_id})
    execution_hash = _identity_hash({"execution_id": execution_id})
    worker_hash = _identity_hash({"worker_id": worker_id})

    return {
        "browser_identity": {**browser, "identity_hash": browser_hash},
        "session_identity": {**session_body, "identity_hash": session_hash},
        "runtime_identity": {"runtime_id": runtime_id, "identity_hash": runtime_hash},
        "execution_identity": {"execution_id": execution_id, "identity_hash": execution_hash},
        "worker_identity": {"worker_id": worker_id, "identity_hash": worker_hash},
        "continuity_hashes": sorted([browser_hash, session_hash, runtime_hash]),
        "bounded": True,
    }
