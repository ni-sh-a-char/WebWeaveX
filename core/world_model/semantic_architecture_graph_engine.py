from __future__ import annotations

from typing import Any, Dict, List

from ._normalize import normalize_imports


def build_semantic_architecture_graph(
    repository_irs: List[Dict[str, Any]],
) -> Dict[str, Any]:

    nodes = []
    edges = []

    for ir in repository_irs:

        path = ir.get("path")

        nodes.append(
            {
                "id": path,
                "kind": "repository_file",
            }
        )

        semantic_ast = ir.get(
            "semantic_ast",
            {},
        )

        for item in normalize_imports(semantic_ast):

            target = item.get("module")

            if target:

                edges.append(
                    {
                        "from": path,
                        "to": target,
                        "relation": "architectural_dependency",
                    }
                )

    return {
        "nodes": sorted(
            nodes,
            key=lambda x: str(x["id"]),
        ),
        "edges": sorted(
            edges,
            key=lambda x: (
                str(x["from"]),
                str(x["to"]),
            ),
        ),
    }
