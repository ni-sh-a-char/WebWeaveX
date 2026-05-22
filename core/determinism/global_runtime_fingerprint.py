from __future__ import annotations

import json
from typing import Any, Dict, Optional

from core.contracts.graph_contracts import RuntimeGraphContract
from core.crypto.kaalka_hash_engine import compute_kaalka_hash


def compute_global_runtime_fingerprint(
    extraction: Optional[Dict[str, Any]] = None,
    graph: Optional[Dict[str, Any]] = None,
    memory: Optional[Dict[str, Any]] = None,
    sync: Optional[Dict[str, Any]] = None,
    reconstruction: Optional[Dict[str, Any]] = None,
    kaalka_seal: str = "",
) -> str:
    """
    Cross-machine stable runtime fingerprint from canonical sorted payloads.
    """
    extraction = extraction or {}
    graph = RuntimeGraphContract.normalize(graph or extraction.get("unified_runtime_graph", {}))

    runtime = extraction.get("runtime", {})
    dom_hash = ""
    if isinstance(runtime, dict):
        dom_hash = str(
            runtime.get("dom_stabilization", {}).get("stabilized_hash", "")
            or runtime.get("spa_stabilization", {}).get("stable_dom_hash", "")
        )
    browser_ir = extraction.get("browser_ir", {})
    identity = browser_ir.get("runtime_identity", "") if isinstance(browser_ir, dict) else ""

    memory_block = {}
    if memory:
        memory_block = {
            "stable_hash": memory.get("stable_hash", memory.get("memory", {}).get("stable_hash", "")),
            "history_len": len(memory.get("memory", {}).get("runtime_history", [])),
        }

    canonical = {
        "dom_hash": dom_hash,
        "runtime_identity": identity,
        "graph_nodes": [n.get("id") for n in graph.get("nodes", [])],
        "graph_edges": [
            (e.get("source", e.get("from")), e.get("target", e.get("to")), e.get("type"))
            for e in graph.get("edges", [])
        ],
        "memory": memory_block,
        "sync_converged": (sync or {}).get("convergence", {}).get("converged"),
        "reconstruction_id": (reconstruction or {}).get("runtime", {}).get("runtime_id", ""),
        "kaalka_seal": kaalka_seal,
        "pipeline_hash": extraction.get("pipeline_hash", ""),
    }
    return compute_kaalka_hash(
        json.dumps(canonical, sort_keys=True, separators=(",", ":"))
    )
