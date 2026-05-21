from __future__ import annotations

from typing import Any, Dict, List

from core.evidence.lineage_engine import build_lineage


def build_parser_cognition_evidence(parsed: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(parsed, dict):
        return {
            "parser_evidence": [],
            "semantic_evidence": [],
            "graph_evidence": [],
            "lineage": build_lineage([]),
        }
    flags = parsed.get("parser_evidence", parsed.get("evidence", {}))
    if not isinstance(flags, dict):
        flags = {}
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    parser_evidence: List[str] = [f"parser:{k}" for k, v in sorted(flags.items()) if v]
    for name in sym.get("classes", []) or []:
        parser_evidence.append(f"symbol:class:{name}")
    for name in sym.get("functions", []) or []:
        parser_evidence.append(f"symbol:function:{name}")
    semantic_evidence: List[str] = []
    deps = (parsed.get("dependencies", {}) or {}).get("dependencies", [])
    for d in deps or []:
        semantic_evidence.append(f"dependency:{d}")
    graph = parsed.get("semantic_graph", {}) or {}
    graph_evidence = [f"graph:edge:{e.get('from')}->{e.get('to')}" for e in (graph.get("edges", []) or [])[:50] if isinstance(e, dict)]
    lineage = build_lineage(
        [
            {
                "stage": "parser_cognition",
                "inputs": [],
                "outputs": sorted(parser_evidence[:20]),
            }
        ]
    )
    return {
        "parser_evidence": sorted(set(parser_evidence)),
        "semantic_evidence": sorted(set(semantic_evidence)),
        "graph_evidence": sorted(set(graph_evidence)),
        "lineage": lineage,
    }
