from __future__ import annotations

from typing import Any, Dict

from core.evidence.evidence_graph_engine import build_evidence_graph


def build_parser_evidence_graph(parsed: Dict[str, Any]) -> Dict[str, Any]:
    claims = []
    if not isinstance(parsed, dict):
        return {"nodes": [], "edges": []}
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    for name in sym.get("classes", []) or []:
        claims.append({"id": f"class:{name}", "sources": ["parser:symbols"]})
    for name in sym.get("functions", []) or []:
        claims.append({"id": f"func:{name}", "sources": ["parser:symbols"]})
    for dep in (parsed.get("dependencies", {}) or {}).get("dependencies", []) if isinstance(parsed.get("dependencies"), dict) else []:
        claims.append({"id": f"dep:{dep}", "sources": ["parser:dependencies"]})
    return build_evidence_graph(claims)
