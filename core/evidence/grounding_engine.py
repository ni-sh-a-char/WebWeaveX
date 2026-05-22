from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.evidence.semantic_conservatism_engine import apply_semantic_conservatism
from core.evidence.semantic_integrity_engine import build_semantic_integrity_object


def ground_parser_output(parsed: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(parsed, dict):
        from core.evidence.provenance_engine import build_provenance

        return build_provenance([], grounding={})
    flags = parsed.get("parser_evidence", parsed.get("evidence", {}))
    if not isinstance(flags, dict):
        flags = {}
    symbols = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
    parsed_facts = {
        "language": parsed.get("language", "text"),
        "classes": list(symbols.get("classes", []) or [])[:50],
        "functions": list(symbols.get("functions", []) or [])[:50],
        "imports": list(symbols.get("imports", []) or [])[:50],
    }
    return build_semantic_integrity_object(
        parsed_facts=parsed_facts,
        parser_payload=parsed,
        lineage_stages=[{"stage": "parser", "inputs": [], "outputs": [f"parser:{k}" for k, v in sorted(flags.items()) if v]}],
    )


def structure_cognition(
    observed: Dict[str, Any],
    inferred: Dict[str, Any],
    reconciled: Dict[str, Any],
    parsed: Dict[str, Any] | None = None,
    contradicted: Optional[Dict[str, Any]] = None,
    ambiguities: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    derived = {"structure": "cognition_bundle"}
    if parsed and reconciled != observed:
        derived["reconciliation_applied"] = True
    amb = list(ambiguities or [])
    if inferred and not observed:
        amb.append("inferred_without_direct_observation")
    parsed_facts = {}
    if parsed:
        sym = parsed.get("symbols", {}) if isinstance(parsed.get("symbols"), dict) else {}
        parsed_facts = {
            "language": parsed.get("language", "text"),
            "classes": list(sym.get("classes", []) or [])[:30],
            "functions": list(sym.get("functions", []) or [])[:30],
        }
    bundle = build_semantic_integrity_object(
        observed=observed,
        parsed_facts=parsed_facts,
        inferred=inferred,
        reconciled=reconciled,
        contradicted=contradicted or {},
        derived=derived,
        ambiguities=amb,
        parser_payload=parsed,
        lineage_stages=[
            {"stage": "observe", "inputs": [], "outputs": sorted(observed.keys())},
            {"stage": "infer", "inputs": sorted(observed.keys()), "outputs": sorted(inferred.keys())},
            {"stage": "reconcile", "inputs": sorted(inferred.keys()), "outputs": sorted(reconciled.keys())},
        ],
    )
    from core.semantic.semantic_uncertainty_engine import apply_semantic_uncertainty

    return apply_semantic_uncertainty(apply_semantic_conservatism(bundle))
