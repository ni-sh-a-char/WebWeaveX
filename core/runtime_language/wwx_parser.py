from __future__ import annotations

from typing import Any, Dict, List


def parse_wwx(source: str) -> Dict[str, Any]:
    statements: List[Dict[str, Any]] = []
    for index, line in enumerate(source.strip().splitlines()):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        verb = parts[0].upper()
        target = parts[1] if len(parts) > 1 else ""
        statements.append({
            "verb": verb,
            "target": target,
            "args": parts[2:],
            "line": index,
        })
    return {"statements": statements, "bounded": True}
