from __future__ import annotations

from typing import Any, Dict, List

from ._normalize import normalize_imports


def build_cross_file_dependencies(
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    edges = []

    known_paths = {
        ir.get("path")
        for ir in repository_irs
    }

    for ir in repository_irs:

        source = ir.get("path")

        semantic_ast = ir.get(
            "semantic_ast",
            {},
        )

        for item in normalize_imports(semantic_ast):

            target = item.get("module")

            if target in known_paths:

                edges.append(
                    {
                        "from": source,
                        "to": target,
                        "relation": "cross_file_dependency",
                    }
                )

    return {
        "edges": sorted(
            edges,
            key=lambda x: (
                str(x["from"]),
                str(x["to"]),
            ),
        ),
    }
