from __future__ import annotations

from typing import Dict, List, Union

from core.evidence import structure_cognition
from core.parsers import parse_source


def infer_service_boundaries_from_text(text: str, path: str = "") -> Dict[str, object]:
    parsed = parse_source(text, path=path)
    symbol_data = parsed.get("symbols", {})
    if isinstance(symbol_data, list):
        classes = symbol_data
    else:
        classes = symbol_data.get("classes", []) if isinstance(symbol_data, dict) else []
    calls = (parsed.get("call_graph") or parsed.get("calls", {})).get("calls", [])
    api = parsed.get("api_evidence") or parsed.get("api_surface", {})
    observed = {
        "services": sorted(
            n for n in classes
            if any(h in str(n).lower() for h in ("service", "worker", "handler", "controller"))
        ),
        "call_edges": len(calls),
        "api_routes": api.get("routes", []) if isinstance(api, dict) else [],
    }
    inferred = {
        "services": sorted(classes)[:10],
        "call_edges": len(calls),
    }
    reconciled = {
        "services": observed["services"] or inferred["services"],
        "call_edges": observed["call_edges"],
        "api_routes": observed["api_routes"],
    }
    out = structure_cognition(observed, inferred, reconciled, parsed=parsed)
    cognition = parsed and {
        "parser_evidence": out.get("evidence", []),
        "semantic_evidence": [f"service:{s}" for s in reconciled.get("services", [])],
        "graph_evidence": [f"call_edge:{i}" for i in range(observed.get("call_edges", 0))],
        "lineage": out.get("lineage", {}),
    }
    out["services"] = reconciled.get("services", [])
    out["boundaries"] = reconciled.get("boundaries", [])
    out["topology_layers"] = {
        "observed": observed,
        "parser_derived": {"services": inferred.get("services", []), "calls": observed.get("call_edges", 0)},
        "inferred": inferred,
        "reconciled": reconciled,
        "ambiguous": out.get("ambiguities", []),
        "contradicted": out.get("contradicted", {}),
    }
    if cognition:
        out.update({k: v for k, v in cognition.items() if k not in out})
    return out


def infer_service_boundaries_from_paths(paths: List[str]) -> Dict[str, object]:
    groups: Dict[str, List[str]] = {}
    for p in sorted(set(paths or [])):
        key = p.split("/")[0] if "/" in p else p.split("\\")[0]
        groups.setdefault(key, []).append(p)
    observed = {"boundaries": [{"service": k, "paths": sorted(v)} for k, v in sorted(groups.items())]}
    out = structure_cognition(observed, observed, observed, parsed=None)
    out["boundaries"] = observed.get("boundaries", [])
    return out


def infer_service_boundaries(text_or_paths: Union[str, List[str]], path: str = "") -> Dict[str, object]:
    if isinstance(text_or_paths, list):
        return infer_service_boundaries_from_paths(text_or_paths)
    return infer_service_boundaries_from_text(text_or_paths, path=path)
