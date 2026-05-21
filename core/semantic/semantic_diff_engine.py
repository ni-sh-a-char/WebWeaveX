from __future__ import annotations

from typing import Any, Dict


def diff_semantic_runtime(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    prev_entities = {
        str(item.get("id", ""))
        for item in previous.get("entities", {}).get("entities", [])
    }
    curr_entities = {
        str(item.get("id", ""))
        for item in current.get("entities", {}).get("entities", [])
    }

    prev_domain = previous.get("domain", {}).get("domain", "")
    curr_domain = current.get("domain", {}).get("domain", "")

    return {
        "entities_added": sorted(curr_entities - prev_entities),
        "entities_removed": sorted(prev_entities - curr_entities),
        "domain_changed": prev_domain != curr_domain,
        "ontology_evolved": previous.get("ontology") != current.get("ontology"),
        "workflow_mutated": (
            previous.get("workflow") != current.get("workflow")
        ),
        "bounded": True,
    }
