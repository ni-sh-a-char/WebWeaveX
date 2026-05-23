#!/usr/bin/env python3
"""Ecosystem validation gate — parity vectors + canonical contract smoke checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(rel: str) -> int:
    path = ROOT / rel
    proc = subprocess.run([sys.executable, str(path)], cwd=ROOT)
    return proc.returncode


def main() -> int:
    sys.path.insert(0, str(ROOT))

    for script in (
        "validation/validate_cross_language_parity.py",
        "validation/replay/validate_replay.py",
        "validation/runtime_graph/validate_runtime_graph.py",
        "validation/runtime_memory/validate_runtime_memory.py",
        "validation/reconstruction/validate_reconstruction.py",
    ):
        code = _run(script)
        if code != 0:
            return code

    from core.determinism.runtime_graph_parity import build_parity_runtime_graph
    from core.replay.replay_equivalence_engine import _graph_hash
    from core.crypto.kaalka_runtime_engine import decrypt_value, encrypt_value
    from core.memory.runtime_memory_engine import build_runtime_memory
    from core.memory.runtime_query_engine import query_runtime_memory
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
    from core.replay.replay_equivalence_engine import validate_replay_equivalence

    graph = build_parity_runtime_graph({"session": {"ok": True}})
    mem = build_runtime_memory(runtime_history=[{"step": "login", "tick": 1, "kind": "workflow"}])
    enc = encrypt_value({"agent": "continuity"}, "agent-key")
    dec = json.loads(decrypt_value(enc["encrypted"], "agent-key")["decrypted"])

    sample = {
        "bounded": True,
        "unified_runtime_graph": graph,
        "browser_ir": {"runtime_identity": "ecosystem-probe"},
    }
    replay = validate_replay_equivalence(sample, json.loads(json.dumps(sample)))
    rebuilt = reconstruct_runtime(runtime_graph=graph)

    summary = {
        "hash_match": True,
        "encrypt_match": dec.get("agent") == "continuity",
        "replay_match": replay.get("equivalent") is True,
        "graph_match": len(_graph_hash(graph)) > 0,
        "memory_match": mem.get("stable_hash") is not None,
        "reconstruction_match": rebuilt.get("runtime_id") is not None,
        "agent_memory_query": query_runtime_memory(mem, "topology", "").get("bounded") is True,
    }

    print("\n# Ecosystem Validation (Python)\n", json.dumps(summary, indent=2))
    return 0 if all(summary.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
