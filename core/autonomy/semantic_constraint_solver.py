from __future__ import annotations

from typing import Any, Dict, List


def solve_semantic_constraints(
    constraints: List[Dict[str, Any]],
) -> Dict[str, Any]:

    valid = []

    invalid = []

    for constraint in constraints:

        if constraint.get("valid", True):
            valid.append(constraint)
        else:
            invalid.append(constraint)

    return {
        "valid_constraints": valid,
        "invalid_constraints": invalid,
    }
