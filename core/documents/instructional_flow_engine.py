from __future__ import annotations

from typing import Any, Dict, List

from core.documents.rhetorical_structure_engine import extract_rhetorical_structure


def extract_instructional_flow(text: str) -> Dict[str, Any]:
    rhet = extract_rhetorical_structure(text)
    steps: List[Dict[str, Any]] = []
    for u in rhet["units"]:
        if u.get("type") == "heading":
            title = str(u.get("title", "")).lower()
            if any(k in title for k in ("step", "tutorial", "install", "setup", "prerequisite")):
                steps.append({"title": u.get("title"), "line": u.get("line")})
            elif u.get("level", 9) <= 2:
                steps.append({"title": u.get("title"), "line": u.get("line"), "implicit": True})
    return {"steps": steps, "prerequisites": [s["title"] for s in steps[:-1]], "deterministic_inputs": [f"steps={len(steps)}"]}
