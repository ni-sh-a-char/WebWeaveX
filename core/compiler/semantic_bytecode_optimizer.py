from __future__ import annotations

from typing import Any, Dict, List, Set


def optimize_semantic_bytecode(
    instructions: List[Dict[str, Any]],
) -> Dict[str, Any]:

    optimized = []

    seen: Set[str] = set()

    for instruction in instructions:
        fingerprint = str(instruction)

        if fingerprint in seen:
            continue

        seen.add(fingerprint)

        optimized.append(instruction)

    return {
        "instructions": optimized,
        "optimized": True,
    }
