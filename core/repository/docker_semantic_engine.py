from __future__ import annotations

from typing import Any, Dict, List


def parse_dockerfile_semantics(
    text: str,
) -> Dict[str, Any]:

    instructions: List[Dict[str, Any]] = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#"):
            continue

        op = line.split()[0].upper()

        instructions.append({
            "instruction": op,
            "raw": line,
        })

    return {
        "instructions": instructions,
        "count": len(instructions),
        "grounded": True,
    }
