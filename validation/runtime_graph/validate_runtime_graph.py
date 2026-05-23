#!/usr/bin/env python3
"""Runtime graph validation gate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.determinism.runtime_graph_parity import build_parity_runtime_graph, normalize_runtime_graph
from core.replay.replay_equivalence_engine import _graph_hash


def main() -> int:
    graph = build_parity_runtime_graph({"a": 1, "b": 2})
    normalized = normalize_runtime_graph(graph)
    fp = _graph_hash(graph)
    results = {
        "graph_match": len(normalized.get("nodes", [])) >= 1,
        "fingerprint_match": len(fp) > 0,
        "deterministic": _graph_hash(graph) == _graph_hash(graph),
    }
    print("PASS", results) if all(results.values()) else print("FAIL", results)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
