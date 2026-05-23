#!/usr/bin/env python3
"""Reconstruction validation gate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.determinism.runtime_graph_parity import build_parity_runtime_graph
from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime


def main() -> int:
    graph = build_parity_runtime_graph({"probe": True})
    r1 = reconstruct_runtime(runtime_graph=graph)
    r2 = reconstruct_runtime(runtime_graph=graph)
    results = {
        "reconstruction_match": r1.get("runtime_id") == r2.get("runtime_id"),
        "bounded": r1.get("bounded") is True,
    }
    print("PASS", results) if all(results.values()) else print("FAIL", results)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
