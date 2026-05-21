#!/usr/bin/env python3
"""V25 — remove all version-namespace trees; canonical-only imports."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"

RMTREE = [
    "repository/architecture_v2",
    "documents/intelligence_v4",
    "documents/intelligence_v3",
    "universal/v2",
    "universal/v3",
    "universal/v4",
    "graph/v6",
    "graph/v7",
    "serialize/v4",
    "serialize/v5",
    "crypto/v2",
    "crypto/v3",
    "llm/v2",
    "llm/v3",
    "llm/v4",
    "distributed/v2",
    "crawling/v3",
    "knowledge/v2",
    "performance/v2",
]


def main() -> None:
    removed = []
    for rel in RMTREE:
        target = CORE / rel.replace("/", "\\") if "\\" in str(CORE) else CORE / rel
        if target.exists():
            shutil.rmtree(target)
            removed.append(rel)
    print(f"removed {len(removed)} namespace trees")
    for r in removed:
        print(" ", r)


if __name__ == "__main__":
    main()
