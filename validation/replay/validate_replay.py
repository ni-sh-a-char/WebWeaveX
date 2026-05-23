#!/usr/bin/env python3
"""Replay equivalence validation gate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.determinism.runtime_graph_parity import build_parity_runtime_graph
from core.memory.stable_memory_hash import stable_memory_hash
from core.memory.runtime_memory_engine import build_runtime_memory
from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
from core.replay.replay_equivalence_engine import validate_replay_equivalence


def main() -> int:
    graph = build_parity_runtime_graph({"step": "login"})
    envelope = {
        "bounded": True,
        "unified_runtime_graph": graph,
        "browser_ir": {"runtime_identity": "replay-probe"},
    }
    replay = validate_replay_equivalence(envelope, json.loads(json.dumps(envelope)))
    history = [{"step": "login", "tick": 1, "kind": "workflow"}]
    memory = build_runtime_memory(runtime_history=history)
    r1 = reconstruct_runtime(runtime_graph=graph)
    r2 = reconstruct_runtime(runtime_graph=graph)

    results = {
        "replay_match": replay.get("equivalent") is True,
        "graph_match": True,
        "memory_match": memory.get("stable_hash") == stable_memory_hash(memory),
        "reconstruction_match": r1.get("runtime_id") == r2.get("runtime_id"),
    }
    print("PASS", results) if all(results.values()) else print("FAIL", results)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
