from __future__ import annotations

from typing import Any, Dict

from core.documents.section_engine import extract_sections
from core.evidence import structure_cognition


def extract_tutorial_flow(text: str) -> Dict[str, Any]:
    hierarchy = extract_sections(text or "").get("hierarchy", [])
    steps = [h.get("title", "") for h in hierarchy if h.get("title")]
    evidence_kind = "section_hierarchy"
    if not steps:
        import re

        steps = sorted(set(re.findall(r"^\s*\d+\.\s+(.+)$", text or "", flags=re.MULTILINE)))
        evidence_kind = "numbered_list_fallback"
    observed = {"steps": steps}
    inferred = {
        "requires_prior": [
            {"step": steps[i], "requires": steps[i - 1]}
            for i in range(1, len(steps))
            if steps[i] and steps[i - 1]
        ],
    }
    reconciled = {
        "steps": steps,
        "flow_edges": [{"from": steps[i], "to": steps[i + 1]} for i in range(max(0, len(steps) - 1))],
    }
    result = structure_cognition(observed, inferred, reconciled, parsed=None)
    result["confidence_basis"] = {**result.get("confidence_basis", {}), "flow_evidence": evidence_kind}
    return result
