from __future__ import annotations

import re
from typing import Any, Dict, List


def extract_rhetorical_structure(text: str) -> Dict[str, Any]:
    """RST-lite: headings, lists, code blocks as rhetorical units."""
    lines = (text or "").splitlines()
    units: List[Dict[str, Any]] = []
    for i, ln in enumerate(lines):
        if m := re.match(r"^(#{1,6})\s+(.+)$", ln.strip()):
            units.append({"type": "heading", "level": len(m.group(1)), "title": m.group(2), "line": i})
        elif re.match(r"^[-*]\s+", ln.strip()):
            units.append({"type": "list_item", "line": i})
        elif ln.strip().startswith("```"):
            units.append({"type": "code_fence", "line": i})
    return {
        "units": units,
        "unit_count": len(units),
        "deterministic_inputs": [f"units={len(units)}"],
    }
