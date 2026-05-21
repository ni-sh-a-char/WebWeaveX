from __future__ import annotations

from typing import Any, Dict, List


def build_workflow_dependencies(
    plan: Dict[str, Any],
) -> Dict[str, Any]:
    ordering: List[Dict[str, Any]] = []
    prerequisites: List[Dict[str, Any]] = []
    runtime_deps: List[Dict[str, Any]] = []
    chains: List[Dict[str, Any]] = []

    steps = list(plan.get("steps", []))
    for index, step in enumerate(steps[:10000]):
        depends_on = str(step.get("depends_on", ""))
        if depends_on:
            ordering.append({
                "step": str(step.get("id", "")),
                "depends_on": depends_on,
            })
            prerequisites.append({
                "step": str(step.get("id", "")),
                "requires": depends_on,
            })

        if index > 0:
            prev_runtime = str(steps[index - 1].get("runtime", ""))
            curr_runtime = str(step.get("runtime", ""))
            if prev_runtime != curr_runtime:
                runtime_deps.append({
                    "from": prev_runtime,
                    "to": curr_runtime,
                })

        chains.append({
            "step": str(step.get("id", "")),
            "action": str(step.get("action", "")),
        })

    return {
        "execution_ordering": ordering,
        "semantic_prerequisites": prerequisites,
        "runtime_dependencies": runtime_deps,
        "extraction_chains": chains,
        "bounded": True,
    }
