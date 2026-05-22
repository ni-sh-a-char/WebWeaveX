from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from core.contracts.graph_contracts import RuntimeGraphContract
from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.global_runtime_fingerprint import compute_global_runtime_fingerprint


def _graph_hash(graph: Dict[str, Any]) -> str:
    normalized = RuntimeGraphContract.normalize(graph)
    return compute_kaalka_hash(
        json.dumps(
            {"nodes": normalized.get("nodes", []), "edges": normalized.get("edges", [])},
            sort_keys=True,
            default=str,
        )
    )


def validate_replay_equivalence(
    original: Dict[str, Any],
    replayed: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Verify replay restored equivalent runtime graphs and fingerprints.
    """
    orig_graph = original.get("unified_runtime_graph", original.get("graph", {}))
    replay_graph = replayed.get("unified_runtime_graph", replayed.get("graph", {}))

    orig_fp = compute_global_runtime_fingerprint(original, graph=orig_graph)
    replay_fp = compute_global_runtime_fingerprint(replayed, graph=replay_graph)

    checks: List[Dict[str, Any]] = [
        {
            "name": "graph_hash",
            "ok": _graph_hash(orig_graph) == _graph_hash(replay_graph),
            "original": _graph_hash(orig_graph)[:16],
            "replay": _graph_hash(replay_graph)[:16],
        },
        {
            "name": "global_fingerprint",
            "ok": orig_fp == replay_fp,
            "original": orig_fp[:16],
            "replay": replay_fp[:16],
        },
        {
            "name": "browser_identity",
            "ok": (
                original.get("browser_ir", {}).get("runtime_identity")
                == replayed.get("browser_ir", {}).get("runtime_identity")
            ),
        },
    ]

    return {
        "equivalent": all(c["ok"] for c in checks),
        "checks": checks,
        "bounded": True,
    }
