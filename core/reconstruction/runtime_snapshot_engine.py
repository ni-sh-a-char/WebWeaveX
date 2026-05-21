from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value


def capture_reconstruction_snapshot(
    state: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "state": dict(state),
        "topology": dict(state.get("topology", {})),
        "identities": dict(state.get("identities", {})),
        "workflows": list(state.get("workflows", [])),
        "replay_chains": list(state.get("replay_chains", [])),
        "captured": True,
        "bounded": True,
    }


def restore_reconstruction_snapshot(
    snapshot: Dict[str, Any],
) -> Dict[str, Any]:
    body = snapshot.get("state", snapshot)
    return {
        "state": dict(body),
        "topology": dict(snapshot.get("topology", body.get("topology", {}))),
        "identities": dict(snapshot.get("identities", body.get("identities", {}))),
        "workflows": list(snapshot.get("workflows", body.get("workflows", []))),
        "replay_chains": list(snapshot.get("replay_chains", body.get("replay_chains", []))),
        "restored": True,
        "bounded": True,
    }


def save_reconstruction_snapshot(
    path: str,
    snapshot: Dict[str, Any],
    key: str,
) -> Dict[str, Any]:
    payload = json.dumps(snapshot, sort_keys=True)
    encrypted = encrypt_value(payload, key)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps({"encrypted": encrypted["encrypted"], "algorithm": "kaalka"}, sort_keys=True),
        encoding="utf-8",
    )
    return {"saved": True, "path": str(target), "algorithm": "kaalka", "bounded": True}


def load_reconstruction_snapshot(
    path: str,
    key: str,
) -> Dict[str, Any]:
    target = Path(path)
    if not target.exists():
        return {"available": False, "snapshot": _empty_snapshot(), "bounded": True}

    wrapper = json.loads(target.read_text(encoding="utf-8"))
    decrypted = decrypt_value(wrapper["encrypted"], key)
    snapshot = json.loads(decrypted["decrypted"])

    return {
        "available": True,
        "snapshot": snapshot,
        "algorithm": "kaalka",
        "bounded": True,
    }


def _empty_snapshot() -> Dict[str, Any]:
    return {
        "state": {},
        "topology": {},
        "identities": {},
        "workflows": [],
        "replay_chains": [],
        "bounded": True,
    }
