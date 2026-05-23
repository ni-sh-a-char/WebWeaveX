#!/usr/bin/env python3
"""Runtime memory validation gate."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from core.memory.runtime_merge_engine import merge_runtime_memories
from core.memory.stable_memory_hash import stable_memory_hash
from core.memory.runtime_memory_engine import build_runtime_memory
from core.memory.runtime_query_engine import query_runtime_memory


def main() -> int:
    history = [{"step": 1, "kind": "workflow", "tick": 1}]
    mem = build_runtime_memory(runtime_history=history)
    merged = merge_runtime_memories([mem, mem])
    query = query_runtime_memory(mem, "topology", "")

    results = {
        "memory_match": mem.get("stable_hash") == stable_memory_hash(mem),
        "query_match": query.get("bounded") is True,
        "merge_match": merged.get("bounded") is True,
        "deterministic": mem.get("stable_hash")
        == build_runtime_memory(runtime_history=history).get("stable_hash"),
    }
    print("PASS", results) if all(results.values()) else print("FAIL", results)
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
