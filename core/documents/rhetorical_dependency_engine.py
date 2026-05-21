from __future__ import annotations

from typing import Any, Dict

from core.documents.rhetorical_parser_engine import parse_rhetorical_structure


def build_rhetorical_dependencies(text: str) -> Dict[str, Any]:
    rhet = parse_rhetorical_structure(text)
    units = rhet.get("units", [])
    deps = []
    for i in range(len(units) - 1):
        deps.append({"from": units[i].get("title", f"u{i}"), "to": units[i + 1].get("title", f"u{i+1}"), "relation": "elaborates"})
    return {"dependencies": deps, "units": units, "evidence": ["discourse:rhetorical"]}
