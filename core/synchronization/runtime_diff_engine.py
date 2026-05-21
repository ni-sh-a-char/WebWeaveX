from __future__ import annotations

from typing import Any, Dict


def diff_runtime_state(
    previous: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    runtime_changes = []
    semantic_mutations = []
    workflow_mutations = []
    distributed_changes = []

    for key in sorted(set(previous.keys()) | set(current.keys())):
        if previous.get(key) == current.get(key):
            continue
        entry = {"field": key, "from": previous.get(key), "to": current.get(key)}
        if "semantic" in key:
            semantic_mutations.append(entry)
        elif "workflow" in key:
            workflow_mutations.append(entry)
        elif "distributed" in key or "worker" in key:
            distributed_changes.append(entry)
        else:
            runtime_changes.append(entry)

    return {
        "runtime_changes": runtime_changes,
        "semantic_mutations": semantic_mutations,
        "workflow_mutations": workflow_mutations,
        "distributed_changes": distributed_changes,
        "bounded": True,
    }
