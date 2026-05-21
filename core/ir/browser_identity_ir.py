from __future__ import annotations

from typing import Any, Dict


def compile_browser_identity_ir(
    identity: Dict[str, Any],
    entropy: Dict[str, Any],
    replay: Dict[str, Any],
) -> Dict[str, Any]:
    return {
        "ir": "browser_identity_runtime",
        "identity_profile": identity,
        "entropy_state": entropy,
        "navigator_runtime": identity.get("navigator", {}),
        "replay_metadata": replay,
        "fingerprint_hashes": {
            "identity": identity.get("fingerprint_hash", ""),
            "entropy": entropy.get("baseline_hash", ""),
        },
        "bounded": True,
    }


def browser_identity_ir_to_runtime_graph(
    identity_ir: Dict[str, Any],
) -> Dict[str, Any]:
    identity = identity_ir.get("identity_profile", {})
    node_id = str(identity.get("fingerprint_hash", "browser_identity"))

    return {
        "ir": "browser_identity_graph",
        "nodes": [
            {
                "id": node_id,
                "type": "browser_identity",
                "name": identity.get("profile_id", "default"),
            }
        ],
        "edges": [],
        "bounded": True,
    }
