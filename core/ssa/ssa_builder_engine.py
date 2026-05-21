from __future__ import annotations

import ast
from typing import Any, Dict, List


def build_ssa_form(code: str) -> Dict[str, Any]:

    tree = ast.parse(code)

    counters: Dict[str, int] = {}

    assignments: List[Dict[str, Any]] = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            for target in node.targets:

                if isinstance(target, ast.Name):

                    name = target.id

                    counters[name] = counters.get(name, 0) + 1

                    assignments.append({
                        "variable": name,
                        "ssa_name": f"{name}_{counters[name]}",
                        "lineno": getattr(node, "lineno", None),
                    })

    return {
        "ssa_assignments": assignments,
        "variable_versions": counters,
        "bounded": True,
        "deterministic": True,
    }
