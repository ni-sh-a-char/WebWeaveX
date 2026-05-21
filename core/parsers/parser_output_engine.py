from __future__ import annotations

from typing import Any, Dict

from core.evidence.grounding_engine import ground_parser_output
from core.parsers.parser_cognition_engine import build_parser_cognition_evidence


def normalize_parser_output(parsed: Dict[str, Any]) -> Dict[str, Any]:
    sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    cognition = build_parser_cognition_evidence(parsed)
    return {
        "symbol_names": sorted(sym.get("symbols", []) or []),
        "import_names": sorted(sym.get("imports", []) or []),
        "export_names": sorted(sym.get("exports", []) or []),
        "function_names": sorted(sym.get("functions", []) or []),
        "class_names": sorted(sym.get("classes", []) or []),
        "interface_names": sorted(sym.get("interfaces", []) or []),
        "trait_names": sorted(sym.get("traits", []) or []),
        "decorator_names": sorted(sym.get("decorators", []) or []),
        "annotation_names": sorted(sym.get("annotations", []) or []),
        "dependency_names": sorted((parsed.get("dependencies", {}) or {}).get("dependencies", []) or []),
        "call_graph": parsed.get("calls", {}),
        "semantic_graph": parsed.get("semantic_graph", {}),
        "runtime_evidence": parsed.get("runtime", {}),
        "framework_evidence": parsed.get("frameworks", {}),
        "api_evidence": parsed.get("api_surface", {}),
        "parser_evidence": parsed.get("evidence", {}),
        "grounding": ground_parser_output(parsed),
        "parser_evidence_list": cognition.get("parser_evidence", []),
        "semantic_evidence_list": cognition.get("semantic_evidence", []),
        "graph_evidence_list": cognition.get("graph_evidence", []),
        "cognition_lineage": cognition.get("lineage", {}),
        "language": parsed.get("language", "text"),
        "source_id": parsed.get("source_id", ""),
    }
